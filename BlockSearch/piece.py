from copy import copy, deepcopy

import numpy as np
from stl import mesh

from hub import Hub
from orientation import Orientation, orient_mesh


class Piece:

    def __init__(self, rotation=np.array((0,0,0)), position=np.array((0,0,0)), piece_mesh=mesh.Mesh.from_file("stl/piece.stl")):
        """
        :param piece_mesh: Object defining shape of piece for rendering, will be DEEP COPIED
        :param rotation: tuple of rotations on X, Y and Z axis, in degrees
                            (90 , 180 , 0) means rotate 90 degrees in x and 180 degrees in y and 0 in z axis
        :param position: a tuple (x,y,z) of position in space.
        """

        self.rotation = rotation
        self.position = position
        self.mesh = deepcopy(piece_mesh)
        self.end1 = Hub(htype=Hub.TYPE_END_1, parent=self, parent_local_face=Orientation.FRONT)
        self.end2 = Hub(htype=Hub.TYPE_END_2, parent=self, parent_local_face=Orientation.BACK)
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