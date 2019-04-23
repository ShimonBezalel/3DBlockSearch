import numpy as np

from grid import GRID_UNIT_IN_MM


class Orientation:
    """
    A class representing a piece's orientation.
    It wraps a special 6-tuple ('orientuple') representing the orientation of the piece:
    (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
    """

    # Axes
    X = 'Left-Right'
    Y = 'Front-Back'
    Z = 'Top-Down'

    # Faces
    TOP = "TOP"
    RIGHT = "RIGHT"
    FRONT = "FRONT"
    DOWN = "DOWN"
    LEFT = "LEFT"
    BACK = "BACK"

    # Global face indexes
    GLOBAL_FACE_INDEX = {
        TOP: 0,
        RIGHT: 1,
        FRONT: 2,
        DOWN: 3,
        LEFT: 4,
        BACK: 5
    }

    # Global ('constant', 'real world') orientuple
    INITIAL_ORIENTUPLE = (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)

    # Rotation dictionaries
    # Rotation clockwise across Right-Left axis
    ROTATION_X = {TOP: BACK,  # TOP
                  RIGHT: RIGHT,  # RIGHT
                  FRONT: TOP,  # FRONT
                  DOWN: FRONT,  # DOWN
                  LEFT: LEFT,  # LEFT
                  BACK: DOWN}  # BACK

    # Rotation clockwise across Front-Back axis
    ROTATION_Y = {TOP: LEFT,  # TOP
                  RIGHT: TOP,  # RIGHT
                  FRONT: FRONT,  # FRONT
                  DOWN: RIGHT,  # DOWN
                  LEFT: DOWN,  # LEFT
                  BACK: BACK}  # BACK

    # Rotation clockwise across Top-Down axis
    ROTATION_Z = {TOP: TOP,  # TOP
                  RIGHT: FRONT,  # RIGHT
                  FRONT: LEFT,  # FRONT
                  DOWN: DOWN,  # DOWN
                  LEFT: BACK,  # LEFT
                  BACK: RIGHT}  # BACK

    ROTATION = {X: ROTATION_X,
                Y: ROTATION_Y,
                Z: ROTATION_Z}

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
            if not (rotation is None):

                # Validate rotation format
                assert len(rotation) == 3, "invalid rotation format"

                x_deg, y_deg, z_deg = rotation
                assert x_deg % 90 == 0, "x rotation must be integer number of 90 degrees"
                assert y_deg % 90 == 0, "y rotation must be integer number of 90 degrees"
                assert z_deg % 90 == 0, "z rotation must be integer number of 90 degrees"

                # Rotate X
                for x_rotation in range(int(x_deg / 90)):
                    self.rotate_90deg(Orientation.X)
                # Rotate Y
                for y_rotation in range(int(y_deg / 90)):
                    self.rotate_90deg(Orientation.Y)
                # Rotate Z
                for z_rotation in range(int(z_deg / 90)):
                    self.rotate_90deg(Orientation.Z)

    def local_to_global(self, local_face):
        """
        Reverse search of given face with respect to the global (initial) orientation.
        :param local_facing: the local face which had rotated with this hub, and we want to tell its current global facing
        :return: the face with respect to global of the given face with respect to local
        Example:
            Initial cube was rotated cw once around FB axis --> The original TOP is now in the global RIGHT.
            cube.local_to_global(TOP) == RIGHT
        """
        return Orientation.INITIAL_ORIENTUPLE[self.__orientuple.index(local_face)]

    @staticmethod
    def get_rotated_90deg(orientuple, axis):
        """
        Return a copy of the given orientuple, rotated 90 degrees along the given axis.
        :param orientuple:  (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
        :param axis:        Rotation axis from {X, Y, Z}
        :return:            Copy of input orientuple, rotated 90 degrees along given global axis.
        """
        # Validate arguments
        assert axis in {Orientation.X, Orientation.Y, Orientation.Z}

        # Build rotated orientation
        rotation_dict = Orientation.ROTATION[axis]
        rotated_orientuple = np.array(Orientation.INITIAL_ORIENTUPLE)

        # Move local faces according to global rotation
        for i, global_face in enumerate(Orientation.INITIAL_ORIENTUPLE):
            local_face = orientuple[i]
            global_face_rotated = rotation_dict[global_face]
            i_rotated = Orientation.GLOBAL_FACE_INDEX[global_face_rotated]
            rotated_orientuple[i_rotated] = local_face
        return tuple(rotated_orientuple)

    def rotate_90deg(self, axis):
        """
        Rotate this orientation with 90 degrees clockwise around the given axis
        :param axis: Rotation axis from {Orientation.X, Orientation.Y, Orientation.Z}
        """
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
        return "global TOP   : local {}\n" \
               "global RIGHT : local {}\n" \
               "global FRONT : local {}\n" \
               "global DOWN  : local {}\n" \
               "global LEFT  : local {}\n" \
               "global BACK  : local {}\n".format(*self.__orientuple)

    def __eq__(self, other):
        return self.__orientuple == other.orientuple


def orient_mesh(mesh_data, rotation, translation):
    """
    Rotate and translate the given mesh according to given rotation and position.
    :param mesh_data:   Mesh to rotate and translate
    :param rotation:    Rotation in degrees per axis - (x_deg, y_deg, z_deg)
    :param translation: Translation in grid units per axis - (x_shift, y_shift, z_shift)
    """

    # Rotate mesh into correct orientation using 3 rotations, around axis x, y, and z
    for i, axis in enumerate([[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        mesh_data.rotate(axis, np.radians(rotation[i]))

    # Translate to correct position. Translations happens from center of the mesh's mass to the objects location
    for i, translation_obj in enumerate([mesh_data.x, mesh_data.y, mesh_data.z]):
        translation_obj += translation[i]


def transform_mesh(mesh_data, rotation, translation):
    matrix = np.zeros((4, 4))
    matrix[0:3, 0:3] = np.diag(np.deg2rad(rotation))
    matrix[0:3, 3] = np.array((translation))
    matrix[3, 3] = 1
    mesh_data.transform(matrix)


def test_rotate_90deg():
    A = Orientation()
    B = Orientation()
    print("A == B" if (A == B) else "A != B")
    print(A)
    A.rotate_90deg(Orientation.X)
    print(A)
    A.rotate_90deg(Orientation.X)
    A.rotate_90deg(Orientation.X)
    A.rotate_90deg(Orientation.X)
    print(A)
    print("A == B" if (A == B) else "A != B")
    A.rotate_90deg(Orientation.Y)
    print(A)
    print("A == B" if (A == B) else "A != B")


def test_local_to_global():
    A = Orientation()
    A.rotate_90deg(Orientation.X)
    print(A)


def main():
    test_local_to_global()


if __name__ == "__main__":
    main()
