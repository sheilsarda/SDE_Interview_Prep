import numpy as np
from scipy.spatial.transform import Rotation, Slerp
import bisect
from typing import Dict, Tuple, List, Optional

# ==========================================
# Exceptions
# ==========================================
class TFException(Exception): 
    pass

class ExtrapolationException(TFException): 
    pass

class ConnectivityException(TFException): 
    pass


# ==========================================
# 1. Spatial Math: SE(3) Transform
# ==========================================
class SE3Transform:
    """3D rigid transform (translation + quaternion)."""
    def __init__(self, translation: np.ndarray, rotation: Rotation):
        self.translation = np.asarray(translation, dtype=float)
        self.rotation = rotation

    @staticmethod
    def identity() -> 'SE3Transform':
        return SE3Transform(np.zeros(3), Rotation.from_quat([0, 0, 0, 1]))

    def compose(self, other: 'SE3Transform') -> 'SE3Transform':
        new_translation = self.translation + self.rotation.apply(other.translation)
        new_rotation = self.rotation * other.rotation
        return SE3Transform(new_translation, new_rotation)

    def inverse(self) -> 'SE3Transform':
        inv_rotation = self.rotation.inv()
        inv_translation = inv_rotation.apply(-self.translation)
        return SE3Transform(inv_translation, inv_rotation)

    def interpolate(self, other: 'SE3Transform', alpha: float) -> 'SE3Transform':
        """
        Linearly interpolates translation and spherically interpolates (Slerp) rotation.
        alpha is between 0.0 and 1.0.
        """
        # Translation Lerp
        t_interp = self.translation + alpha * (other.translation - self.translation)
        
        # Rotation Slerp
        times = [0.0, 1.0]
        rotations = Rotation.concatenate([self.rotation, other.rotation])
        slerp_algo = Slerp(times, rotations)
        r_interp = slerp_algo([alpha])[0]
        
        return SE3Transform(t_interp, r_interp)

    def apply_to_point(self, point: np.ndarray) -> np.ndarray:
        return self.translation + self.rotation.apply(point)

    def __repr__(self):
        return f"SE3(t={self.translation}, q={self.rotation.as_quat()})"


# ==========================================
# 2. Temporal Math: Time Cache / Ring Buffer
# ==========================================
class TimeCache:
    """Stores a time-sorted history of transforms for a single frame link."""
    def __init__(self, max_duration: float = 10.0):
        self.max_duration = max_duration
        self.times: List[float] = []
        self.transforms: List[SE3Transform] = []

    def insert(self, time: float, transform: SE3Transform) -> None:
        """Inserts a transform and prunes old data."""
        # Fast path: appending newest data
        if not self.times or time >= self.times[-1]:
            self.times.append(time)
            self.transforms.append(transform)
        else:
            # Handle out-of-order data via binary insertion
            idx = bisect.bisect_right(self.times, time)
            self.times.insert(idx, time)
            self.transforms.insert(idx, transform)

        # Garbage collection: Prune data older than max_duration
        latest_time = self.times[-1]
        cutoff_time = latest_time - self.max_duration
        
        prune_idx = bisect.bisect_left(self.times, cutoff_time)
        if prune_idx > 0:
            # Keep one older transform just outside the window for interpolation
            prune_idx = max(0, prune_idx - 1)
            self.times = self.times[prune_idx:]
            self.transforms = self.transforms[prune_idx:]

    def get_transform(self, time: float) -> SE3Transform:
        """Returns the exact or interpolated transform at the requested time."""
        if not self.times:
            raise TFException("Cache is empty.")

        # Extrapolation Checks
        if time < self.times[0]:
            raise ExtrapolationException(f"Requested time {time} is before oldest data {self.times[0]}.")
        if time > self.times[-1]:
            raise ExtrapolationException(f"Requested time {time} is after newest data {self.times[-1]}.")

        # Binary search for the surrounding timestamps
        idx = bisect.bisect_left(self.times, time)
        
        if self.times[idx] == time:
            return self.transforms[idx]

        # Interpolate between idx-1 and idx
        t1, trans1 = self.times[idx - 1], self.transforms[idx - 1]
        t2, trans2 = self.times[idx], self.transforms[idx]
        
        alpha = (time - t1) / (t2 - t1)
        return trans1.interpolate(trans2, alpha)


# ==========================================
# 3. Graph Math: Time-Aware Transform Tree
# ==========================================
class TimeAwareTransformTree:
    """A directed forest representing the ROS tf tree across time."""
    def __init__(self):
        # Maps child_frame -> (parent_frame, TimeCache)
        self._tree: Dict[str, Tuple[str, TimeCache]] = {}

    def set_transform(self, parent: str, child: str, time: float, transform: SE3Transform) -> None:
        if parent == child:
            raise ValueError("Parent and child cannot be the same frame.")
        
        if child not in self._tree or self._tree[child][0] != parent:
            self._tree[child] = (parent, TimeCache())
            
        self._tree[child][1].insert(time, transform)

    def _get_path_to_root(self, frame: str) -> List[str]:
        path = [frame]
        current = frame
        while current in self._tree:
            parent = self._tree[current][0]
            current = parent
            path.append(current)
        return path

    def _latest_common_time(self, source_frame: str, target_frame: str) -> float:
        """Calculates the most recent timestamp where a continuous chain exists."""
        source_path = self._get_path_to_root(source_frame)
        target_path = self._get_path_to_root(target_frame)

        lca = next((f for f in source_path if f in target_path), None)
        if lca is None:
            raise ConnectivityException("Frames are not connected.")

        links = []
        for path in (source_path, target_path):
            current = path[0]
            while current != lca:
                links.append(current)
                current = self._tree[current][0]

        if not links:
            return 0.0

        max_oldest_time = -float('inf')
        min_newest_time = float('inf')

        for child in links:
            cache = self._tree[child][1]
            if not cache.times:
                raise TFException(f"No data for link {child}")
                
            max_oldest_time = max(max_oldest_time, cache.times[0])
            min_newest_time = min(min_newest_time, cache.times[-1])

        if max_oldest_time > min_newest_time:
            raise ExtrapolationException("No overlapping time window exists across the transform chain.")

        return min_newest_time

    def lookup_transform(self, target_frame: str, source_frame: str, time: float = 0.0) -> SE3Transform:
        """
        Resolves T_target_source at a specific time. 
        If time == 0.0, it resolves to the latest common time.
        """
        if target_frame == source_frame:
            return SE3Transform.identity()

        query_time = time if time != 0.0 else self._latest_common_time(source_frame, target_frame)

        source_path = self._get_path_to_root(source_frame)
        target_path = self._get_path_to_root(target_frame)

        lca = next((f for f in source_path if f in target_path), None)
        if lca is None:
            raise ConnectivityException(f"No path between {source_frame} and {target_frame}")

        # Walk up from source to LCA
        t_lca_source = SE3Transform.identity()
        current = source_frame
        while current != lca:
            parent, cache = self._tree[current]
            t_parent_child = cache.get_transform(query_time)
            t_lca_source = t_parent_child.compose(t_lca_source)
            current = parent

        # Walk up from target to LCA
        t_lca_target = SE3Transform.identity()
        current = target_frame
        while current != lca:
            parent, cache = self._tree[current]
            t_parent_child = cache.get_transform(query_time)
            t_lca_target = t_parent_child.compose(t_lca_target)
            current = parent

        # Compose final transform
        t_target_lca = t_lca_target.inverse()
        return t_target_lca.compose(t_lca_source)