import numpy as np
from stl import mesh


class Piece:

    def __init__(self, shape, orientation, position):
        """

        :param shape: Object defining shape of piece for rendering
        :param orientation: tuple of rotations on X, Y and Z axis, in degrees
                            (90 , 180 , 0) means rotate 90 degrees in x and 180 degrees in y and 0 in z axis
        :param position: a tuple (x,y,z) of position in space.
        """
        self.mesh = mesh.Mesh(shape.copy())
        self.orientation = orientation
        self.position = position
        self.rendered_mesh = None


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
        if (self.rendered_mesh):
            return self.rendered_mesh

        # Rotate mesh into correct orientation using 3 rotations, around axis x, y, and z
        self.mesh.rotate()

        # Translate to correct position. Translations happens from center of the mesh's mass to the objects location

