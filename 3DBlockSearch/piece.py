from copy import copy, deepcopy

import numpy as np
from stl import mesh

class Orientation:
    """
    A class representing a piece's orientation.
    (TOP, RIGHT, FRONT, DOWN, LEFT, BACK)
    """

    X = 'x'
    Y = 'y'
    Z = 'z'

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
    def __init__(self, rotation):
        """
        convert the given rotation to orientation representation
        :param rotation: tuple (x_deg, y_deg, z_deg)
        """

        # Validate
        assert len(rotation) == 3, "invalid rotation format"

        x_deg, y_deg, z_deg = rotation

        assert x_deg % 90 == 0, "x rotation must be integer number of 90 degrees"
        assert y_deg % 90 == 0, "y rotation must be integer number of 90 degrees"
        assert z_deg % 90 == 0, "z rotation must be integer number of 90 degrees"

    @staticmethod
    def rotate_90deg(orientation, axis):
        """

        :param orientation:
        :param axis:
        :return:
        """
        # Validate arguments
        assert len(orientation) == 6, "invalid orientation format"
        assert axis in {Orientation.X, Orientation.Y, Orientation.Z}

        # Build rotated orientation
        rotation_dict = Orientation.ROTATION[axis]
        rotated = []
        for face in range(6):
            # Map each face to its rotated face according to dict
            rotated_face = orientation[rotation_dict[face] - 1]  # -1 because faces are numbered 1-6, but indexed 0-5
            rotated.append(rotated_face)

        return rotated

    def rotate_90deg(self, axis):
        self.
class Piece:

    def __init__(self, piece_mesh, rotation, position):
        """

        :param piece_mesh: Object defining shape of piece for rendering, will be DEEP COPIED
        :param rotation: tuple of rotations on X, Y and Z axis, in degrees
                            (90 , 180 , 0) means rotate 90 degrees in x and 180 degrees in y and 0 in z axis
        :param position: a tuple (x,y,z) of position in space.
        """
        self.rotation = rotation
        self.position = position
        self.mesh = deepcopy(piece_mesh)
        orient_mesh(self.mesh, self.rotation, self.position)

    def get_hubs(self):
        """
        Returns a list of hubs spawned by this piece
        :return:
        """
        pass

    def copy(self):
        """

        :return:
        """
        # TODO: needed for state copy
        pass

    def get_spawning_move(self):
        pass

    def __str__(self):
        """

        :return:
        """
        pass

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

    def get_mesh(self):
        """
        Return the piece's mesh
        :return: A mesh oriented and positioned in 3D space
        """
        return self.mesh


def orient_mesh(mesh_data, rotation, translation):
    """
    Rotate and translate the given mesh according to given rotation and position.
    :param mesh_data:   Mesh to rotate and translate
    :param rotation:    Rotation in degrees per axis - (x_rad, y_rad, z_rad)
    :param translation: Translation in grid units per axis - (x_shift, y_shift, z_shift)
    :return:            Oriented mesh
    """
    # Rotate mesh into correct orientation using 3 rotations, around axis x, y, and z
    for i, axis in enumerate([[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        mesh_data.rotate(axis, np.radians(rotation[i]))

    # Translate to correct position. Translations happens from center of the mesh's mass to the objects location
    for i, translation_obj in enumerate([mesh_data.x, mesh_data.y, mesh_data.z]):
        translation_obj += translation[i]
