from copy import copy
from util import TwoWayDict, dictInverted
import numpy as np

# Local Faces
LOCAL_TOP = "Local Top"
LOCAL_RIGHT = "Local Right"
LOCAL_FRONT = "Local Front"
LOCAL_DOWN = "Local Down"
LOCAL_BACK = "Local Back"
LOCAL_LEFT = "Local Left"
LOCAL_FACES = (LOCAL_TOP, LOCAL_RIGHT, LOCAL_FRONT, LOCAL_DOWN, LOCAL_LEFT, LOCAL_BACK)

# Local Rotation Axes
LOCAL_X_CW = 'Local Right-Left Clockwise'
LOCAL_Y_CW = 'Local Front-Back Clockwise'
LOCAL_Z_CW = 'Local Top-Down Clockwise'
LOCAL_X_CCW = 'Local Right-Left Counter-Clockwise'
LOCAL_Y_CCW = 'Local Front-Back Counter-Clockwise'
LOCAL_Z_CCW = 'Local Top-Down Counter-Clockwise'
LOCAL_ROTATION_AXES = (LOCAL_X_CW, LOCAL_Y_CW, LOCAL_Z_CW, LOCAL_X_CCW, LOCAL_Y_CCW, LOCAL_Z_CCW)

# Global Faces
GLOBAL_TOP = "Global Top"
GLOBAL_RIGHT = "Global Right"
GLOBAL_FRONT = "Global Front"
GLOBAL_DOWN = "Global Down"
GLOBAL_BACK = "Global Back"
GLOBAL_LEFT = "Global Left"
GLOBAL_FACES = (GLOBAL_TOP, GLOBAL_RIGHT, GLOBAL_FRONT, GLOBAL_DOWN, GLOBAL_LEFT, GLOBAL_BACK)

# Global Rotation Axes
GLOBAL_X_CW = 'Global Right-Left Clockwise'
GLOBAL_Y_CW = 'Global Front-Back Clockwise'
GLOBAL_Z_CW = 'Global Top-Down Clockwise'
GLOBAL_X_CCW = 'Global Right-Left Counter-Clockwise'
GLOBAL_Y_CCW = 'Global Front-Back Counter-Clockwise'
GLOBAL_Z_CCW = 'Global Top-Down Counter-Clockwise'
GLOBAL_ROTATION_AXES = (GLOBAL_X_CW, GLOBAL_Y_CW, GLOBAL_Z_CW, GLOBAL_X_CCW, GLOBAL_Y_CCW, GLOBAL_Z_CCW)

# Initial Mapping (Global face = Local face)
INITIAL_MAPPING = TwoWayDict({GLOBAL_TOP: LOCAL_TOP,
                              GLOBAL_RIGHT: LOCAL_RIGHT,
                              GLOBAL_FRONT: LOCAL_FRONT,
                              GLOBAL_DOWN: LOCAL_DOWN,
                              GLOBAL_LEFT: LOCAL_LEFT,
                              GLOBAL_BACK: LOCAL_BACK})

# Local Rotation Dictionaries - lookup global face by local face ('at which global face is the local front?')
# Rotation clockwise across local Right-Left axis
ROTATION_LOCAL_X_CW = {LOCAL_TOP: LOCAL_BACK,  # TOP
                       LOCAL_RIGHT: LOCAL_RIGHT,  # RIGHT
                       LOCAL_FRONT: LOCAL_TOP,  # FRONT
                       LOCAL_DOWN: LOCAL_FRONT,  # DOWN
                       LOCAL_LEFT: LOCAL_LEFT,  # LEFT
                       LOCAL_BACK: LOCAL_DOWN}  # BACK
ROTATION_LOCAL_X_CCW = dictInverted(ROTATION_LOCAL_X_CW)

# Rotation clockwise across LOCAL Front-Back axis
ROTATION_LOCAL_Y_CW = {LOCAL_TOP: LOCAL_RIGHT,  # TOP
                       LOCAL_RIGHT: LOCAL_DOWN,  # RIGHT
                       LOCAL_FRONT: LOCAL_FRONT,  # FRONT
                       LOCAL_DOWN: LOCAL_LEFT,  # DOWN
                       LOCAL_LEFT: LOCAL_TOP,  # LEFT
                       LOCAL_BACK: LOCAL_BACK}  # BACK
ROTATION_LOCAL_Y_CCW = dictInverted(ROTATION_LOCAL_Y_CW)

# Rotation clockwise across LOCAL Top-Down axis
ROTATION_LOCAL_Z_CW = {LOCAL_TOP: LOCAL_TOP,  # TOP
                       LOCAL_RIGHT: LOCAL_FRONT,  # RIGHT
                       LOCAL_FRONT: LOCAL_LEFT,  # FRONT
                       LOCAL_DOWN: LOCAL_DOWN,  # DOWN
                       LOCAL_LEFT: LOCAL_BACK,  # LEFT
                       LOCAL_BACK: LOCAL_RIGHT}  # BACK
ROTATION_LOCAL_Z_CCW = dictInverted(ROTATION_LOCAL_Z_CW)

# Rotation dictionary by rotation axis
ROTATION_LOCAL = {LOCAL_X_CW: ROTATION_LOCAL_X_CW,
                  LOCAL_Y_CW: ROTATION_LOCAL_Y_CW,
                  LOCAL_Z_CW: ROTATION_LOCAL_Z_CW,
                  LOCAL_X_CCW: ROTATION_LOCAL_X_CCW,
                  LOCAL_Y_CCW: ROTATION_LOCAL_Y_CCW,
                  LOCAL_Z_CCW: ROTATION_LOCAL_Z_CCW}

# Conversion from face to normal axis
LOCAL_FACE_TO_AXIS = {LOCAL_TOP: LOCAL_Z_CW,
                      LOCAL_RIGHT: LOCAL_X_CW,
                      LOCAL_FRONT: LOCAL_Y_CW,
                      LOCAL_DOWN: LOCAL_Z_CCW,
                      LOCAL_LEFT: LOCAL_X_CCW,
                      LOCAL_BACK: LOCAL_Y_CCW}
LOCAL_AXIS_TO_FACE = dictInverted(LOCAL_FACE_TO_AXIS)

# Global rotation dictionaries - lookup local face by global face ('what local face is at global top?')
# Rotation clockwise across global Right-Left axis
ROTATION_GLOBAL_X_CW = {GLOBAL_TOP: GLOBAL_BACK,  # TOP
                        GLOBAL_RIGHT: GLOBAL_RIGHT,  # RIGHT
                        GLOBAL_FRONT: GLOBAL_TOP,  # FRONT
                        GLOBAL_DOWN: GLOBAL_FRONT,  # DOWN
                        GLOBAL_LEFT: GLOBAL_LEFT,  # LEFT
                        GLOBAL_BACK: GLOBAL_DOWN}  # BACK
ROTATION_GLOBAL_X_CCW = dictInverted(ROTATION_GLOBAL_X_CW)

# Rotation clockwise across global Front-Back axis
ROTATION_GLOBAL_Y_CW = {GLOBAL_TOP: GLOBAL_RIGHT,  # TOP
                        GLOBAL_RIGHT: GLOBAL_DOWN,  # RIGHT
                        GLOBAL_FRONT: GLOBAL_FRONT,  # FRONT
                        GLOBAL_DOWN: GLOBAL_LEFT,  # DOWN
                        GLOBAL_LEFT: GLOBAL_TOP,  # LEFT
                        GLOBAL_BACK: GLOBAL_BACK}  # BACK
ROTATION_GLOBAL_Y_CCW = dictInverted(ROTATION_GLOBAL_Y_CW)

# Rotation clockwise across global Top-Down axis
ROTATION_GLOBAL_Z_CW = {GLOBAL_TOP: GLOBAL_TOP,  # TOP
                        GLOBAL_RIGHT: GLOBAL_FRONT,  # RIGHT
                        GLOBAL_FRONT: GLOBAL_LEFT,  # FRONT
                        GLOBAL_DOWN: GLOBAL_DOWN,  # DOWN
                        GLOBAL_LEFT: GLOBAL_BACK,  # LEFT
                        GLOBAL_BACK: GLOBAL_RIGHT}  # BACK
ROTATION_GLOBAL_Z_CCW = dictInverted(ROTATION_GLOBAL_Z_CW)

# Rotation dictionary by rotation axis
ROTATION_GLOBAL = {GLOBAL_X_CW: ROTATION_GLOBAL_X_CW,
                   GLOBAL_Y_CW: ROTATION_GLOBAL_Y_CW,
                   GLOBAL_Z_CW: ROTATION_GLOBAL_Z_CW,
                   GLOBAL_X_CCW: ROTATION_GLOBAL_X_CCW,
                   GLOBAL_Y_CCW: ROTATION_GLOBAL_Y_CCW,
                   GLOBAL_Z_CCW: ROTATION_GLOBAL_Z_CCW}

# Conversion from face to normal axis
GLOBAL_FACE_TO_AXIS = {GLOBAL_TOP: GLOBAL_Z_CW,
                       GLOBAL_RIGHT: GLOBAL_X_CW,
                       GLOBAL_FRONT: GLOBAL_Y_CW,
                       GLOBAL_DOWN: GLOBAL_Z_CCW,
                       GLOBAL_LEFT: GLOBAL_X_CCW,
                       GLOBAL_BACK: GLOBAL_Y_CCW}
GLOBAL_AXIS_TO_FACE = dictInverted(GLOBAL_FACE_TO_AXIS)

# Inverted Rotations Dictionary
INVERT_ROTATIONS = {LOCAL_X_CW: LOCAL_X_CCW,
                    LOCAL_X_CCW: LOCAL_X_CW,
                    LOCAL_Y_CW: LOCAL_Y_CCW,
                    LOCAL_Y_CCW: LOCAL_Y_CW,
                    LOCAL_Z_CW: LOCAL_Z_CCW,
                    LOCAL_Z_CCW: LOCAL_Z_CW,
                    GLOBAL_X_CW: GLOBAL_X_CCW,
                    GLOBAL_X_CCW: GLOBAL_X_CW,
                    GLOBAL_Y_CW: GLOBAL_Y_CCW,
                    GLOBAL_Y_CCW: GLOBAL_Y_CW,
                    GLOBAL_Z_CW: GLOBAL_Z_CCW,
                    GLOBAL_Z_CCW: GLOBAL_Z_CW}

STR_TO_ROTATIONS_FROM_RESET = {'{ T | R | F | D | L | B }': [],
                               '{ T | B | R | D | F | L }': [GLOBAL_Z_CW],
                               '{ T | L | B | D | R | F }': [GLOBAL_Z_CW, GLOBAL_Z_CW],
                               '{ T | F | L | D | B | R }': [GLOBAL_Z_CCW],
                               '{ L | T | F | R | D | B }': [GLOBAL_Y_CW],
                               '{ L | B | T | R | F | D }': [GLOBAL_Y_CW, GLOBAL_Z_CW],
                               '{ L | D | B | R | T | F }': [GLOBAL_Y_CW, GLOBAL_Z_CW, GLOBAL_Z_CW],
                               '{ L | F | D | R | B | T }': [GLOBAL_Y_CW, GLOBAL_Z_CCW],
                               '{ D | L | F | T | R | B }': [GLOBAL_Y_CW, GLOBAL_Y_CW],
                               '{ D | B | L | T | F | R }': [GLOBAL_Y_CW, GLOBAL_Y_CW, GLOBAL_Z_CW],
                               '{ D | R | B | T | L | F }': [GLOBAL_Y_CW, GLOBAL_Y_CW, GLOBAL_Z_CW, GLOBAL_Z_CW],
                               '{ D | F | R | T | B | L }': [GLOBAL_Y_CW, GLOBAL_Y_CW, GLOBAL_Z_CCW],
                               '{ R | D | F | L | T | B }': [GLOBAL_Y_CCW],
                               '{ R | B | D | L | F | T }': [GLOBAL_Y_CCW, GLOBAL_Z_CW],
                               '{ R | T | B | L | D | F }': [GLOBAL_Y_CCW, GLOBAL_Z_CW, GLOBAL_Z_CW],
                               '{ R | F | T | L | B | D }': [GLOBAL_Y_CCW, GLOBAL_Z_CCW],
                               '{ F | R | D | B | L | T }': [GLOBAL_X_CW],
                               '{ F | T | R | B | D | L }': [GLOBAL_X_CW, GLOBAL_Z_CW],
                               '{ F | L | T | B | R | D }': [GLOBAL_X_CW, GLOBAL_Z_CW, GLOBAL_Z_CW],
                               '{ F | D | L | B | T | R }': [GLOBAL_X_CW, GLOBAL_Z_CCW],
                               '{ B | L | D | F | R | T }': [GLOBAL_X_CW, GLOBAL_Y_CW, GLOBAL_Y_CW],
                               '{ B | T | L | F | D | R }': [GLOBAL_X_CW, GLOBAL_Y_CW, GLOBAL_Y_CW, GLOBAL_Z_CW],
                               '{ B | R | T | F | L | D }': [GLOBAL_X_CW, GLOBAL_Y_CW, GLOBAL_Y_CW, GLOBAL_Z_CW,
                                                             GLOBAL_Z_CW],
                               '{ B | D | R | F | T | L }': [GLOBAL_X_CW, GLOBAL_Y_CW, GLOBAL_Y_CW, GLOBAL_Z_CCW]
                               }


class Orientation:
    """
    A class representing a piece's orientation.
    It wraps a TwoWayDict ('orientation_mapping') representing the orientation of the piece:
    {GLOBAL_FACE : LOCAL_FACE} per each face
    """

    def __init__(self, orientation_mapping=None, rotation=None, global_rotations=None):
        """
        Convert the given input to an Orientation object.
        If orientation_mapping is given - it is wrapped by an Orientation object, and rotation is IGNORED.
        If only rotation is given - create Orientation by rotating the initial orientation accordingly (note that order
        of rotations is x, then y, then z, and that order matters!)
        If no parameter is given - Copy the initial orientation.
        :param orientation_mapping:  Optional - TwoWayDict ({GLOBAL_FACE : LOCAL_FACE} for each face)
        :param rotation:             Optional - Rotation tuple (x_deg, y_deg, z_deg) IGNORED if orientation_mapping is given
        :param global_rotations:     Optional - A list of global rotations to apply to the initial orientation
        """

        if orientation_mapping:
            self.__orientation_mapping = copy(orientation_mapping)

        else:
            self.__orientation_mapping = copy(INITIAL_MAPPING)

            # Apply rotation to orientation_mapping
            if not (rotation is None):

                # Validate rotation format
                assert len(rotation) == 3, "invalid rotation format"

                x_deg, y_deg, z_deg = rotation
                assert x_deg % 90 == 0, "x rotation must be integer number of 90 degrees"
                assert y_deg % 90 == 0, "y rotation must be integer number of 90 degrees"
                assert z_deg % 90 == 0, "z rotation must be integer number of 90 degrees"
                assert x_deg >= 0, 'x rotation must be non-negative'
                assert y_deg >= 0, 'y rotation must be non-negative'
                assert z_deg >= 0, 'z rotation must be non-negative'

                # Global rotate X
                for global_x_rotation in range(int(x_deg / 90)):
                    self.rotate_90deg_global_axis(GLOBAL_X_CW)
                # Global rotate Y
                for global_y_rotation in range(int(y_deg / 90)):
                    self.rotate_90deg_global_axis(GLOBAL_Y_CW)
                # Global rotate Z
                for global_z_rotation in range(int(z_deg / 90)):
                    self.rotate_90deg_global_axis(GLOBAL_Z_CW)

            elif not (global_rotations is None):
                self.rotate_multiple_global_axis(global_rotations)

    def local_face_to_global_face(self, local_face):
        """
        At which global face is the given local face?
        """
        return self.__orientation_mapping[local_face]

    def global_face_to_local_face(self, global_face):
        """
        Which local faces is at the given global face?
        """
        return self.__orientation_mapping[global_face]

    def local_axis_to_global_axis(self, local_axis):
        """
        Which global axis converges with the given local axis?
        :param local_axis: Axis from LOCAL_ROTATION_AXES
        :return: Axis from GLOBAL_ROTATION_AXES
        """
        local_normal_face = LOCAL_AXIS_TO_FACE[local_axis]
        global_normal_face = self.local_face_to_global_face(local_normal_face)
        global_axis = GLOBAL_FACE_TO_AXIS[global_normal_face]
        return global_axis

    @staticmethod
    def get_rotated_90deg_global(orientation_mapping, global_axis):
        """
        Return a copy of the given orientation_mapping, rotated 90 degrees along the given global axis.
        :param orientation_mapping: TwoWayDict {GLOBAL_FACE : LOCAL_FACE} for each face
        :param global_axis:         Global rotation axis from GLOBAL_ROTATION_AXES
        :return:                    TwoWayDict - Copy of input orientation_mapping, rotated 90 degrees along given
                                    global axis.
        """
        # Validate arguments
        assert global_axis in GLOBAL_ROTATION_AXES

        # Build rotated orientation
        rotation_dict = ROTATION_GLOBAL[global_axis]
        rotated_mapping = TwoWayDict()

        # Move local faces according to global rotation
        for global_face in GLOBAL_FACES:
            local_face = orientation_mapping[global_face]
            global_face_rotated = rotation_dict[global_face]
            rotated_mapping[global_face_rotated] = local_face

        return rotated_mapping

    def rotate_90deg_global_axis(self, global_axis):
        """
        Rotate this orientation with 90 degrees clockwise around the given global axis
        :param global_axis: Rotation axis from GLOBAL_ROTATION_AXES
        """
        self.__orientation_mapping = Orientation.get_rotated_90deg_global(self.__orientation_mapping, global_axis)

    def rotate_multiple_global_axis(self, global_rotations):
        """
        Apply the given global rotations to this orientation
        :param global_rotations: List of global rotation axes from GLOBAL_ROTATION_AXES
        """
        for global_rotation in global_rotations:
            self.rotate_90deg_global_axis(global_rotation)

    def rotate_90deg_local_axis(self, local_axis):
        """
        Rotate this orientation with 90 degrees clockwise around the given global axis
        :param global_axis: Rotation axis from LOCAL_ROTATION_AXES
        """
        global_axis = self.local_axis_to_global_axis(local_axis)
        return self.rotate_90deg_global_axis(global_axis)

    def get_global_rotations_towards_reset(self):
        """
        Returns a list of 90-deg global rotation axes to apply for returning this orientation to the initial.
        Example:
            Initial orientation --> [] (no action required)
            Initial rotated 90 deg over global x --> [x,x,x] (rotate 3 more times around x to return to initial)
            Initial rotated 90 deg over global x, then 270 deg over global y --> [y,x,x,x]
        :return:
        """
        rotated = copy(self)
        rotations = []

        # Correct TOP if misplaced
        global_of_local_top = rotated.global_of_local_top
        if global_of_local_top != GLOBAL_TOP:
            # Is it all the way down?
            if global_of_local_top == GLOBAL_DOWN:
                # Rotate twice over x to correct
                rotations.append(GLOBAL_X_CW)
                rotations.append(GLOBAL_X_CW)
            # Otherwise, is it on one of the sides?
            elif global_of_local_top == GLOBAL_FRONT:
                rotations.append(GLOBAL_X_CW)
            elif global_of_local_top == GLOBAL_LEFT:
                rotations.append(GLOBAL_Y_CW)
            elif global_of_local_top == GLOBAL_BACK:
                rotations.append(GLOBAL_X_CCW)
            elif global_of_local_top == GLOBAL_RIGHT:
                rotations.append(GLOBAL_Y_CCW)
            else:
                raise AssertionError("local TOP face in an invalid global face '{}'!".format(global_of_local_top))

        # Apply rotations to rotated copy
        for rotation in rotations:
            rotated.rotate_90deg_global_axis(rotation)

        # Now TOP is correct, fix the sides
        global_face_of_local_front = rotated.global_of_local_front
        if global_face_of_local_front != GLOBAL_FRONT:
            if global_face_of_local_front == GLOBAL_LEFT:
                rotations.append(GLOBAL_Z_CW)
            elif global_face_of_local_front == GLOBAL_BACK:
                rotations.append(GLOBAL_Z_CW)
                rotations.append(GLOBAL_Z_CW)
            elif global_face_of_local_front == GLOBAL_RIGHT:
                rotations.append(GLOBAL_Z_CCW)
            else:
                raise AssertionError(
                    "local FRONT face in an invalid global face '{}'!".format(global_face_of_local_front))

        return rotations

    def get_global_rotations_from_reset(self):
        """
        Returns a list of 90-deg global rotation axes to apply for getting the initial orientation to this one.
        Example:
            Initial orientation --> [] (no action required)
            Initial rotated 90 deg over global x --> [x] (rotate 1 time around x)
            Initial rotated 90 deg over global x, then 270 deg over global y --> [x,y,y,y]
        """
        return STR_TO_ROTATIONS_FROM_RESET[str(self)]

        s = copy(self)
        rotated = Orientation()
        global_rotations = []

        # Single axis (or inverted axis) rotations?
        only_z = False
        if self.local_at_global_top == LOCAL_DOWN:
            rotated.rotate_90deg_global_axis(GLOBAL_X_CW)
            rotated.rotate_90deg_global_axis(GLOBAL_X_CW)
            global_rotations.append(GLOBAL_X_CW)
            global_rotations.append(GLOBAL_X_CW)
            only_z = True
        if self.local_at_global_top == LOCAL_TOP:
            only_z = True

        if only_z:
            # Only Z rotations required
            while rotated.local_at_global_front != self.local_at_global_front:
                rotated.rotate_90deg_global_axis(GLOBAL_Z_CW)
                global_rotations.append(GLOBAL_Z_CW)
            return global_rotations

        only_y = False
        if self.local_at_global_front == LOCAL_BACK:
            rotated.rotate_90deg_global_axis(GLOBAL_X_CW)
            rotated.rotate_90deg_global_axis(GLOBAL_X_CW)
            global_rotations.append(GLOBAL_X_CW)
            global_rotations.append(GLOBAL_X_CW)
            only_y = True
        if self.local_at_global_front == LOCAL_FRONT:
            only_y = True

        if only_y:
            # Only Y rotations required
            while rotated.local_at_global_top != self.local_at_global_top:
                rotated.rotate_90deg_global_axis(GLOBAL_Y_CW)
                global_rotations.append(GLOBAL_Y_CW)
            return global_rotations

        only_x = False
        if self.local_at_global_right == LOCAL_LEFT:
            rotated.rotate_90deg_global_axis(GLOBAL_Y_CW)
            rotated.rotate_90deg_global_axis(GLOBAL_Y_CW)
            global_rotations.append(GLOBAL_Y_CW)
            global_rotations.append(GLOBAL_Y_CW)
            only_x = True
        if self.local_at_global_right == LOCAL_RIGHT:
            only_x = True

        if only_x:
            # Only X rotations required
            while rotated.local_at_global_top != self.local_at_global_top:
                rotated.rotate_90deg_global_axis(GLOBAL_X_CW)
                global_rotations.append(GLOBAL_X_CW)
            return global_rotations

        # Two axis rotations
        # Start with X
        rotated.rotate_90deg_global_axis(GLOBAL_X_CW)
        global_rotations.append(GLOBAL_X_CW)
        # Then rotate along Y
        while rotated.local_at_global_top != self.local_at_global_top:
            rotated.rotate_90deg_global_axis(GLOBAL_Y_CW)
            global_rotations.append(GLOBAL_Y_CW)
        while rotated.local_at_global_front != self.local_at_global_front:
            rotated.rotate_90deg_global_axis(GLOBAL_Z_CW)
            global_rotations.append(GLOBAL_Z_CW)
        return global_rotations

    def to_rotation(self):
        """
        Return the rotation (x,y,z) of this orientation with respect to the initial (0,0,0)
        """
        rotations = self.get_global_rotations_from_reset()
        return (90 * (rotations.count(GLOBAL_X_CW) - rotations.count(GLOBAL_X_CCW)) % 360,
                90 * (rotations.count(GLOBAL_Y_CW) - rotations.count(GLOBAL_Y_CCW)) % 360,
                90 * (rotations.count(GLOBAL_Z_CW) - rotations.count(GLOBAL_Z_CCW)) % 360)

    # Easy access properties
    # Local faces
    @property
    def global_of_local_top(self):
        return self.__orientation_mapping[LOCAL_TOP]

    @property
    def global_of_local_right(self):
        return self.__orientation_mapping[LOCAL_RIGHT]

    @property
    def global_of_local_front(self):
        return self.__orientation_mapping[LOCAL_FRONT]

    @property
    def global_of_local_down(self):
        return self.__orientation_mapping[LOCAL_DOWN]

    @property
    def global_of_local_left(self):
        return self.__orientation_mapping[LOCAL_LEFT]

    @property
    def global_of_local_back(self):
        return self.__orientation_mapping[LOCAL_BACK]

    # Global faces
    @property
    def local_at_global_top(self):
        return self.__orientation_mapping[GLOBAL_TOP]

    @property
    def local_at_global_right(self):
        return self.__orientation_mapping[GLOBAL_RIGHT]

    @property
    def local_at_global_front(self):
        return self.__orientation_mapping[GLOBAL_FRONT]

    @property
    def local_at_global_down(self):
        return self.__orientation_mapping[GLOBAL_DOWN]

    @property
    def local_at_global_left(self):
        return self.__orientation_mapping[GLOBAL_LEFT]

    @property
    def local_at_global_back(self):
        return self.__orientation_mapping[GLOBAL_BACK]

    def __str__(self):
        return self.__repr__()
        # return "\n".join(["{}".format("{:<12} : {}".format(face, self.__orientation_mapping[face])) for face in
        #                  GLOBAL_FACES]) + '\n'

    def __eq__(self, other):
        return self.__orientation_mapping == other.__orientation_mapping

    # def __repr__(self):
    #     return "{ " + " | ".join(["{}".format("{} : {}".format(
    #         shorten_face_name(face), shorten_face_name(self.__orientation_mapping[face]))) for face in
    #         GLOBAL_FACES]) + " }"
    def __repr__(self):
        return "{ " + " | ".join(["{}".format(self.__orientation_mapping[face].split()[1][0]) for face in
                                  GLOBAL_FACES]) + " }"

    def __hash__(self):
        return hash((self.local_at_global_top, self.local_at_global_right, self.local_at_global_front,
                     self.local_at_global_down, self.local_at_global_left, self.local_at_global_back))


def shorten_face_name(face_name):
    return ''.join(part[0] for part in face_name.split(' '))


def orient_mesh(mesh_data, rotation, translation):
    """
    Rotate and translate the given mesh according to given rotation and position.
    :param mesh_data:   Mesh to rotate and translate
    :param rotation:    Rotation in degrees per axis - (x_deg, y_deg, z_deg)
    :param translation: Translation in grid units per axis - (x_shift, y_shift, z_shift)
    """

    # Rotate mesh into correct orientation using 3 rotations, around axis x, y, and z
    for i, axis in enumerate([[1, 0, 0], [0, -1, 0], [0, 0, 1]]):
        mesh_data.rotate(axis, np.radians(rotation[i]))

    # Translate to correct position. Translations happens from center of the mesh's mass to the objects location
    for i, translation_obj in enumerate([mesh_data.x, mesh_data.y, mesh_data.z]):
        translation_obj += translation[i]


def transform_mesh(mesh_data, rotation, translation):  # NOT TESTED!!!
    matrix = np.zeros((4, 4))
    matrix[0:3, 0:3] = np.diag(np.deg2rad(rotation))
    matrix[0:3, 3] = np.array((translation))
    matrix[3, 3] = 1
    mesh_data.transform(matrix)
