from copy import copy, deepcopy

import numpy as np
from stl import mesh

import hub
from display import random_color
from orientation import Orientation, orient_mesh, LOCAL_FRONT, LOCAL_BACK

PIECE_MESH = mesh.Mesh.from_file("stl/piece.stl")

class Piece:

    def __init__(self, orientation=None, rotation=np.array((0,0,0),dtype=int), position=np.array((0,0,0),dtype=int), piece_mesh=PIECE_MESH,
                 color=None, alpha=0.20):
        """
        :param piece_mesh:  Object defining shape of piece for rendering, will be DEEP COPIED
        :param orientation: Orientation object, if given - rotation is ignored.
        :param rotation:    tuple of rotations on X, Y and Z axis, in degrees
                            (90 , 180 , 0) means rotate 90 degrees in x and 180 degrees in y and 0 in z axis
                            IGNORED if orientation is given
        :param position: a tuple (x,y,z) of position in space.
        """
        if orientation:
            rotation = orientation.to_rotation()
        if not color:
            color = 'white'#random_color()
        self.rotation = rotation
        self.position = position
        self.end1 = hub.Hub(htype=hub.TYPE_END_1, parent=self, parent_local_face=LOCAL_FRONT, color=color)
        self.end2 = hub.Hub(htype=hub.TYPE_END_2, parent=self, parent_local_face=LOCAL_BACK, color=color)
        self.center = hub.Hub(htype=hub.TYPE_CENTER, parent=self, color=color)
        self.color = color
        self.alpha = alpha

    def get_mesh(self):
        """
        Return the piece's mesh
        :return: A mesh rotated and positioned in 3D space
        """
        mesh = deepcopy(PIECE_MESH)
        orient_mesh(mesh, self.rotation, self.position)
        return mesh

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
        return "{} : {}".format(np.array(self.position,dtype=int), self.orientation)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass