import math
import unittest

from tf_tree import SE2Transform, TFTree, TransformLookupError


class TestTFTree(unittest.TestCase):
    def test_chain_lookup_and_point_transform(self) -> None:
        tree = TFTree()
        tree.set_transform("world", "base", SE2Transform(1.0, 0.0, 0.0), timestamp=1.0)
        tree.set_transform("base", "camera", SE2Transform(0.0, 2.0, math.pi / 2.0), timestamp=1.0)

        world_from_camera = tree.lookup_transform("camera", "world", timestamp=1.0)
        self.assertAlmostEqual(world_from_camera.x, 1.0, places=6)
        self.assertAlmostEqual(world_from_camera.y, 2.0, places=6)
        self.assertAlmostEqual(world_from_camera.yaw, math.pi / 2.0, places=6)

        wx, wy = tree.transform_point((1.0, 0.0), "camera", "world", timestamp=1.0)
        self.assertAlmostEqual(wx, 1.0, places=6)
        self.assertAlmostEqual(wy, 3.0, places=6)

    def test_interpolation_within_edge_history(self) -> None:
        tree = TFTree()
        tree.set_transform("world", "base", SE2Transform(0.0, 0.0, 0.0), timestamp=0.0)
        tree.set_transform("world", "base", SE2Transform(10.0, 0.0, 0.0), timestamp=10.0)

        world_from_base = tree.lookup_transform("base", "world", timestamp=5.0)
        self.assertAlmostEqual(world_from_base.x, 5.0, places=6)
        self.assertAlmostEqual(world_from_base.y, 0.0, places=6)
        self.assertAlmostEqual(world_from_base.yaw, 0.0, places=6)

    def test_lookup_raises_for_time_outside_history(self) -> None:
        tree = TFTree()
        tree.set_transform("world", "base", SE2Transform(0.0, 0.0, 0.0), timestamp=1.0)
        tree.set_transform("world", "base", SE2Transform(1.0, 0.0, 0.0), timestamp=2.0)

        with self.assertRaises(TransformLookupError):
            tree.lookup_transform("base", "world", timestamp=3.0)

    def test_lookup_raises_for_disconnected_subtrees(self) -> None:
        tree = TFTree()
        tree.set_transform("world", "base", SE2Transform(0.0, 0.0, 0.0), timestamp=1.0)
        tree.set_transform("map", "lidar", SE2Transform(0.0, 0.0, 0.0), timestamp=1.0)

        with self.assertRaises(TransformLookupError):
            tree.lookup_transform("base", "lidar", timestamp=1.0)

    def test_time_zero_uses_latest_common_time(self) -> None:
        tree = TFTree()
        # world<-base is available from t=[0, 10]
        tree.set_transform("world", "base", SE2Transform(0.0, 0.0, 0.0), timestamp=0.0)
        tree.set_transform("world", "base", SE2Transform(10.0, 0.0, 0.0), timestamp=10.0)
        # base<-camera is only available at t=8, so latest common should be t=8.
        tree.set_transform("base", "camera", SE2Transform(0.0, 1.0, 0.0), timestamp=8.0)

        world_from_camera = tree.lookup_transform("camera", "world", timestamp=0.0)
        self.assertAlmostEqual(world_from_camera.x, 8.0, places=6)
        self.assertAlmostEqual(world_from_camera.y, 1.0, places=6)

    def test_reparenting_replaces_old_parent_path(self) -> None:
        tree = TFTree()
        tree.set_transform("world", "tool", SE2Transform(1.0, 0.0, 0.0), timestamp=1.0)
        tree.set_transform("base", "tool", SE2Transform(2.0, 0.0, 0.0), timestamp=2.0)
        tree.set_transform("world", "base", SE2Transform(3.0, 0.0, 0.0), timestamp=2.0)

        world_from_tool = tree.lookup_transform("tool", "world", timestamp=2.0)
        self.assertAlmostEqual(world_from_tool.x, 5.0, places=6)
        self.assertAlmostEqual(world_from_tool.y, 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
