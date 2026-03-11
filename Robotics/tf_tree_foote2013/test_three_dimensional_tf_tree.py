import unittest
import numpy as np
from scipy.spatial.transform import Rotation
from three_dimensional_tf_tree import SE3Transform, TimeCache, TimeAwareTransformTree, TFException, ExtrapolationException, ConnectivityException


class TestTimeAwareTransformTree(unittest.TestCase):
    def setUp(self):
        self.tree = TimeAwareTransformTree()
        
        # Scenario: A mobile base with a camera.
        # odom publishes at 10Hz (every 0.1s)
        # camera publishes at 5Hz (every 0.2s)
        
        # Populate odom -> base_link (Moving +1m in X every 0.1s)
        for i in range(10):
            t = i * 0.1
            trans = SE3Transform(
                translation=[float(i), 0.0, 0.0],
                rotation=Rotation.identity()
            )
            self.tree.set_transform("odom", "base_link", t, trans)

        # Populate base_link -> camera (Static +0.5m in Z, published at 0.0, 0.2, 0.4, 0.6)
        for i in range(4):
            t = i * 0.2
            trans = SE3Transform(
                translation=[0.0, 0.0, 0.5],
                rotation=Rotation.from_euler('y', 90, degrees=True) # looking down
            )
            self.tree.set_transform("base_link", "camera", t, trans)

    # ==========================================
    # 1. Exact Time Lookups
    # ==========================================
    def test_exact_time_lookup(self):
        """Test looking up a transform exactly at a synchronized timestamp."""
        # At t=0.4, base_link is at X=4.0. Camera is at Z=0.5 relative to base.
        t_odom_cam = self.tree.lookup_transform("odom", "camera", time=0.4)
        np.testing.assert_almost_equal(t_odom_cam.translation, [4.0, 0.0, 0.5])

    # ==========================================
    # 2. Interpolation (Lerp & Slerp)
    # ==========================================
    def test_temporal_interpolation(self):
        """Test requesting a transform exactly between two cached timestamps."""
        # Request t=0.45. 
        # odom -> base_link has data at 0.4 (X=4) and 0.5 (X=5). Should interpolate to X=4.5.
        # base_link -> camera has data at 0.4 and 0.6. Should interpolate static offset.
        t_odom_cam = self.tree.lookup_transform("odom", "camera", time=0.45)
        np.testing.assert_almost_equal(t_odom_cam.translation, [4.5, 0.0, 0.5])

    def test_slerp_rotation_interpolation(self):
        """Verify quaternion shortest-path interpolation."""
        tree = TimeAwareTransformTree()
        # 0 deg at t=1.0
        tree.set_transform("map", "joint_1", 1.0, SE3Transform([0,0,0], Rotation.from_euler('z', 0, degrees=True)))
        # 90 deg at t=2.0
        tree.set_transform("map", "joint_1", 2.0, SE3Transform([0,0,0], Rotation.from_euler('z', 90, degrees=True)))
        
        # Request at t=1.5 (Exactly halfway)
        t_interp = tree.lookup_transform("map", "joint_1", time=1.5)
        
        expected_quat = Rotation.from_euler('z', 45, degrees=True).as_quat()
        np.testing.assert_almost_equal(t_interp.rotation.as_quat(), expected_quat)

    # ==========================================
    # 3. Extrapolation Rejection
    # ==========================================
    def test_extrapolation_past_fails(self):
        """Requesting a time before the buffer begins should raise an ExtrapolationException."""
        with self.assertRaises(ExtrapolationException):
            self.tree.lookup_transform("odom", "camera", time=-0.1)

    def test_extrapolation_future_fails(self):
        """Requesting a time after the buffer ends should raise an ExtrapolationException."""
        # Latest odom is 0.9. Latest camera is 0.6. Requesting 0.8 fails on camera link.
        with self.assertRaises(ExtrapolationException):
            self.tree.lookup_transform("odom", "camera", time=0.8)

    # ==========================================
    # 4. Time "Zero" (Latest Common Time)
    # ==========================================
    def test_latest_common_time_success(self):
        """
        time=0.0 should automatically resolve to the bottlenecked newest time.
        odom goes to 0.9. camera goes to 0.6. Latest common time should be 0.6.
        At t=0.6, base_link X=6.0.
        """
        t_odom_cam = self.tree.lookup_transform("odom", "camera", time=0.0)
        np.testing.assert_almost_equal(t_odom_cam.translation, [6.0, 0.0, 0.5])

    def test_latest_common_time_asynchronous_drop(self):
        """
        Simulate a sensor dropping offline. 
        If there is no overlapping window, time=0.0 should fail.
        """
        tree = TimeAwareTransformTree()
        
        # Sensor A publishes from t=1.0 to t=5.0
        tree.set_transform("map", "odom", 1.0, SE3Transform.identity())
        tree.set_transform("map", "odom", 5.0, SE3Transform.identity())
        
        # Sensor B drops offline! It only published from t=10.0 to t=15.0
        tree.set_transform("odom", "base_link", 10.0, SE3Transform.identity())
        tree.set_transform("odom", "base_link", 15.0, SE3Transform.identity())

        # The time windows [1.0, 5.0] and [10.0, 15.0] do not intersect.
        with self.assertRaises(ExtrapolationException):
            tree.lookup_transform("map", "base_link", time=0.0)

    # ==========================================
    # 5. Garbage Collection / Ring Buffer
    # ==========================================
    def test_buffer_pruning(self):
        """Verify that data older than max_duration is discarded."""
        tree = TimeAwareTransformTree()
        # Insert at t=1.0, 2.0, 3.0, 4.0, 5.0, 6.0 with a max_duration of 2.0 seconds
        for i in range(1, 7):
            # We override the max_duration directly for testing
            if "child" not in tree._tree:
                tree._tree["child"] = ("parent", TimeCache(max_duration=2.0))
            tree._tree["child"][1].insert(float(i), SE3Transform.identity())
            
        cache = tree._tree["child"][1]
        
        # Latest time is 6.0. Cutoff is 4.0. 
        # The cache should keep 4.0, 5.0, 6.0, PLUS 3.0 (to allow interpolation between 3.0 and 4.0)
        # Times 1.0 and 2.0 should be pruned.
        self.assertNotIn(1.0, cache.times)
        self.assertNotIn(2.0, cache.times)
        self.assertIn(3.0, cache.times)
        self.assertEqual(len(cache.times), 4)

if __name__ == '__main__':
    unittest.main()