from copy import copy, deepcopy

import numpy as np
from stl import mesh

from hub import Hub
from orientation import Orientation


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
        self.end1 = Hub(htype=Hub.TYPE_END_1, parent=self)
        self.end2 = Hub(htype=Hub.TYPE_END_2, parent=self)
        self.center = Hub(htype=Hub.TYPE_CENTER, parent=self)
        orient_mesh(self.mesh, self.rotation, self.position)

    def get_mesh(self):
        """
        Return the piece's mesh
        :return: A mesh rotated and positioned in 3D space
        """
        return self.mesh

    @property
    def orientation(self):
        """
        Return the piece's orientation object (see orientation.py)
        Derived from the piece's rotation.
        :return: orientation object of the piece
        """
        return Orientation(rotation=self.rotation)

    def get_hubs(self):
        """
        Returns a tuple of hubs spawned by this piece:
        (END_1, CENTER, END_2)
        :return: tuple (END_1, CENTER, END_2) - the hubs of this piece
        """
        return (self.end1, self.center, self.end2)

    def copy(self):
        """

        :return:
        """
        # TODO: needed for state copy
        pass

    def get_spawning_move(self):
        pass

    def __str__(self):
        pass

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass


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
    matrix = np.zeros((4,4))
    matrix[0:3, 0:3] = np.diag(np.deg2rad(rotation))
    matrix[0:3,3] = np.array((translation))
    matrix[3,3] = 1
    mesh_data.transform(matrix)