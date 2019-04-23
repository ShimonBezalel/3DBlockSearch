import numpy as np
from stl import mesh

from grid import GRID_UNIT_IN_MM
from orientation import Orientation, orient_mesh
#from piece import Piece


class Hub:
    TYPE_END_1 = "END_HUB_1"
    TYPE_END_2 = "END_HUB_2"
    TYPE_CENTER = "CENTER_HUB"

    POSITION_SHIFT = 1.5 * GRID_UNIT_IN_MM
    END_POSITION_SHIFT_BY_FACE = {Orientation.TOP: np.array((0, 0, POSITION_SHIFT)),  # TOP
                                  Orientation.RIGHT: np.array((POSITION_SHIFT, 0, 0)),  # RIGHT
                                  Orientation.FRONT: np.array((0, -POSITION_SHIFT, 0)),  # FRONT
                                  Orientation.DOWN: np.array((0, 0, -POSITION_SHIFT)),  # DOWN
                                  Orientation.LEFT: np.array((-POSITION_SHIFT, 0, 0)),  # LEFT
                                  Orientation.BACK: np.array((0, POSITION_SHIFT, 0))}  # BACK

    PIECE_FACE_END_1 = Orientation.LEFT
    PIECE_FACE_END_2 = Orientation.RIGHT

    def __init__(self, htype, parent, parent_local_face=None): #TODO: Solve import problems of Piece, set default parent=Piece()
        """
        :param htype: One of discreet hub types
        :param orientation: Orientation object of this hub
        :param position:    (X,Y,Z) of the hub
        :param rotation:    (X_deg, Y_deg, Z_deg) rotation of the hub
        :param parent:      Spawning Piece object
        """
        self.htype = htype
        self.parent = parent

        if self.htype == Hub.TYPE_END_1:
            if not parent_local_face:
                parent_local_face = Orientation.FRONT
            self.mesh = mesh.Mesh.from_file("stl/hub_end_1.stl")
        elif self.htype == Hub.TYPE_END_2:
            if not parent_local_face:
                parent_local_face = Orientation.BACK
            self.mesh = mesh.Mesh.from_file("stl/hub_end_2.stl")
        elif self.htype == Hub.TYPE_CENTER:
            self.mesh = mesh.Mesh.from_file("stl/hub_center.stl")

        self.parent_local_face = parent_local_face

        #print(self.position)
        orient_mesh(self.mesh, self.rotation, self.position)

    def get_mesh(self):
        """
        Return the hub's mesh
        :return: A mesh rotated and positioned in 3D space
        """
        return self.mesh

    @property
    def position(self):
        if not self.parent_local_face: # Center Hub uses parent's position
            position_shift = np.array((0,0,0))
        else:
            parent_global_face = self.parent.orientation.local_to_global(self.parent_local_face)
            position_shift = Hub.END_POSITION_SHIFT_BY_FACE[parent_global_face] if parent_global_face else np.array((0, 0, 0))
        return self.parent.position + position_shift

    @property
    def rotation(self):
        return self.parent.rotation

    @property
    def orientation(self):
        return self.parent.orientation

    def can_connect(self, other):
        """
        Checks if this hub can sit in a single voxel along with the given other.
        :param other:
        :return:
        """
        if self.htype != other.htype:
            # TODO: Handle END_1 + END_2 cases
            return False

        if self.htype == Hub.TYPE_END_1:
            s = self.orientation
            o = other.orientation

            #      OPTION 1
            # --------+--------
            #   Self  |  Other
            # --------+--------
            #   TOP   |  LEFT
            #   RIGHT |  DOWN
            #   FRONT |  BACK

            if (s.top == o.left) and \
                    (s.right == o.down) and \
                    (s.front == o.back):
                return True

            #      OPTION 2
            # --------+--------
            #   Self  |  Other
            # --------+--------
            #   TOP   |  BACK
            #   RIGHT |  LEFT
            #   FRONT |  DOWN
            if (s.top == o.back) and \
                    (s.right == o.left) and \
                    (s.front == o.down):
                return True

            #      OPTION 3
            # --------+--------
            #   Self  |  Other
            # --------+--------
            #   TOP   |  DOWN
            #   RIGHT |  BACK
            #   FRONT |  LEFT
            if (s.top == o.down) and \
                    (s.right == o.back) and \
                    (s.front == o.left):
                return True

        return False

    def get_connectible_pieces(self):
        """
        Returns a list of potential pieces that can connect to this hub.
        The pieces are defined by thier positions and orientation relative to this hub.
        :return:
        """
        pass

    def get_type(self):
        pass

    def get_spawning_piece(self):
        """
        returns the parents piece of this hub.
        :return:
        """
        pass

    def __str__(self):
        pass
