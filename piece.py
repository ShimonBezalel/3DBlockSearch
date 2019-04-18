import numpy as np
from stl import mesh


class Piece:

    def __init__(self, mesh, orientation, position):
        """

        :param mesh: Object defining shape of piece for rendering
        :param orientation: TODO: Define orientation standard (dice? vector? enum?)
        :param move: spawning parent move
        """
        self.mesh = mesh
        self.orientation = orientation
        self.position = position


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
        #TODO: needed for state copy
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

    def render(self):
        """
        Draw the piece
        :return: A mesh oriented and positioned in 3D space
        """
        # Mesh starts around 0,0,0, or origin

        # Rotate mesh into correct orientation using 3 rotations, around axis x y and z
        pass

        #

