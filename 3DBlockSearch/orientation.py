
class Orientation:
    """
    A class representing a piece's orientation.
    It wraps a special 6-tuple ('orientuple') representing the orientation of the piece:
    (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
    """

    X = 'x'
    Y = 'y'
    Z = 'z'

    INITIAL_ORIENTUPLE = (1, 2, 3, 4, 5, 6)

    ROTATION_X = {1: 3,  # TOP
                  2: 2,  # RIGHT
                  3: 4,  # FRONT
                  4: 6,  # DOWN
                  5: 5,  # LEFT
                  6: 1}  # BACK

    ROTATION_Y = {1: 2,  # TOP
                  2: 4,  # RIGHT
                  3: 3,  # FRONT
                  4: 5,  # DOWN
                  5: 1,  # LEFT
                  6: 6}  # BACK

    ROTATION_Z = {1: 1,  # TOP
                  2: 3,  # RIGHT
                  3: 2,  # FRONT
                  4: 4,  # DOWN
                  5: 6,  # LEFT
                  6: 5}  # BACK

    ROTATION = {X : ROTATION_X,
                Y : ROTATION_Y,
                Z : ROTATION_Z}

    def __init__(self, orientuple=None, rotation=None):
        """
        Convert the given input to an Orientation object.
        If orientuple is given - it is wrapped by an Orientation object, and rotation is IGNORED.
        If only rotation is given - create Orientation by rotating the initial orientation accordingly (note that order
        of rotations is x, then y, then z, and that order matters)
        If none is given - Use the initial orientation
        :param orientuple:  Optional - Initial orientuple (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
        :param rotation:    Optional - Rotation tuple (x_deg, y_deg, z_deg)
        """

        if orientuple:
            self.orientuple = orientuple

        else:
            orientuple = Orientation.INITIAL_ORIENTUPLE
            self.orientuple = orientuple

            # Apply rotation to orientuple
            if rotation:

                # Validate rotation format
                assert len(rotation) == 3, "invalid rotation format"

                x_deg, y_deg, z_deg = rotation
                assert x_deg % 90 == 0, "x rotation must be integer number of 90 degrees"
                assert y_deg % 90 == 0, "y rotation must be integer number of 90 degrees"
                assert z_deg % 90 == 0, "z rotation must be integer number of 90 degrees"

                # Rotate X
                for x_rotation in range(x_deg/90):
                    self.rotate_90deg(Orientation.X)
                # Rotate Y
                for y_rotation in range(y_deg / 90):
                    self.rotate_90deg(Orientation.Y)
                # Rotate Z
                for z_rotation in range(z_deg / 90):
                    self.rotate_90deg(Orientation.Z)

    @staticmethod
    def get_rotated_90deg(orientuple, axis):
        """
        Return a copy of the given orientuple, rotated 90 degrees along the given axis.
        :param orientuple:  (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
        :param axis:        Rotation axis from {X, Y, Z}
        :return:            Copy of input orientuple, rotated 90 degrees along given axis.
        """
        # Validate arguments
        assert axis in {Orientation.X, Orientation.Y, Orientation.Z}

        # Build rotated orientation
        rotation_dict = Orientation.ROTATION[axis]
        rotated = []
        for face_num in range(6):
            # Map each face to its rotated face according to dict
            rotated_face = orientuple[rotation_dict[face_num+1] - 1]  # -1 because faces are numbered 1-6, but indexed 0-5
            rotated.append(rotated_face)

        return tuple(rotated)

    def rotate_90deg(self, axis):
        self.orientuple = Orientation.get_rotated_90deg(self.orientuple, axis)

    def __str__(self):
        return "TOP   : {}\n" \
               "RIGHT : {}\n" \
               "FRONT : {}\n" \
               "DOWN  : {}\n" \
               "LEFT  : {}\n" \
               "BACK  : {}\n".format(*self.orientuple)

    def __eq__(self, other):
        return self.orientuple == other.orientuple

def main():
    A = Orientation()
    B = Orientation()
    print ("A == B" if (A == B) else "A != B")
    print(A)
    A.rotate_90deg('x')
    print(A)
    A.rotate_90deg('x')
    A.rotate_90deg('x')
    A.rotate_90deg('x')
    print(A)
    print("A == B" if (A == B) else "A != B")
    A.rotate_90deg('y')
    print(A)
    print("A == B" if (A == B) else "A != B")


if __name__ == "__main__":
    main()