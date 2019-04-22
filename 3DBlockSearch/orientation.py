class Orientation:
    """
    A class representing a piece's orientation.
    It wraps a special 6-tuple ('orientuple') representing the orientation of the piece:
    (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
    """

    LR = 'Left-Right'
    FB = 'Front-Back'
    TD = 'Top-Down'

    INITIAL_ORIENTUPLE = (1, 2, 3, 4, 5, 6)

    # Rotation clockwise across Right-Left axis
    ROTATION_LR = {1: 3,  # TOP
                   2: 2,  # RIGHT
                   3: 4,  # FRONT
                   4: 6,  # DOWN
                   5: 5,  # LEFT
                   6: 1}  # BACK

    # Rotation clockwise across Front-Back axis
    ROTATION_FB = {1: 2,  # TOP
                   2: 4,  # RIGHT
                   3: 3,  # FRONT
                   4: 5,  # DOWN
                   5: 1,  # LEFT
                   6: 6}  # BACK

    # Rotation clockwise across Top-Down axis
    ROTATION_TD = {1: 1,  # TOP
                   2: 3,  # RIGHT
                   3: 2,  # FRONT
                   4: 4,  # DOWN
                   5: 6,  # LEFT
                   6: 5}  # BACK

    ROTATION = {LR: ROTATION_LR,
                FB: ROTATION_FB,
                TD: ROTATION_TD}

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
            self.__orientuple = orientuple

        else:
            orientuple = Orientation.INITIAL_ORIENTUPLE
            self.__orientuple = orientuple

            # Apply rotation to orientuple
            if rotation.any():

                # Validate rotation format
                assert len(rotation) == 3, "invalid rotation format"

                x_deg, y_deg, z_deg = rotation
                assert x_deg % 90 == 0, "x rotation must be integer number of 90 degrees"
                assert y_deg % 90 == 0, "y rotation must be integer number of 90 degrees"
                assert z_deg % 90 == 0, "z rotation must be integer number of 90 degrees"

                # Rotate X
                for x_rotation in range(int(x_deg / 90)):
                    self.rotate_90deg(Orientation.LR)
                # Rotate Y
                for y_rotation in range(int(y_deg / 90)):
                    self.rotate_90deg(Orientation.FB)
                # Rotate Z
                for z_rotation in range(int(z_deg / 90)):
                    self.rotate_90deg(Orientation.TD)

    @staticmethod
    def get_rotated_90deg(orientuple, axis):
        """
        Return a copy of the given orientuple, rotated 90 degrees along the given axis.
        :param orientuple:  (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
        :param axis:        Rotation axis from {X, Y, Z}
        :return:            Copy of input orientuple, rotated 90 degrees along given axis.
        """
        # Validate arguments
        assert axis in {Orientation.LR, Orientation.FB, Orientation.TD}

        # Build rotated orientation
        rotation_dict = Orientation.ROTATION[axis]
        rotated = []
        for face_num in range(6):
            # Map each face to its rotated face according to dict
            rotated_face = orientuple[
                rotation_dict[face_num + 1] - 1]  # -1 because faces are numbered 1-6, but indexed 0-5
            rotated.append(rotated_face)

        return tuple(rotated)

    def rotate_90deg(self, axis):
        self.__orientuple = Orientation.get_rotated_90deg(self.__orientuple, axis)

    @property
    def top(self):
        return self.__orientuple[0]  # TOP index

    @property
    def right(self):
        return self.__orientuple[1]  # RIGHT index

    @property
    def front(self):
        return self.__orientuple[2]  # FRONT index

    @property
    def down(self):
        return self.__orientuple[3]  # DOWN index

    @property
    def left(self):
        return self.__orientuple[4]  # LEFT  index

    @property
    def back(self):
        return self.__orientuple[5]  # BACK index

    def __str__(self):
        return "TOP   : {}\n" \
               "RIGHT : {}\n" \
               "FRONT : {}\n" \
               "DOWN  : {}\n" \
               "LEFT  : {}\n" \
               "BACK  : {}\n".format(*self.__orientuple)

    def __eq__(self, other):
        return self.__orientuple == other.orientuple

def main():
    A = Orientation()
    B = Orientation()
    print("A == B" if (A == B) else "A != B")
    print(A)
    A.rotate_90deg(Orientation.LR)
    print(A)
    A.rotate_90deg(Orientation.LR)
    A.rotate_90deg(Orientation.LR)
    A.rotate_90deg(Orientation.LR)
    print(A)
    print("A == B" if (A == B) else "A != B")
    A.rotate_90deg(Orientation.FB)
    print(A)
    print("A == B" if (A == B) else "A != B")


if __name__ == "__main__":
    main()
