import math
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).parents[1] / "analysis"))
from kinematics import Linkage, rocker_point


class KinematicsTests(unittest.TestCase):
    def test_default_linkage_closes_over_full_rotation(self):
        linkage = Linkage(120, 35, 110, 90)
        for degree in range(0, 361, 5):
            px, py = rocker_point(linkage, math.radians(degree))
            crank_x = linkage.crank * math.cos(math.radians(degree))
            crank_y = linkage.crank * math.sin(math.radians(degree))
            self.assertAlmostEqual(math.hypot(px - crank_x, py - crank_y), 110)
            self.assertAlmostEqual(math.hypot(px - 120, py), 90)

    def test_grashof_classification(self):
        self.assertTrue(Linkage(120, 35, 110, 90).grashof)
        self.assertFalse(Linkage(100, 80, 70, 60).grashof)

    def test_invalid_geometry_is_rejected(self):
        with self.assertRaises(ValueError):
            Linkage(0, 35, 110, 90)
        with self.assertRaises(ValueError):
            rocker_point(Linkage(200, 10, 10, 10), 0)


if __name__ == "__main__":
    unittest.main()
