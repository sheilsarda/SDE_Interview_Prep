# ROS 2 & Core Robotics Algorithms — Interview Question Bank

> **Format:** Coderpad-style virtual interview
> **Time per question:** ~45 minutes
> **Level:** Senior / Staff Robotics Software Engineer
> **Language:** Python (ROS 2 rclpy), NumPy where needed

---

## Question 1: Lifecycle Nodes and QoS Mismatch Debugging

### Problem

You are building a sensor processing pipeline. You have a LIDAR driver node publishing `sensor_msgs/LaserScan` on `/scan`, and a downstream obstacle detection node subscribing to it.

**Part A (Theory, ~10 min)**

Explain what a lifecycle (managed) node is in ROS 2, how it differs from a regular unmanaged node, what the state transitions are, and why you would use one for the LIDAR driver in this scenario. What are the alternatives to lifecycle nodes for managing startup/shutdown ordering, and what are the tradeoffs?

**Part B (Theory, ~10 min)**

The obstacle detection node is subscribing but receiving zero messages. The LIDAR driver node is confirmed publishing. Both are in the same DDS domain. Walk through how you would systematically debug this. At some point in your debugging you discover it is a QoS mismatch. Explain the QoS compatibility rules in ROS 2. Specifically:

- What happens when a publisher uses `BEST_EFFORT` reliability and a subscriber uses `RELIABLE`?
- What about the reverse?
- How does durability (`VOLATILE` vs. `TRANSIENT_LOCAL`) factor in?

**Part C (Code, ~25 min)**

Write a ROS 2 Python lifecycle node for the LIDAR driver that:

1. In `on_configure`: creates the publisher with a specific QoS profile (reliable, transient local durability, queue depth 10)
2. In `on_activate`: starts a timer that publishes a dummy `LaserScan` message at 10 Hz
3. In `on_deactivate`: cancels the timer
4. In `on_cleanup`: destroys the publisher

Then write the corresponding subscriber node (can be a regular node) with a **compatible** QoS profile and a callback that logs the min range value from each scan.

---

### A+ Response Benchmark

#### Part A — Lifecycle Nodes

The candidate should explain:

- The four primary states: **Unconfigured**, **Inactive**, **Active**, **Finalized**.
- The transition callbacks: `on_configure`, `on_activate`, `on_deactivate`, `on_cleanup`, `on_shutdown`, and `on_error`.
- The key insight: lifecycle nodes separate **resource allocation** (configure) from **data flow** (activate). This lets you bring up a LIDAR driver, verify the hardware connection, allocate buffers, and only start publishing when the entire pipeline is ready.
- Alternatives:
  - **Launch event handlers** for sequencing (e.g., `RegisterEventHandler` + `OnProcessStart`). Simpler but coarse-grained, no health management.
  - **Component composition** with manual readiness flags via parameters or topics. Flexible but ad-hoc.
  - **A health/orchestrator node** that monitors heartbeats and triggers startup. More robust but more code.
- Lifecycle nodes are the ROS 2 native answer but add complexity. If you do not need deterministic bringup or managed teardown, a regular node is simpler.

#### Part B — QoS Debugging

The candidate should identify the core compatibility rule: **the subscriber's QoS must be equal to or less strict than the publisher's**.

| Publisher | Subscriber | Compatible? |
|-----------|-----------|-------------|
| `BEST_EFFORT` | `RELIABLE` | No (sub is stricter) |
| `RELIABLE` | `BEST_EFFORT` | Yes (sub is less strict) |
| `VOLATILE` | `TRANSIENT_LOCAL` | No (sub expects late-join data pub won't provide) |
| `TRANSIENT_LOCAL` | `VOLATILE` | Yes |

Debugging steps:

1. `ros2 topic list` to verify topic name matches
2. `ros2 topic info /scan -v` to inspect QoS on both endpoints
3. Check domain ID (`ROS_DOMAIN_ID`)
4. Check DDS implementation match (`RMW_IMPLEMENTATION`)
5. `ros2 doctor` for general diagnostics

Bonus: mention `QoSIncompatibleEvent` callbacks (`on_offered_incompatible_qos` / `on_requested_incompatible_qos`) for runtime detection.

#### Part C — Code

```python
import rclpy
from rclpy.lifecycle import Node as LifecycleNode
from rclpy.lifecycle import TransitionCallbackReturn
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import LaserScan
import math
import random


class LifecycleLidarDriver(LifecycleNode):
    def __init__(self):
        super().__init__('lifecycle_lidar_driver')
        self._publisher = None
        self._timer = None
        self.get_logger().info('Node constructed (Unconfigured)')

    def on_configure(self, state):
        self.get_logger().info('Configuring...')
        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._publisher = self.create_lifecycle_publisher(LaserScan, '/scan', qos)
        self.get_logger().info('Publisher created with RELIABLE / TRANSIENT_LOCAL QoS')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state):
        self.get_logger().info('Activating...')
        timer_period = 0.1  # 10 Hz
        self._timer = self.create_timer(timer_period, self._publish_scan)
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state):
        self.get_logger().info('Deactivating...')
        if self._timer is not None:
            self.destroy_timer(self._timer)
            self._timer = None
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state):
        self.get_logger().info('Cleaning up...')
        if self._publisher is not None:
            self.destroy_publisher(self._publisher)
            self._publisher = None
        return TransitionCallbackReturn.SUCCESS

    def _publish_scan(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'lidar_link'
        msg.angle_min = -math.pi
        msg.angle_max = math.pi
        msg.angle_increment = math.pi / 180.0  # 1 degree
        msg.range_min = 0.1
        msg.range_max = 30.0
        # Generate dummy ranges: 360 readings with some randomness
        msg.ranges = [random.uniform(0.5, 10.0) for _ in range(360)]
        self._publisher.publish(msg)


def main():
    rclpy.init()
    node = LifecycleLidarDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import LaserScan


class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector')
        # Compatible QoS: RELIABLE matches RELIABLE (equal),
        # TRANSIENT_LOCAL matches TRANSIENT_LOCAL (equal).
        # Could also use BEST_EFFORT / VOLATILE (less strict) and still work.
        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self._scan_callback, qos
        )

    def _scan_callback(self, msg: LaserScan):
        valid_ranges = [r for r in msg.ranges if msg.range_min <= r <= msg.range_max]
        if valid_ranges:
            min_range = min(valid_ranges)
            self.get_logger().info(f'Min range: {min_range:.3f} m')
        else:
            self.get_logger().warn('No valid ranges in scan')


def main():
    rclpy.init()
    node = ObstacleDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Key details to look for:

- Uses `create_lifecycle_publisher` (not `create_publisher`) so the publisher respects lifecycle state.
- Timer is created in `on_activate` and destroyed in `on_deactivate`, not in `on_configure`.
- Subscriber filters invalid ranges before computing min.
- QoS profiles are explicitly compatible.

---

## Question 2: tf2 Transform Chain and Frame Math

### Problem

You have an AMR with a robot arm. The tf2 tree looks like:

```
map -> odom -> base_link -> arm_base -> link1 -> link2 -> ee_link
                         -> lidar_link
                         -> camera_link
```

**Part A (Theory, ~10 min)**

Explain how the tf2 library works under the hood in ROS 2. What topics does it use? What is the difference between `/tf` and `/tf_static`? Why is there a buffer, and what happens when you request a transform that is in the future or too far in the past? What is the difference between `lookupTransform` and the timeout parameter in ROS 2's tf2 API?

**Part B (Theory, ~5 min)**

Your camera detects an object at position `[0.5, 0.1, 1.2]` in `camera_link` frame. You need that in `map` frame. Conceptually, what is tf2 doing to get you there? What if the camera data is timestamped 200ms ago but the latest tf data for `odom -> base_link` is only 50ms old?

**Part C (Code, ~30 min)**

Write a ROS 2 Python node that:

1. Publishes a static transform from `base_link` to `camera_link` (translation `[0.1, 0.0, 0.3]`, no rotation) using a `StaticTransformBroadcaster`
2. Subscribes to a `geometry_msgs/PointStamped` topic called `/object_in_camera`
3. In the callback, uses a `tf2_ros.Buffer` and `TransformListener` to transform the point from `camera_link` to `map` frame
4. Handles the case where the transform is not yet available (catch the right exceptions)
5. Publishes the transformed point on `/object_in_map`

---

### A+ Response Benchmark

#### Part A — tf2 Internals

- `/tf` topic carries **dynamic transforms** (e.g., odom, joint states). Published at high rate. Uses `BEST_EFFORT` reliability, `VOLATILE` durability.
- `/tf_static` carries **static transforms** (e.g., sensor mounts). Uses `RELIABLE` reliability, `TRANSIENT_LOCAL` durability so late-joining nodes receive them.
- The **buffer** stores a time-indexed history of transforms (default 10 seconds). This allows looking up where frames were at any past timestamp within the window.
- **Future request:** fails with `ExtrapolationException` (extrapolation is disabled by default for safety).
- **Too far in the past:** fails with `ExtrapolationException` (data has been evicted from the buffer).
- In ROS 2, `lookupTransform` can take an optional `timeout` parameter. With `timeout=Duration(0)`, it is non-blocking and throws immediately if unavailable. With a positive timeout, it blocks up to that duration waiting for the transform to appear. This replaces the separate `waitForTransform` + `lookupTransform` pattern from ROS 1.
- tf2 uses a **tree** structure (not a graph), so there is exactly one path between any two frames.

#### Part B — Frame Chain

tf2 traverses: `camera_link -> base_link -> odom -> map`. At each hop it applies the homogeneous transform (4x4 matrix multiplication, or equivalent quaternion rotation + translation). The result is `T_map_camera = T_map_odom * T_odom_base * T_base_camera`.

For the timestamp mismatch: tf2 needs transforms at the **requested timestamp** (200ms ago). If `odom -> base_link` only has data 50ms old, the 200ms-old timestamp is not in the buffer and the lookup fails with `ExtrapolationException`. Solutions:

1. Use `rclpy.time.Time()` (time zero) to request the **latest available** transform at any timestamp. Sacrifices temporal accuracy.
2. Use the advanced `lookupTransform(target_frame, target_time, source_frame, source_time, fixed_frame)` API for time travel through a fixed frame.
3. Increase the tf buffer size or the publishing rate of the relevant broadcaster.

#### Part C — Code

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import PointStamped, TransformStamped
import tf2_geometry_msgs  # Required to register PointStamped with tf2


class CameraToMapTransformer(Node):
    def __init__(self):
        super().__init__('camera_to_map_transformer')

        # --- Static transform broadcaster: base_link -> camera_link ---
        self._static_broadcaster = StaticTransformBroadcaster(self)
        static_tf = TransformStamped()
        static_tf.header.stamp = self.get_clock().now().to_msg()
        static_tf.header.frame_id = 'base_link'
        static_tf.child_frame_id = 'camera_link'
        static_tf.transform.translation.x = 0.1
        static_tf.transform.translation.y = 0.0
        static_tf.transform.translation.z = 0.3
        static_tf.transform.rotation.x = 0.0
        static_tf.transform.rotation.y = 0.0
        static_tf.transform.rotation.z = 0.0
        static_tf.transform.rotation.w = 1.0  # Identity quaternion
        self._static_broadcaster.sendTransform(static_tf)

        # --- tf2 buffer and listener ---
        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

        # --- Subscriber and publisher ---
        self._sub = self.create_subscription(
            PointStamped, '/object_in_camera', self._point_callback, 10
        )
        self._pub = self.create_publisher(PointStamped, '/object_in_map', 10)

    def _point_callback(self, msg: PointStamped):
        try:
            # Use Time() (zero) to get the latest available transform
            # Alternatively, use msg.header.stamp for temporally accurate lookup
            transformed = self._tf_buffer.transform(
                msg, 'map', timeout=rclpy.duration.Duration(seconds=0.1)
            )
            self._pub.publish(transformed)
            self.get_logger().info(
                f'Transformed to map: [{transformed.point.x:.3f}, '
                f'{transformed.point.y:.3f}, {transformed.point.z:.3f}]'
            )
        except TransformException as ex:
            self.get_logger().warn(f'Could not transform point: {ex}')


def main():
    rclpy.init()
    node = CameraToMapTransformer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Key details to look for:

- `import tf2_geometry_msgs` is critical. Without it, the buffer does not know how to transform `PointStamped` and throws a `TypeException`. Many candidates miss this.
- Uses `buffer.transform()` (the high-level API) rather than manually calling `lookupTransform` + doing the math. Both are acceptable, but `transform()` is cleaner.
- Catches `TransformException` (base class covers `LookupException`, `ConnectivityException`, `ExtrapolationException`).
- Static broadcaster sends once; the `TRANSIENT_LOCAL` durability ensures late joiners receive it.
- Quaternion is explicitly set to identity `(0, 0, 0, 1)` for no rotation.

---

## Question 3: Implementing A* as a Nav2-Style Planner

### Problem

**Part A (Theory, ~15 min)**

Explain the Nav2 architecture at a high level. What is the behavior tree, and how does it coordinate the planner, controller, and recovery servers? What is the difference between a global planner and a local controller in this stack? When a robot gets a goal pose, walk through the sequence of events in Nav2 from goal receipt to the robot moving.

**Part B (Code, ~30 min)**

Implement A* search in Python. The function signature is:

```python
def a_star(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """
    grid:  2D occupancy grid, 0 = free, 1 = occupied
    start: (row, col)
    goal:  (row, col)
    Returns: path as list of (row, col) from start to goal inclusive,
             or empty list if no path exists.
    Use 8-connected neighbors and Euclidean heuristic.
    """
```

After writing it, answer:

- Is your heuristic admissible? Is it consistent?
- What would happen if you used Manhattan distance as the heuristic for 8-connected movement? Would A* still return the optimal path?

---

### A+ Response Benchmark

#### Part A — Nav2 Architecture

- **Behavior Tree (BT):** A tree of condition and action nodes that orchestrates the navigation pipeline. The BT navigator ticks at a fixed rate. Action nodes call the planner, controller, and recovery servers via ROS 2 actions. Condition nodes check things like "is the path still valid?" or "is the goal reached?"
- **Planner Server (Global):** Receives a start and goal pose, queries the **global costmap**, runs a planner plugin (e.g., NavFn, Smac, Theta*), returns a `nav_msgs/Path`.
- **Controller Server (Local):** Takes the global path and the **local costmap**, runs a controller plugin (e.g., DWB, MPPI, Regulated Pure Pursuit) at a high rate (e.g., 20 Hz) to compute `geometry_msgs/Twist` velocity commands.
- **Recovery Server:** Handles failures with recovery behaviors (spin, backup, wait, clear costmap).

Sequence on goal receipt:

1. NavigateToPose action received by the BT navigator.
2. BT ticks: calls `ComputePathToPose` action on the planner server.
3. Planner server invokes the loaded planner plugin against the global costmap, returns a `Path`.
4. BT passes the path to `FollowPath` action on the controller server.
5. Controller server runs the controller plugin at its control rate, publishes `cmd_vel`.
6. If the controller fails (e.g., stuck), BT condition detects failure, triggers recovery sub-tree.
7. Recovery executes (e.g., spin in place, clear costmap), then BT retries planning.

Bonus: the plugin interface pattern (C++ `pluginlib`) allows swapping planner/controller implementations without modifying Nav2 core.

#### Part B — Code

```python
import heapq
import math


def a_star(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    rows = len(grid)
    cols = len(grid[0])

    # Edge cases
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return []
    if start == goal:
        return [start]

    def heuristic(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    # 8-connected neighbors: (drow, dcol, cost)
    directions = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            cost = math.sqrt(2) if (dr != 0 and dc != 0) else 1.0
            directions.append((dr, dc, cost))

    # Priority queue: (f_score, counter, node)
    counter = 0
    open_set = [(heuristic(start, goal), counter, start)]
    came_from = {}
    g_score = {start: 0.0}
    closed = set()

    while open_set:
        f, _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            node = goal
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path.reverse()
            return path

        if current in closed:
            continue
        closed.add(current)

        for dr, dc, move_cost in directions:
            nr, nc = current[0] + dr, current[1] + dc

            # Bounds check
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            # Obstacle check
            if grid[nr][nc] == 1:
                continue

            neighbor = (nr, nc)
            if neighbor in closed:
                continue

            tentative_g = g_score[current] + move_cost

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))

    return []  # No path found
```

#### Heuristic Discussion

- **Euclidean is admissible** for 8-connected grids: the straight-line distance never overestimates because the cheapest possible path (a pure diagonal) costs exactly `sqrt(2)` per diagonal step, which equals the Euclidean distance for that step.
- **Euclidean is consistent** (monotone): for any node `n` and neighbor `n'`, `h(n) <= cost(n, n') + h(n')`. This follows from the triangle inequality.
- **Manhattan distance for 8-connected grids is inadmissible:** a diagonal move costs `sqrt(2) ~ 1.414`, but Manhattan distance charges `2` for the same displacement. This overestimates, so A* is **not** guaranteed to find the optimal path.
- **Bonus:** The correct admissible heuristic for 8-connected grids is the **Octile distance**: `max(|dx|, |dy|) + (sqrt(2) - 1) * min(|dx|, |dy|)`. This exactly models the cost of moving diagonally as much as possible, then straight.

Key details to look for:

- Diagonal moves cost `sqrt(2)`, not `1`. Candidates who use cost `1` for all moves are implementing BFS-like A* and will not find optimal paths.
- The `counter` tiebreaker in the heap prevents comparison errors when `f` scores are equal and tuples of `(f, node)` cannot be compared.
- `closed` set prevents reprocessing. Without it, the algorithm is correct but slower.
- Path reconstruction via `came_from` dict, walking backwards from goal to start.

---

## Question 4: EKF Sensor Fusion (Theory + Implementation)

### Problem

You have an AMR with wheel odometry (provides `dx, dy, dtheta` in the body frame) and a GPS sensor (provides absolute `x, y`). You want to fuse them for localization.

**Part A (Theory, ~15 min)**

Explain the Extended Kalman Filter at a conceptual level:

- What are the predict and update steps?
- Why "extended" vs. regular Kalman?
- What state vector would you choose for this problem?
- What is the process model? The observation model for GPS?
- What role does the Jacobian play, and where does linearization happen?
- What are the failure modes of an EKF?

**Part B (Code, ~30 min)**

Implement a 2D EKF in Python using only NumPy. State vector is `[x, y, theta]`.

```python
class EKF2D:
    def __init__(self, initial_state, initial_covariance, process_noise, gps_noise):
        """
        initial_state: np.array shape (3,)  -- [x, y, theta]
        initial_covariance: np.array shape (3,3)
        process_noise: np.array shape (3,3)  -- Q
        gps_noise: np.array shape (2,2)  -- R
        """
        pass

    def predict(self, dx, dy, dtheta):
        """
        Odometry-based prediction.
        dx, dy are in the robot's body frame.
        """
        pass

    def update_gps(self, gps_x, gps_y):
        """
        GPS measurement update.
        """
        pass
```

Implement both methods. Show the Jacobians explicitly.

---

### A+ Response Benchmark

#### Part A — EKF Theory

- **Predict step:** Propagate state forward using the motion model. Grow the covariance: `P = F * P * F^T + Q`. This reflects increased uncertainty from movement.
- **Update step:** Incorporate a measurement to shrink uncertainty. Compute the Kalman gain `K`, update state `x = x + K * (z - h(x))`, update covariance `P = (I - K * H) * P`.
- **"Extended"** because the motion model is **nonlinear** (rotation introduces `sin`/`cos`). The standard Kalman filter assumes linear models. EKF linearizes via first-order Taylor expansion (Jacobians).
- **State vector:** `[x, y, theta]` (2D pose).
- **Process model:**
  ```
  x' = x + dx * cos(theta) - dy * sin(theta)
  y' = y + dx * sin(theta) + dy * cos(theta)
  theta' = theta + dtheta
  ```
- **GPS observation model:** `h(x) = [x, y]`, which is linear. `H = [[1, 0, 0], [0, 1, 0]]`.
- **Jacobian F** is the partial derivative of the process model w.r.t. the state vector. It captures how small changes in the current state affect the predicted state. Linearization happens at the current state estimate (operating point).
- **Failure modes:**
  - Heavy nonlinearity where linearization is a poor approximation
  - Incorrect noise parameters (Q, R) causing overconfidence or sluggish updates
  - Non-Gaussian noise (EKF assumes Gaussian)
  - Unobservable states (e.g., theta with GPS-only updates in a straight line)
  - Divergence from accumulated linearization errors
- **Alternatives:** UKF (unscented transform, no explicit Jacobians), particle filters (handle arbitrary distributions, higher compute cost).

#### Part B — Code

```python
import numpy as np


class EKF2D:
    def __init__(self, initial_state, initial_covariance, process_noise, gps_noise):
        """
        initial_state:      np.array (3,)   [x, y, theta]
        initial_covariance: np.array (3,3)  P0
        process_noise:      np.array (3,3)  Q
        gps_noise:          np.array (2,2)  R
        """
        self.x = initial_state.copy().astype(float)       # (3,)
        self.P = initial_covariance.copy().astype(float)   # (3,3)
        self.Q = process_noise.copy().astype(float)        # (3,3)
        self.R = gps_noise.copy().astype(float)            # (2,2)

    @staticmethod
    def _normalize_angle(angle):
        """Wrap angle to [-pi, pi]."""
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def predict(self, dx, dy, dtheta):
        """
        Odometry-based prediction step.
        dx, dy: displacement in robot body frame.
        dtheta: rotation increment.
        """
        theta = self.x[2]
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)

        # --- Process model ---
        # Transform body-frame deltas to world frame
        self.x[0] += dx * cos_t - dy * sin_t
        self.x[1] += dx * sin_t + dy * cos_t
        self.x[2] += dtheta
        self.x[2] = self._normalize_angle(self.x[2])

        # --- Jacobian of the process model w.r.t. state ---
        # F = d f(x) / d x
        #
        # df0/dtheta = -dx * sin(theta) - dy * cos(theta)
        # df1/dtheta =  dx * cos(theta) - dy * sin(theta)
        F = np.array([
            [1.0, 0.0, -dx * sin_t - dy * cos_t],
            [0.0, 1.0,  dx * cos_t - dy * sin_t],
            [0.0, 0.0,  1.0],
        ])

        # --- Covariance prediction ---
        self.P = F @ self.P @ F.T + self.Q

    def update_gps(self, gps_x, gps_y):
        """
        GPS measurement update.
        Measurement z = [gps_x, gps_y] observes the state [x, y] directly.
        """
        # --- Observation model ---
        # h(x) = [x, y], which is linear
        H = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ])

        # --- Innovation (measurement residual) ---
        z = np.array([gps_x, gps_y])
        z_pred = H @ self.x  # predicted measurement
        y = z - z_pred       # innovation

        # --- Innovation covariance ---
        S = H @ self.P @ H.T + self.R

        # --- Kalman gain ---
        K = self.P @ H.T @ np.linalg.inv(S)

        # --- State update ---
        self.x = self.x + K @ y
        self.x[2] = self._normalize_angle(self.x[2])

        # --- Covariance update (Joseph form for numerical stability) ---
        I = np.eye(3)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ self.R @ K.T


# --- Example usage ---
if __name__ == '__main__':
    x0 = np.array([0.0, 0.0, 0.0])
    P0 = np.eye(3) * 1.0
    Q = np.diag([0.01, 0.01, 0.001])
    R = np.diag([0.5, 0.5])

    ekf = EKF2D(x0, P0, Q, R)

    # Simulate driving forward 1m, then getting a GPS reading
    ekf.predict(dx=1.0, dy=0.0, dtheta=0.05)
    print(f'After predict: x={ekf.x}, diag(P)={np.diag(ekf.P)}')

    ekf.update_gps(gps_x=1.05, gps_y=0.02)
    print(f'After GPS update: x={ekf.x}, diag(P)={np.diag(ekf.P)}')
```

Key details to look for:

- **Jacobian F** has the correct partial derivatives in the third column (`-dx*sin - dy*cos` and `dx*cos - dy*sin`). This is the most common error.
- **Angle normalization** after both predict and update. Without this, theta drifts outside `[-pi, pi]` and the Jacobian linearization becomes increasingly inaccurate.
- **Covariance update:** the Joseph form `(I - KH) P (I - KH)^T + K R K^T` is preferred for numerical stability over the simpler `(I - KH) P`, which can lose positive-definiteness due to floating point errors. Either is acceptable, but Joseph form is a strong signal.
- H is `(2, 3)`, K is `(3, 2)`, dimensions are all consistent.
- Copies inputs in `__init__` to avoid aliasing bugs.

---

## Question 5: ROS 2 Action Server for Trajectory Execution

### Problem

**Part A (Theory, ~10 min)**

Explain the ROS 2 action protocol:

- How does it differ from services and topics?
- What are the three components of an action (goal, feedback, result)?
- Under the hood, what topics and services does an action actually create?
- Why would you use an action instead of a service for trajectory execution?
- What happens if the client sends a cancel request mid-execution?

**Part B (Code, ~35 min)**

Define a custom action file, then write a ROS 2 Python action server and client.

**Action definition (`FollowWaypoints.action`):**

```
# Goal
geometry_msgs/PoseStamped[] waypoints
---
# Result
int32 waypoints_completed
---
# Feedback
int32 current_index
int32 remaining
```

The **server** should:

1. Accept a goal containing a list of `PoseStamped` waypoints
2. Validate the goal in a `goal_callback` (reject if the waypoint list is empty)
3. In the execute callback, iterate through waypoints, simulating movement by sleeping 1 second per waypoint
4. Publish feedback after each waypoint (current index, number remaining)
5. Check for cancellation between each waypoint and handle it gracefully (return a partial result)
6. Return a result with the number of waypoints completed

The **client** should:

1. Send a goal with 5 dummy waypoints
2. Print feedback as it arrives
3. Handle the final result

---

### A+ Response Benchmark

#### Part A — Action Protocol

- **Topics:** fire-and-forget, many-to-many, no acknowledgment. Good for streaming sensor data.
- **Services:** synchronous request-reply, blocks until response. Good for quick queries (get parameter, trigger snapshot).
- **Actions:** for **long-running tasks** that need **feedback** during execution and **cancellation** support. Essential for trajectory execution where you need progress updates and the ability to preempt.
- **Three components:**
  - **Goal:** what the client wants (list of waypoints)
  - **Feedback:** streamed progress during execution (current waypoint index)
  - **Result:** final outcome on completion or cancellation (waypoints completed)
- **Under the hood**, an action creates:
  - `_action/send_goal` (service)
  - `_action/cancel_goal` (service)
  - `_action/get_result` (service)
  - `_action/feedback` (topic)
  - `_action/status` (topic)
- **Cancel flow:** client calls `cancel_goal` service. Server's `cancel_callback` fires and returns `ACCEPT` or `REJECT`. If accepted, the execute callback checks `goal_handle.is_cancel_requested`, calls `goal_handle.canceled()`, and returns a partial result.
- **Bonus:** goal policy. If a new goal arrives while one is executing, the server must decide: accept and abort the current one, queue it, or reject. This is handled in `handle_accepted_callback` or by setting the goal policy.

#### Part B — Code

**Action Server:**

```python
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import PoseStamped

# Assuming the action is defined in a package called "custom_actions"
# from custom_actions.action import FollowWaypoints
# For this example, we use nav2_msgs which has a similar interface:
from nav2_msgs.action import FollowWaypoints


class WaypointServer(Node):
    def __init__(self):
        super().__init__('waypoint_server')
        self._action_server = ActionServer(
            self,
            FollowWaypoints,
            'follow_waypoints',
            execute_callback=self._execute_callback,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback,
            callback_group=ReentrantCallbackGroup(),
        )
        self.get_logger().info('Waypoint action server ready')

    def _goal_callback(self, goal_request):
        """Validate the goal before accepting."""
        if not goal_request.poses:
            self.get_logger().warn('Rejected: empty waypoint list')
            return GoalResponse.REJECT
        self.get_logger().info(
            f'Accepted goal with {len(goal_request.poses)} waypoints'
        )
        return GoalResponse.ACCEPT

    def _cancel_callback(self, goal_handle):
        """Accept all cancel requests."""
        self.get_logger().info('Cancel requested')
        return CancelResponse.ACCEPT

    async def _execute_callback(self, goal_handle):
        """Iterate through waypoints, publishing feedback and checking cancel."""
        self.get_logger().info('Executing waypoint following...')
        waypoints = goal_handle.request.poses
        feedback = FollowWaypoints.Feedback()
        completed = 0

        for i, waypoint in enumerate(waypoints):
            # --- Check for cancellation ---
            if goal_handle.is_cancel_requested:
                self.get_logger().info(
                    f'Cancelled at waypoint {i}/{len(waypoints)}'
                )
                goal_handle.canceled()
                result = FollowWaypoints.Result()
                result.missed_waypoints = list(range(i, len(waypoints)))
                return result

            # --- Simulate movement to waypoint ---
            self.get_logger().info(
                f'Moving to waypoint {i}: '
                f'({waypoint.pose.position.x:.2f}, '
                f'{waypoint.pose.position.y:.2f})'
            )
            time.sleep(1.0)  # Simulate travel time
            completed += 1

            # --- Publish feedback ---
            feedback.current_waypoint = i
            goal_handle.publish_feedback(feedback)

        # --- All waypoints reached ---
        goal_handle.succeed()
        result = FollowWaypoints.Result()
        result.missed_waypoints = []
        self.get_logger().info(f'All {completed} waypoints completed')
        return result


def main():
    rclpy.init()
    node = WaypointServer()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

**Action Client:**

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import FollowWaypoints


class WaypointClient(Node):
    def __init__(self):
        super().__init__('waypoint_client')
        self._client = ActionClient(self, FollowWaypoints, 'follow_waypoints')

    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._client.wait_for_server()

        # Build 5 dummy waypoints
        goal = FollowWaypoints.Goal()
        for i in range(5):
            wp = PoseStamped()
            wp.header.frame_id = 'map'
            wp.pose.position.x = float(i)
            wp.pose.position.y = float(i * 0.5)
            wp.pose.orientation.w = 1.0
            goal.poses.append(wp)

        self.get_logger().info(f'Sending {len(goal.poses)} waypoints')
        future = self._client.send_goal_async(
            goal, feedback_callback=self._feedback_callback
        )
        future.add_done_callback(self._goal_response_callback)

    def _feedback_callback(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(f'Feedback: at waypoint {fb.current_waypoint}')

    def _goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal was rejected')
            return
        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._result_callback)

    def _result_callback(self, future):
        result = future.result().result
        missed = result.missed_waypoints
        if not missed:
            self.get_logger().info('All waypoints completed successfully!')
        else:
            self.get_logger().info(f'Missed waypoints: {missed}')
        rclpy.shutdown()


def main():
    rclpy.init()
    client = WaypointClient()
    client.send_goal()
    rclpy.spin(client)


if __name__ == '__main__':
    main()
```

Key details to look for:

- **`ReentrantCallbackGroup`** on the action server. Without it (or a `MultiThreadedExecutor`), the cancel callback cannot fire while the execute callback is running, making cancellation impossible. This is the single most common bug in action server implementations.
- **`MultiThreadedExecutor`** on the server side to allow concurrent callback execution.
- Goal validation in `goal_callback` returns `GoalResponse.REJECT` for empty waypoints.
- Cancel check happens **between** waypoints (inside the loop, before the sleep), not after. If the check is after the sleep, you waste a full cycle before responding to cancellation.
- Client uses the **async pattern**: `send_goal_async` returns a future, `add_done_callback` chains to `get_result_async`. No blocking calls in the callback chain.
- Feedback callback is registered as a parameter to `send_goal_async`, not separately.
- Note: The code uses `nav2_msgs/action/FollowWaypoints` which has a slightly different Result type (`missed_waypoints` instead of `waypoints_completed`). A candidate using the custom action definition from the problem would have `result.waypoints_completed = completed` instead. Either approach is fine; the important thing is the structural correctness.