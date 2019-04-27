from copy import copy, deepcopy

import numpy as np
from stl import mesh

from display import display_meshes_with_colors
from grid import GRID_UNIT_IN_MM
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

END_2_TO_INITIAL_END_2_ORIENTATIONS = {Orientation(rotation=(90, 0, 180)),
                                       Orientation(rotation=(0, 180, 90)),
                                       Orientation(rotation=(0, 270, 180))}

END_2_TO_INITIAL_END_1_ORIENTATIONS = {Orientation(rotation=(180, 0, 90)),
                                       Orientation(rotation=(0, 270, 0)),
                                       Orientation(rotation=(90, 0, 0))}

END_1_TO_INITIAL_END_2_ORIENTATIONS = {Orientation(rotation=(0, 180, 90)),
                                       Orientation(rotation=(00, 270, 0)),
                                       Orientation(rotation=(90, 0, 00))}

CENTER_TO_INITIAL_CENTER_ORIENTATIONS = {Orientation(rotation=(180, 0, 90)),
                                         Orientation(rotation=(180, 0, 270)),
                                         Orientation(rotation=(90, 0, 180))}

# Hub Types
TYPE_END_1 = "END_HUB_1"
TYPE_END_2 = "END_HUB_2"
TYPE_CENTER = "CENTER_HUB"

# Local faces of piece where hubs are located
PIECE_LOCAL_FACE_END_1 = LOCAL_FRONT
PIECE_LOCAL_FACE_END_2 = LOCAL_BACK

# Position shift of hub center relative to piece center
POSITION_SHIFT = 1.5 * GRID_UNIT_IN_MM
END_POSITION_SHIFT_BY_GLOBAL_FACE = {GLOBAL_TOP: np.array((0, 0, POSITION_SHIFT)),  # TOP
                                     GLOBAL_RIGHT: np.array((POSITION_SHIFT, 0, 0)),  # RIGHT
                                     GLOBAL_FRONT: np.array((0, -POSITION_SHIFT, 0)),  # FRONT
                                     GLOBAL_DOWN: np.array((0, 0, -POSITION_SHIFT)),  # DOWN
                                     GLOBAL_LEFT: np.array((-POSITION_SHIFT, 0, 0)),  # LEFT
                                     GLOBAL_BACK: np.array((0, POSITION_SHIFT, 0))}  # BACK

class Hub:

    def __init__(self, htype, parent,
                 parent_local_face=None):  # TODO: Solve import problems of Piece, set default parent=Piece()
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
            self.mesh = deepcopy(END_1_MESH)
        elif self.htype == TYPE_END_2:
            if not parent_local_face:
                parent_local_face = LOCAL_BACK
            self.mesh = deepcopy(END_2_MESH)
        elif self.htype == TYPE_CENTER:
            self.mesh = deepcopy(CENTER_MESH)

        self.parent_local_face = parent_local_face

        orient_mesh(self.mesh, self.rotation, self.position)

    def get_mesh(self):
        """
        Return the hub's mesh
        :return: A mesh rotated and positioned in 3D space
        """
        return self.mesh

    @property
    def position(self):
        if not self.parent_local_face:  # Center Hub uses parent's position
            position_shift = np.array((0, 0, 0))
        else:
            parent_global_face = self.parent.orientation.local_face_to_global_face(self.parent_local_face)
            position_shift = END_POSITION_SHIFT_BY_GLOBAL_FACE[
                parent_global_face] if parent_global_face else np.array((0, 0, 0))
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

        # Compare when translating both so that self is reset
        global_rotations_towards_reset = self.orientation.get_global_rotations_towards_reset()
        o = copy(other.orientation)
        o.rotate_multiple_global_axis(global_rotations_towards_reset)

        if self.htype == TYPE_END_1:
            if other.htype == TYPE_END_1:
                return o in END_1_TO_INITIAL_END_1_ORIENTATIONS
            if other.htype == TYPE_END_2:
                return o in END_2_TO_INITIAL_END_1_ORIENTATIONS

        if self.htype == TYPE_END_2:
            if other.htype == TYPE_END_1:
                return o in END_1_TO_INITIAL_END_2_ORIENTATIONS
            if other.htype == TYPE_END_2:
                return o in END_2_TO_INITIAL_END_2_ORIENTATIONS

        if self.htype == TYPE_CENTER: # we already validated in this case they are identical
            return o in CENTER_TO_INITIAL_CENTER_ORIENTATIONS

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
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_1)
                # Find respective shift of piece center
                position_shift = tuple([-1 * shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_1_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                #display_meshes_with_colors([self.get_mesh(), end_1_piece.get_mesh()], ['white','purple'])
                pieces.append(end_1_piece)

            # Pieces connecting through their END_2
            for orientation in END_2_TO_INITIAL_END_1_ORIENTATIONS:
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_2)
                # Find respective shift of piece center
                position_shift = tuple([-1*shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_2_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                display_meshes_with_colors([self.get_mesh(), end_2_piece.get_mesh()], ['white','purple'])
                pieces.append(end_2_piece)

        elif self.htype == TYPE_END_2:
            # Pieces connecting through their END_2
            for orientation in END_2_TO_INITIAL_END_2_ORIENTATIONS:
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_2)
                # Find respective shift of piece center
                position_shift = tuple([-1 * shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_2_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                #display_meshes_with_colors([self.get_mesh(), end_2_piece.get_mesh()], ['white','purple'])
                pieces.append(end_2_piece)

            # Pieces connecting through their END_2
            for orientation in END_1_TO_INITIAL_END_2_ORIENTATIONS:
                # Translate the connection to current orientation of self
                orientation.rotate_multiple_global_axis(global_rotations_from_reset)
                # Find global face of this connection
                global_face = orientation.local_face_to_global_face(PIECE_LOCAL_FACE_END_1)
                # Find respective shift of piece center
                position_shift = tuple([-1*shift for shift in END_POSITION_SHIFT_BY_GLOBAL_FACE[global_face]])
                # Generate matching piece
                end_1_piece = piece.Piece(orientation=orientation, position=self.position + position_shift)
                display_meshes_with_colors([self.get_mesh(), end_1_piece.get_mesh()], ['white','purple'])
                pieces.append(end_1_piece)

        # TODO: Handle END_2 and CENTER
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
        pass
