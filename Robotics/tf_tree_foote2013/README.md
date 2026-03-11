# tf Tree (Foote 2013) - Barebones Python Implementation

This folder contains a minimal, interview-friendly implementation of the core ideas from:

- Tully Foote, **"tf: The Transform Library"**, TePRA 2013

## What Is Implemented

- A small `TFTree` class to manage coordinate frames as a **tree**
- Time-stamped transform history per edge (`parent -> child`)
- Interpolation between transform samples for arbitrary query times
- Transform lookup between any two connected frames via common ancestor traversal
- Point transformation utility (`transform_point`)
- "Latest common time" behavior when query time is `0.0` (similar to tf convention)
- Basic dynamic re-parenting support (child can switch parent)

## Paper Concepts to Code Mapping

- **Tree, not arbitrary graph** -> `TFTree` enforces one parent per child and prevents cycles
- **Directed edge transforms** -> stores `parent_from_child` transforms per edge
- **History per edge** -> `_TimedTransformBuffer` stores sorted `(time, transform)` samples
- **Interpolation** -> `SE2Transform.interpolate(...)` used in buffer lookup
- **Query by spanning/common ancestor path** -> `lookup_transform(...)` builds ancestor maps and composes transforms
- **Error on unavailable data** -> `TransformLookupError` is raised for disconnected frames, unknown frames, and out-of-range times

## Simplifications (Intentional for Interview Barebones)

- Uses **2D rigid transforms (`SE2`)**: `(x, y, yaw)` instead of full 3D + quaternion SLERP
- No networking/broadcaster-listener layer (single-process in-memory model)
- No uncertainty modeling, covariance propagation, or advanced extrapolation

## Files

- `tf_tree.py` - implementation
- `test_tf_tree.py` - unit tests using Python `unittest`

## Run Tests

From this directory:

```bash
python -m unittest -q
```

## Why This Is a Good Staff-Level Interview Skeleton

- Demonstrates frame-graph modeling and transform composition fundamentals
- Shows robust API behavior with explicit failure modes
- Includes time-aware querying and interpolation (critical real robotics concern)
- Is small enough to extend live (3D transforms, quaternions, caching, thread safety, ROS bridge)
