"""Barebones tf-tree style frame manager.

This module intentionally implements a small subset of the ideas from:
T. Foote, "tf: The Transform Library", TePRA 2013.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
import math
from typing import Dict, List, Tuple


class TransformLookupError(RuntimeError):
    """Raised when a transform query cannot be satisfied."""


def _wrap_angle(angle_rad: float) -> float:
    """Wrap an angle to [-pi, pi]."""
    return (angle_rad + math.pi) % (2.0 * math.pi) - math.pi


@dataclass(frozen=True)
class SE2Transform:
    """2D rigid transform (x, y, yaw).

    Naming follows tf-style notation:
    `parent_from_child` means it maps points from child frame to parent frame.
    """

    x: float
    y: float
    yaw: float

    @staticmethod
    def identity() -> "SE2Transform":
        return SE2Transform(0.0, 0.0, 0.0)

    def compose(self, other: "SE2Transform") -> "SE2Transform":
        """Return self * other in transform-chain order."""
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)

        x = self.x + cos_yaw * other.x - sin_yaw * other.y
        y = self.y + sin_yaw * other.x + cos_yaw * other.y
        yaw = _wrap_angle(self.yaw + other.yaw)
        return SE2Transform(x, y, yaw)

    def inverse(self) -> "SE2Transform":
        """Return inverse transform."""
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)

        x = -(cos_yaw * self.x + sin_yaw * self.y)
        y = -(-sin_yaw * self.x + cos_yaw * self.y)
        return SE2Transform(x, y, _wrap_angle(-self.yaw))

    def apply_to_point(self, px: float, py: float) -> Tuple[float, float]:
        """Apply transform to a 2D point."""
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)
        tx = self.x + cos_yaw * px - sin_yaw * py
        ty = self.y + sin_yaw * px + cos_yaw * py
        return tx, ty

    @staticmethod
    def interpolate(a: "SE2Transform", b: "SE2Transform", alpha: float) -> "SE2Transform":
        """Linear interpolation in SE2 (translation + shortest-angle yaw)."""
        x = a.x + alpha * (b.x - a.x)
        y = a.y + alpha * (b.y - a.y)
        dyaw = _wrap_angle(b.yaw - a.yaw)
        yaw = _wrap_angle(a.yaw + alpha * dyaw)
        return SE2Transform(x, y, yaw)


class _TimedTransformBuffer:
    """Chronologically sorted transform history for one tree edge."""

    def __init__(self) -> None:
        self._times: List[float] = []
        self._transforms: List[SE2Transform] = []

    def add_sample(self, timestamp: float, transform: SE2Transform) -> None:
        idx = bisect_left(self._times, timestamp)
        if idx < len(self._times) and self._times[idx] == timestamp:
            self._transforms[idx] = transform
            return
        self._times.insert(idx, timestamp)
        self._transforms.insert(idx, transform)

    def latest_time(self) -> float:
        if not self._times:
            raise TransformLookupError("No transform samples stored for edge.")
        return self._times[-1]

    def earliest_time(self) -> float:
        if not self._times:
            raise TransformLookupError("No transform samples stored for edge.")
        return self._times[0]

    def lookup(self, timestamp: float) -> SE2Transform:
        if not self._times:
            raise TransformLookupError("No transform samples stored for edge.")

        if timestamp < self._times[0] or timestamp > self._times[-1]:
            raise TransformLookupError(
                f"Time {timestamp} outside edge history [{self._times[0]}, {self._times[-1]}]."
            )

        right = bisect_right(self._times, timestamp)
        left = right - 1

        if self._times[left] == timestamp:
            return self._transforms[left]

        if right >= len(self._times):
            return self._transforms[-1]

        t0, t1 = self._times[left], self._times[right]
        alpha = (timestamp - t0) / (t1 - t0)
        return SE2Transform.interpolate(self._transforms[left], self._transforms[right], alpha)


class TFTree:
    """Minimal tf-like frame tree with time-stamped edge histories.

    Design choices borrowed from the paper:
    - Tree-only graph (acyclic, one parent per child).
    - Per-edge time history with interpolation.
    - Queries between arbitrary frames by walking to a common ancestor.
    """

    def __init__(self) -> None:
        self._parent_of: Dict[str, str] = {}
        self._buffers: Dict[str, _TimedTransformBuffer] = {}
        self._frames: set[str] = set()

    def set_transform(
        self,
        parent_frame: str,
        child_frame: str,
        parent_from_child: SE2Transform,
        timestamp: float,
    ) -> None:
        """Insert/update one directed edge sample at a timestamp."""
        if parent_frame == child_frame:
            raise ValueError("A frame cannot be its own parent.")
        if timestamp < 0.0:
            raise ValueError("Timestamp must be non-negative.")

        # Re-parenting is allowed by tf semantics, but we avoid mixing old and
        # new parent histories in the same edge buffer.
        if child_frame in self._parent_of and self._parent_of[child_frame] != parent_frame:
            if self._would_create_cycle(parent_frame, child_frame):
                raise ValueError("Re-parenting would create a cycle in the tree.")
            self._buffers[child_frame] = _TimedTransformBuffer()

        if child_frame not in self._parent_of and self._would_create_cycle(parent_frame, child_frame):
            raise ValueError("Edge insertion would create a cycle in the tree.")

        self._parent_of[child_frame] = parent_frame
        self._frames.add(parent_frame)
        self._frames.add(child_frame)
        self._buffers.setdefault(child_frame, _TimedTransformBuffer()).add_sample(
            timestamp, parent_from_child
        )

    def lookup_transform(
        self,
        source_frame: str,
        target_frame: str,
        timestamp: float,
    ) -> SE2Transform:
        """Return target_from_source at requested time.

        If `timestamp == 0.0`, this behaves like tf's "latest common time" query.
        """
        self._validate_known_frame(source_frame)
        self._validate_known_frame(target_frame)

        if source_frame == target_frame:
            return SE2Transform.identity()

        resolved_time = (
            self._latest_common_time(source_frame, target_frame)
            if timestamp == 0.0
            else timestamp
        )

        source_map, source_chain = self._ancestor_map(source_frame, resolved_time)
        target_map, _ = self._ancestor_map(target_frame, resolved_time)

        common = next((f for f in source_chain if f in target_map), None)
        if common is None:
            raise TransformLookupError(
                f"No connection between '{source_frame}' and '{target_frame}'."
            )

        common_from_source = source_map[common]
        common_from_target = target_map[common]
        return common_from_target.inverse().compose(common_from_source)

    def transform_point(
        self,
        point_xy: Tuple[float, float],
        source_frame: str,
        target_frame: str,
        timestamp: float,
    ) -> Tuple[float, float]:
        """Transform a point from source frame to target frame."""
        target_from_source = self.lookup_transform(source_frame, target_frame, timestamp)
        return target_from_source.apply_to_point(point_xy[0], point_xy[1])

    def _validate_known_frame(self, frame: str) -> None:
        if frame not in self._frames:
            raise TransformLookupError(f"Unknown frame '{frame}'.")

    def _would_create_cycle(self, parent_frame: str, child_frame: str) -> bool:
        current = parent_frame
        while current in self._parent_of:
            if current == child_frame:
                return True
            current = self._parent_of[current]
        return current == child_frame

    def _ancestor_map(
        self, frame: str, timestamp: float
    ) -> Tuple[Dict[str, SE2Transform], List[str]]:
        """Return mapping: ancestor -> ancestor_from_frame, and ancestor chain."""
        chain: List[str] = [frame]
        ancestor_from_frame: Dict[str, SE2Transform] = {frame: SE2Transform.identity()}

        current = frame
        running = SE2Transform.identity()
        while current in self._parent_of:
            parent = self._parent_of[current]
            parent_from_current = self._buffers[current].lookup(timestamp)
            running = parent_from_current.compose(running)
            chain.append(parent)
            ancestor_from_frame[parent] = running
            current = parent

        return ancestor_from_frame, chain

    def _path_children_to_common(self, frame: str, common: str) -> List[str]:
        children: List[str] = []
        current = frame
        while current != common:
            if current not in self._parent_of:
                raise TransformLookupError(f"No path from '{frame}' to '{common}'.")
            children.append(current)
            current = self._parent_of[current]
        return children

    def _latest_common_time(self, source_frame: str, target_frame: str) -> float:
        # Find a common ancestor by structure only, then intersect time ranges
        # for all edges on the source->common and target->common paths.
        source_ancestors = []
        cur = source_frame
        source_set = set()
        while True:
            source_ancestors.append(cur)
            source_set.add(cur)
            if cur not in self._parent_of:
                break
            cur = self._parent_of[cur]

        common = None
        cur = target_frame
        while True:
            if cur in source_set:
                common = cur
                break
            if cur not in self._parent_of:
                break
            cur = self._parent_of[cur]

        if common is None:
            raise TransformLookupError(
                f"No connection between '{source_frame}' and '{target_frame}'."
            )

        edge_children = self._path_children_to_common(source_frame, common)
        edge_children.extend(self._path_children_to_common(target_frame, common))

        if not edge_children:
            return 0.0

        earliest = max(self._buffers[child].earliest_time() for child in edge_children)
        latest = min(self._buffers[child].latest_time() for child in edge_children)

        if earliest > latest:
            raise TransformLookupError(
                "No overlapping time window across transform path "
                f"between '{source_frame}' and '{target_frame}'."
            )
        return latest
