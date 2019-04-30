from copy import copy, deepcopy

import numpy as np
from stl import mesh

from display import display_meshes_with_colors, random_color
import grid
from orientation import Orientation, orient_mesh, GLOBAL_TOP, GLOBAL_RIGHT, GLOBAL_FRONT, GLOBAL_DOWN, GLOBAL_LEFT, \
    GLOBAL_BACK, LOCAL_FRONT, LOCAL_BACK, LOCAL_TOP, LOCAL_Z_CW

import piece

END_1_MESH = mesh.Mesh.from_file("stl/hub_end_1.stl")
END_2_MESH = mesh.Mesh.from_file("stl/hub_end_2.stl")
CENTER_MESH = mesh.Mesh.from_file("stl/hub_center.stl")

# Orientations of END_1 hub (B) that connect to another END_1 hub (A) in the initial orientation
# Dict structure: {(A) Local Face : (B) Local Face}
END_1_TO_INITIAL_END_1_ORIENTATIONS = {Orientation(rotation=(0, 180, 90)),
                                       Orientation(rotation=(180, 90, 0)),
                                       Orientation(rotation=(270, 0, 180))}

END_2_TO_INITIAL_END_2_ORIENTATIONS = {Orientation(rotation=(180, 270, 0)),
                                       Orientation(rotation=(180, 0, 270)),
                                       Orientation(rotation=(90, 0, 180))}

END_2_TO_INITIAL_END_1_ORIENTATIONS = {Orientation(rotation=(180, 0, 90)),
                                       Orientation(rotation=(0, 270, 0)),
                                       Orientation(rotation=(90, 0, 0))}

END_1_TO_INITIAL_END_2_ORIENTATIONS = {Orientation(rotation=(0, 180, 270)),
                                       Orientation(rotation=(0, 90, 0)),
                                       Orientation(rotation=(270, 0, 0))}

CENTER_TO_INITIAL_CENTER_ORIENTATIONS = {Orientation(rotation=(180, 0, 90)),
                                         Orientation(rotation=(180, 0, 270)),
                                         Orientation(rotation=(270, 0, 180))}

# Hub Types
TYPE_END_1 = "END_HUB_1"
TYPE_END_2 = "END_HUB_2"
TYPE_CENTER = "CENTER_HUB"

# Local faces of piece where hubs are located
PIECE_LOCAL_FACE_END_1 = LOCAL_FRONT
PIECE_LOCAL_FACE_END_2 = LOCAL_BACK

# Position shift of hub center relative to piece center
POSITION_SHIFT = 1.5 * 20  # grid.GRID_UNIT_IN_MM
END_POSITION_SHIFT_BY_GLOBAL_FACE = {GLOBAL_TOP: np.array((0, 0, POSITION_SHIFT), dtype=int),  # TOP
                                     GLOBAL_RIGHT: np.array((POSITION_SHIFT, 0, 0), dtype=int),  # RIGHT
                                     GLOBAL_FRONT: np.array((0, -POSITION_SHIFT, 0), dtype=int),  # FRONT
                                     GLOBAL_DOWN: np.array((0, 0, -POSITION_SHIFT), dtype=int),  # DOWN
                                     GLOBAL_LEFT: np.array((-POSITION_SHIFT, 0, 0), dtype=int),  # LEFT
                                     GLOBAL_BACK: np.array((0, POSITION_SHIFT, 0), dtype=int)}  # BACK


class Hub:

    def __init__(self, htype, parent,
                 parent_local_face=None,
                 color=random_color(),
                 alpha=0.70):  # TODO: Solve import problems of Piece, set default parent=Piece()
        """
        :param htype: One of discreet hub types
        :param orientation: Orientation object of this hub
        :param position:    (X,Y,Z) of the hub
        :param rotation:    (X_deg, Y_deg, Z_deg) rotation of the hub
        :param parent:      Spawning Piece object
        """
        self.htype = htype
        self.parent = parent

        if self.htype == TYPE_END_1:
            if not parent_local_face:
                parent_local_face = LOCAL_FRONT
        elif self.htype == TYPE_END_2:
            if not parent_local_face:
                parent_local_face = LOCAL_BACK

        self.parent_local_face = parent_local_face
        self.color = color
        self.alpha = alpha

    def get_mesh(self):
        """
        Return the hub's mesh
        :return: A mesh rotated and positioned in 3D space
        """
        if self.htype == TYPE_END_1:
            mesh = deepcopy(END_1_MESH)
        elif self.htype == TYPE_END_2:
            mesh = deepcopy(END_2_MESH)
        elif self.htype == TYPE_CENTER:
            mesh = deepcopy(CENTER_MESH)
        else:
            raise AssertionError('Self has invalid hub type {}!'.format(self.htype))
        orient_mesh(mesh, self.rotation, self.position)
        return mesh

    @property
    def position(self):
        if not self.parent_local_face:  # Center Hub uses parent's position
            position_shift = np.array((0, 0, 0), dtype=int)
        else:
            parent_global_face = self.parent.orientation.local_face_to_global_face(self.parent_local_face)
            position_shift = END_POSITION_SHIFT_BY_GLOBAL_FACE[
                parent_global_face] if parent_global_face else np.array((0, 0, 0), dtype=int)
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
        if (self.htype == TYPE_CENTER and other.htype != TYPE_CENTER) or \
                (self.htype != TYPE_CENTER and other.htype == TYPE_CENTER):
            return False

        global_rotations_from_reset = self.orientation.get_global_rotations_from_reset()
        if self.htype == TYPE_END_1:
            # Pieces connecting through their END_1
            if other.htype == TYPE_END_1:
                for orientation in END_1_TO_INITIAL_END_1_ORIENTATIONS:
                    orientation = copy(orientation)
                    # Translate the connection to current orientation of self
                    orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                    if other.orientation == orientation:
                        return True

            # Pieces connecting through their END_2
            elif other.htype == TYPE_END_2:
                for orientation in END_2_TO_INITIAL_END_1_ORIENTATIONS:
                    orientation = copy(orientation)
                    # Translate the connection to current orientation of self
                    orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                    if other.orientation == orientation:
                        return True

        elif self.htype == TYPE_END_2:
            # Pieces connecting through their END_2
            if other.htype == TYPE_END_2:
                for orientation in END_2_TO_INITIAL_END_2_ORIENTATIONS:
                    orientation = copy(orientation)
                    # Translate the connection to current orientation of self
                    orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                    if other.orientation == orientation:
                        return True

            # Pieces connecting through their END_1
            elif other.htype == TYPE_END_1:
                for orientation in END_1_TO_INITIAL_END_2_ORIENTATIONS:
                    orientation = copy(orientation)
                    # Translate the connection to current orientation of self
                    orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                    if other.orientation == orientation:
                        return True

        elif self.htype == TYPE_CENTER:
            # Pieces connecting through their END_2
            for orientation in CENTER_TO_INITIAL_CENTER_ORIENTATIONS:
                orientation = copy(orientation)
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                if other.orientation == orientation:
                    return True
        return False

    def get_connectible_pieces(self):
        """
        Returns a list of potential pieces that can connect to this hub.
        :return:
        """
        global_rotations_from_reset = self.orientation.get_global_rotations_from_reset()
        pieces = []
        if self.htype == TYPE_END_1:
            # Pieces connecting through their END_1
            for orientation in END_1_TO_INITIAL_END_1_ORIENTATIONS:
                orientation = copy(orientation)
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_1)
                # Find respective shift of piece center
                position_shift = tuple([-1 * shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_1_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                pieces.append(end_1_piece)

            # Pieces connecting through their END_2
            for orientation in END_2_TO_INITIAL_END_1_ORIENTATIONS:
                orientation = copy(orientation)
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_2)
                # Find respective shift of piece center
                position_shift = tuple([-1 * shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_2_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                pieces.append(end_2_piece)

        elif self.htype == TYPE_END_2:
            # Pieces connecting through their END_2
            for orientation in END_2_TO_INITIAL_END_2_ORIENTATIONS:
                orientation = copy(orientation)
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_2)
                # Find respective shift of piece center
                position_shift = tuple([-1 * shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_2_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                pieces.append(end_2_piece)

            # Pieces connecting through their END_1
            for orientation in END_1_TO_INITIAL_END_2_ORIENTATIONS:
                orientation = copy(orientation)
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_1)
                # Find respective shift of piece center
                position_shift = tuple([-1 * shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_1_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                pieces.append(end_1_piece)

        elif self.htype == TYPE_CENTER:
            # Pieces connecting through their END_2
            for orientation in CENTER_TO_INITIAL_CENTER_ORIENTATIONS:
                orientation = copy(orientation)
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Generate matching piece
                center_piece = piece.Piece(orientation=orientation, position=self.position)
                pieces.append(center_piece)

        return pieces

    def get_type(self):
        pass

    def get_spawning_piece(self):
        """
        returns the parents piece of this hub.
        :return:
        """
        pass

    def __str__(self):
        return "{} : {} : {}".format(self.htype, np.array(self.position,dtype=int), self.orientation)

    def __repr__(self):
        return str(self)
