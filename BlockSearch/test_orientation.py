from unittest import TestCase
from orientation import *


class Test_Orientation(TestCase):
    def test_make_rotations_dict(self):
        from_reset = dict()
        for x_rotations in [[], [GLOBAL_X_CW], [GLOBAL_X_CW, GLOBAL_X_CW], [GLOBAL_X_CCW]]:
            for y_rotations in [[], [GLOBAL_Y_CW], [GLOBAL_Y_CW, GLOBAL_Y_CW], [GLOBAL_Y_CCW]]:
                for z_rotations in [[], [GLOBAL_Z_CW], [GLOBAL_Z_CW, GLOBAL_Z_CW], [GLOBAL_Z_CCW]]:
                    o = Orientation()
                    rotations = x_rotations + y_rotations + z_rotations
                    o.rotate_multiple_global_axis(rotations)
                    if o not in from_reset:
                        print("{} : {}\n".format(o, rotations))
                        from_reset[o] = rotations
        print(from_reset)


    def test_get_global_rotations_from_reset(self):
        o = Orientation

    def test_rotation(self):
        for x_rot in range(0,360,90):
            for y_rot in range(0, 360, 90):
                for z_rot in range(0, 360, 90):
                    world_rotation = (x_rot, y_rot, z_rot)
                    o = Orientation(rotation=world_rotation)
                    my_rotation = o.to_rotation()
                    m = Orientation(rotation=my_rotation)
                    print('world : ',world_rotation, '\nmine  : ',my_rotation,'\n')
                    self.assertEqual(o, m)

    def test_from_rotation(self):
        o = Orientation(rotation=(0, 0, 0))
        self.assertEqual(o.global_of_local_top, GLOBAL_TOP)
        self.assertEqual(o.global_of_local_front, GLOBAL_FRONT)
        self.assertEqual(o.global_of_local_right, GLOBAL_RIGHT)

        o1 = Orientation()
        o1.rotate_90deg_global_axis(GLOBAL_X_CW)
        o2 = Orientation(rotation=(90, 0, 0))
        self.assertEqual(o1, o2)

        o1.rotate_90deg_global_axis(GLOBAL_Z_CW)
        o2 = Orientation(rotation=(90, 0, 90))
        self.assertEqual(o1, o2)

        o1.rotate_90deg_global_axis(GLOBAL_Z_CCW)
        o2 = Orientation(rotation=(90, 360, 720))
        self.assertEqual(o1, o2)

        o1 = Orientation()
        o1.rotate_multiple_global_axis([GLOBAL_X_CW, GLOBAL_Y_CW, GLOBAL_Z_CW])
        o2 = Orientation(rotation=(90,90,90))
        o3 = Orientation()
        o3.rotate_90deg_global_axis(GLOBAL_X_CW)
        o3.rotate_90deg_global_axis(GLOBAL_Y_CW)
        o3.rotate_90deg_global_axis(GLOBAL_Z_CW)
        print(o1)
        self.assertEqual(o1, o2)
        self.assertEqual(o3, o2)

    def test_equal(self):
        o1 = Orientation()
        o2 = Orientation()
        self.assertEqual(o1, o2)

        o1.rotate_90deg_global_axis(GLOBAL_X_CW)
        o2.rotate_90deg_global_axis(GLOBAL_X_CCW)
        o2.rotate_90deg_global_axis(GLOBAL_X_CCW)
        o2.rotate_90deg_global_axis(GLOBAL_X_CCW)
        self.assertEqual(o1, o2)

        o3 = Orientation(rotation=(180, 180, 0))
        o4 = Orientation(rotation=(0, 0, 180))
        self.assertEqual(o3, o4)

    def test_rotate_90deg_global_axis(self):
        o = Orientation()
        self.assertEqual(o.local_at_global_front, LOCAL_FRONT)
        o.rotate_90deg_global_axis(GLOBAL_X_CW)
        self.assertEqual(o.local_at_global_front, LOCAL_DOWN)
        o.rotate_90deg_global_axis(GLOBAL_Z_CW)
        self.assertEqual(o.local_at_global_front, LOCAL_RIGHT)
        o.rotate_90deg_global_axis(GLOBAL_Y_CW)
        self.assertEqual(o.local_at_global_front, LOCAL_RIGHT)

    def test_rotate_90deg_global_axis_ccw(self):
        o = Orientation()
        self.assertEqual(o.local_at_global_front, LOCAL_FRONT)
        o.rotate_90deg_global_axis(GLOBAL_X_CCW)
        self.assertEqual(o.local_at_global_front, LOCAL_TOP)
        o.rotate_90deg_global_axis(GLOBAL_Z_CCW)
        self.assertEqual(o.local_at_global_front, LOCAL_LEFT)

    def test_rotation_conversions(self):
        o = Orientation()
        r = o.to_rotation()
        self.assertEqual(r, (0, 0, 0))
        o.rotate_90deg_global_axis(GLOBAL_X_CW)
        r = o.to_rotation()
        self.assertEqual(r, (90, 0, 0))
        o.rotate_90deg_global_axis(GLOBAL_Z_CW)
        r = o.to_rotation()
        self.assertEqual(r, (90, 0, 90))

    def test_local_to_global_90_deg_x(self):
        o = Orientation()
        #print(o)
        o.rotate_90deg_global_axis(GLOBAL_X_CW)
        #print(o)
        self.assertEqual(o.global_of_local_front, GLOBAL_TOP)
        self.assertEqual(o.global_of_local_right, GLOBAL_RIGHT)
        self.assertEqual(o.global_of_local_down, GLOBAL_FRONT)
        self.assertEqual(o.global_of_local_back, GLOBAL_DOWN)
        self.assertEqual(o.global_of_local_left, GLOBAL_LEFT)
        self.assertEqual(o.global_of_local_top, GLOBAL_BACK)

    def test_local_to_global_90_deg_z(self):
        o = Orientation()
        #print(o)
        o.rotate_90deg_global_axis(GLOBAL_Z_CW)
        #print(o)
        self.assertEqual(o.global_of_local_top, GLOBAL_TOP)
        self.assertEqual(o.global_of_local_right, GLOBAL_FRONT)
        self.assertEqual(o.global_of_local_front, GLOBAL_LEFT)
        self.assertEqual(o.global_of_local_down, GLOBAL_DOWN)
        self.assertEqual(o.global_of_local_left, GLOBAL_BACK)
        self.assertEqual(o.global_of_local_back, GLOBAL_RIGHT)

    def test_local_to_global_90_deg_xz(self):
        o = Orientation()
        #print("initial")
        #print(o)
        o.rotate_90deg_global_axis(GLOBAL_X_CW)
        #print("90 deg x")
        #print(o)
        o.rotate_90deg_global_axis(GLOBAL_Z_CW)
        #print("90 deg z")
        #print(o)
        self.assertEqual(o.global_of_local_front, GLOBAL_TOP)
        self.assertEqual(o.global_of_local_right, GLOBAL_FRONT)
        self.assertEqual(o.global_of_local_down, GLOBAL_LEFT)
        self.assertEqual(o.global_of_local_back, GLOBAL_DOWN)
        self.assertEqual(o.global_of_local_left, GLOBAL_BACK)
        self.assertEqual(o.global_of_local_top, GLOBAL_RIGHT)

    def test_get_rotations_towards_reset(self):
        o = Orientation()
        rotations = o.get_global_rotations_towards_reset()
        #print(rotations)
        self.assertEqual(rotations, [])

        o.rotate_90deg_global_axis(GLOBAL_X_CW)
        rotations = o.get_global_rotations_towards_reset()
        #print(rotations)
        self.assertEqual(rotations, [GLOBAL_X_CCW])

        o.rotate_90deg_global_axis(GLOBAL_Y_CW)
        rotations = o.get_global_rotations_towards_reset()
        #print(rotations)
