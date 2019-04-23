from unittest import TestCase
from orientation import Orientation

class Test_Orientation(TestCase):
    def test_local_to_global_90_deg_x(self):
        o = Orientation()
        print(o)
        o.rotate_90deg(Orientation.X)
        print(o)
        self.assertEqual(o.local_to_global(Orientation.FRONT), Orientation.TOP)
        self.assertEqual(o.local_to_global(Orientation.RIGHT), Orientation.RIGHT)
        self.assertEqual(o.local_to_global(Orientation.DOWN), Orientation.FRONT)
        self.assertEqual(o.local_to_global(Orientation.BACK), Orientation.DOWN)
        self.assertEqual(o.local_to_global(Orientation.LEFT), Orientation.LEFT)
        self.assertEqual(o.local_to_global(Orientation.TOP), Orientation.BACK)

    def test_local_to_global_90_deg_z(self):
        o = Orientation()
        print(o)
        o.rotate_90deg(Orientation.Z)
        print(o)
        self.assertEqual(o.local_to_global(Orientation.TOP), Orientation.TOP)
        self.assertEqual(o.local_to_global(Orientation.RIGHT), Orientation.FRONT)
        self.assertEqual(o.local_to_global(Orientation.FRONT), Orientation.LEFT)
        self.assertEqual(o.local_to_global(Orientation.DOWN), Orientation.DOWN)
        self.assertEqual(o.local_to_global(Orientation.LEFT), Orientation.BACK)
        self.assertEqual(o.local_to_global(Orientation.BACK), Orientation.RIGHT)

    def test_local_to_global_90_deg_xz(self):
        o = Orientation()
        print("initial")
        print(o)
        o.rotate_90deg(Orientation.X)
        print("90 deg x")
        print(o)
        o.rotate_90deg(Orientation.Z)
        print("90 deg z")
        print(o)
        self.assertEqual(o.local_to_global(Orientation.FRONT), Orientation.TOP)
        self.assertEqual(o.local_to_global(Orientation.RIGHT), Orientation.FRONT)
        self.assertEqual(o.local_to_global(Orientation.DOWN), Orientation.LEFT)
        self.assertEqual(o.local_to_global(Orientation.BACK), Orientation.DOWN)
        self.assertEqual(o.local_to_global(Orientation.LEFT), Orientation.BACK)
        self.assertEqual(o.local_to_global(Orientation.TOP), Orientation.RIGHT)