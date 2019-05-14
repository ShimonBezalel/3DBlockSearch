from copy import deepcopy
from enum import Enum
from random import shuffle
from pprint import pprint as pp
from memoized import memoized
# from BlockSearch.piece import Piece
import math
import numpy as np
from stl import mesh
from typing import List, Set, Dict, Tuple, Optional, Generator
from BlockSearch.render import display, display_multiple_grids, display_colored

X = 0
Y = 1
Z = 2

COG = 1

DEBUG = True

class ORIENTATION(Enum):
    SHORT_WIDE    = (0, 0, 0),
    TALL_WIDE     = (90, 0, 0),
    SHORT_THIN    = (0, 0, 90),
    TALL_THIN     = (90, 0, 90),
    FLAT_THIN     = (90, 90, 0),
    FLAT_WIDE     = (0, 90, 0)

ORIENTATIONS = {
    'short_wide'    : (0, 0, 0),
    'tall_wide'     : (90, 0, 0),
    'short_thin'    : (0, 0, 90),
    'tall_thin'     : (90, 0, 90),
    'flat_thin'     : (90, 90, 0),
    'flat_wide'     : (0, 90, 0)
}
ORIENTATION_LAYING = {
    ORIENTATION.SHORT_THIN.value[0],
    ORIENTATION.FLAT_THIN.value[0],
    ORIENTATION.FLAT_WIDE.value[0],
    ORIENTATION.SHORT_WIDE.value[0]
}
ORIENTATION_STANDING = {
    ORIENTATION.TALL_THIN.value[0],
    ORIENTATION.TALL_WIDE.value[0]
}

block_mesh = mesh.Mesh.from_file('kapla.stl')

COVER_THRESHOLD = 0.4

@memoized
def init_rotated_mesh(arg):
    orientation = arg
    new_mesh = deepcopy(block_mesh)
    # Rotate mesh into correct orientation using 3 rotations, around axis x, y, and z
    for i, axis in enumerate([[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        new_mesh.rotate(axis, math.radians(orientation[i]))
    return new_mesh

class Block (Piece):
    """
    Shape of KAPLA piece, proportionally, in number of cells in each direction. Before rotation.


                      z                                 z
    Font View         ^ -> y         |   Right View     ^ -> x
    ---------------------------------|----------------
                                     |
    X X X X X X X X X X X X X X X    |       X
    X X X X X X X X X X X X X X X    |       X
    X X X X X X X X X X X X X X X    |       X

    (Width, Height, Length) or (X, Y, Z)
    Actual widths are twice as wide!
    """
    SHAPE_IN_CELLS = (1, 15, 3)


    def __init__(self):
        """
        Used as copy constructor
        """
        # super().__init__()
        self.orientation = None
        self.position = None
        self._rendered_mesh = None
        self._saturated = False
        self._temp_above        = set()
        self._str: str        = "Block N/A"
        self.position           = (-10, -10, -10)
        self._spreads_memory    = set()
        self.orientation        = (0, 0, 0)
        self._rendered_mesh      = mesh.Mesh([])
        self._original_shape    = mesh.Mesh([])
        self._quick_data : np.ndarray  = np.array([])
        self._memoized_aggregate = mesh.Mesh([])
        self._aggregate_cog     = None
        self._repr              = "Block N/A"

    def __init__(self, shape : mesh.Mesh, orientation : tuple or str or ORIENTATION, position):
        assert (orientation in ORIENTATIONS or orientation in ORIENTATIONS.values() or type(orientation) == ORIENTATION)
        if type(orientation) == str:
            orientation = ORIENTATIONS[orientation]

        elif type(orientation) == ORIENTATION:
            orientation = orientation.value[0]
        # todo: reuse rotation matrix!! can reduce init time by 30%

        super().__init__(shape, orientation, position)
        self.orientation = orientation
        self.position = position
        self._rendered_mesh = shape
        self._saturated = False
        self._rendered_mesh = deepcopy(init_rotated_mesh(orientation))
        self._init_translation()
        self._original_shape = shape
        self._spreads_memory = dict()
        self._temp_above     = set()
        self._init_shape()
        self._init_cog()
        self._init_cells()
        self._init_levels()
        self._blocks_below_me   = set()
        self._block_above_me    = set()
        self._memoized_aggregate = None
        self._quick_data = np.array(np.concatenate((self.orientation, self.position)), dtype=np.int16)
        self._str = Block.gen_str((orientation, position))
        self._repr = self._get_repr()

        self._h = self._quick_data.__hash__

    def _init_translation(self):
        # Translate to correct position. Translations happens from center of the mesh's mass to the objects location
        for i, translation_obj in enumerate([self._rendered_mesh.x, self._rendered_mesh.y, self._rendered_mesh.z]):
            translation_obj += self.position[i]

    def get_cog(self):
        """
        Returns this blocks center of gravity as a point
        :return:
        """
        return self._cog

    def get_aggregate_cog(self, state):
        """
        Returns the center of gravity for all the blocks above this (recursively), included this block
        :param state:
        :return:
        """
        if self._aggregate_cog is None:
            self.get_aggregate_mesh(state)
        return self._aggregate_cog

    def is_perpendicular(self, other: 'Block' or Tuple[int, int, int] or str):
        """
        Returns if this block is perpendicular to a given block, in some axis
        :param other: a block
        :return: True iff these two blocks are not have parallel orientations on the XY plane
        """
        other = ORIENTATIONS[other] if type(other) == str else other
        other_orientation = other.orientation if type(other) == Block else other
        if self.orientation in ORIENTATION_STANDING:
            return other_orientation in ORIENTATION_LAYING
        else: #  self.orientation in ORIENTATION_LAYING ...
            return other_orientation in ORIENTATION_STANDING

    def is_overlapping(self, other : 'Block'):
        """
        Returns true if these two blocks occupy the same place, meaning a least one of thier cells sit in the same location.
        :param other: A seperate block to check
        :return:
        """
        # todo: improve time!
        return (self.get_cells() & other.get_cells()) != set()

    def get_bottom_level(self) -> int:
        """
        Return the lowest level this block sits in. Anything under this level supports this block

        """
        return self._bottom_level

    def get_top_level(self) -> int:
        """
        Return the highest level this block sits in. Anything above this level can be supported by this block.

        """
        return self._top_level

    def get_cover_cells(self) -> Set[Tuple[int, int]]:
        """
        :return: Return a set of 2D cells on XY plane covered by this block
        """
        return self._cover_cells

    def get_cells(self) -> Set[Tuple[int, int, int]]:
        return self._cells

    def _init_cells(self):
        """

        :return:
        """
        #TODO: convert cells to np array
        # Set of all the cells contained within this block
        self._cells = set()
        # self._cells = np.array
        # Set of theoretical cells with only X and Y, that are this blocks footprint
        self._cover_cells = set()
        cog = tuple(int(i) for i in self.get_cog())

        half_depth = self.SHAPE_IN_CELLS[X] // 2
        half_width = self.SHAPE_IN_CELLS[Y] // 2
        half_height = self.SHAPE_IN_CELLS[Z] // 2

        for x in range(-half_depth, half_depth + 1):
            for y in range(-half_width, half_width + 1):
                for z in range(-half_height, half_height + 1):
                    self._cells.add((cog[X] + x, cog[Y] + y, cog[Z] + z))
                self._cover_cells.add((cog[X] + x, cog[Y] + y))

    def _init_levels(self):
        """
        Returns the level (Z height off ground) of the lowest cell in the block

        Standing orientation                   |    Horizontal Orientation
       ----------------------------------------|---------------------------------------------------------------
        Top Level ->        X    X X           |
                            X    X X           |
                            X    X X           |
                            X    X X           |                               Top Level ->       X X X X X
        Bottom Level ->     X    X X           |    B.Level ->    X X X X X                       X X X X X

        """

        min_z = np.inf
        max_z = -np.inf
        for cell in self._cells:
            if cell[Z] > max_z:
                max_z = cell[Z]
            if cell[Z] < min_z:
                min_z = cell[Z]
        assert min_z < np.inf
        assert max_z > -np.inf
        assert max_z >= min_z

        self._bottom_level  = int(min_z)
        self._top_level     = int(max_z)

    def _init_cog(self):
        self._cog               = np.array(self.position)
        self._aggregate_cog       = None  # force to be calculated

    def _init_shape(self):
        self.SHAPE_IN_CELLS = Block.orient_cells(self.orientation)

    @staticmethod
    def orient_cells(orientation):
        """
            X X X X X X X X X X X X X X X
            X X X X X X X X X X X X X X X       =>              NO CHANGE
            X X X X X X X X X X X X X X X

        """
        new_orientation = []
        if orientation == (0, 0, 0):
            new_orientation = Block.SHAPE_IN_CELLS

        """
                                                                    X X X
                                                                    X X X
            X X X X X X X X X X X X X X X                           X X X
            X X X X X X X X X X X X X X X       =>                  X X X
            X X X X X X X X X X X X X X X                           X X X
                                                                    X X X    
                      z                                             X X X    
                      ^                                             X X X
                       -> y                                         X X X    
        """
        if orientation == (90, 0, 0):
            new_orientation = (Block.SHAPE_IN_CELLS[X], Block.SHAPE_IN_CELLS[Z], Block.SHAPE_IN_CELLS[Y] )


        """       
            X X X X X X X X X X X X X X X                           X
            X X X X X X X X X X X X X X X       =>                  X  
            X X X X X X X X X X X X X X X                           X

                      z                                            
                      ^                                            
                       -> y                                            
        """
        if orientation == (0, 0, 90):
            new_orientation = (Block.SHAPE_IN_CELLS[Y], Block.SHAPE_IN_CELLS[X], Block.SHAPE_IN_CELLS[Z])

        """
                                                                    X
                                                                    X 
            X X X X X X X X X X X X X X X                           X 
            X X X X X X X X X X X X X X X       =>                  X 
            X X X X X X X X X X X X X X X                           X 
                                                                    X    
                      z                                             X    
                      ^                                             X 
                       -> y                                         X     
        """
        if orientation == (90, 0, 90):
            new_orientation = (Block.SHAPE_IN_CELLS[Z], Block.SHAPE_IN_CELLS[X], Block.SHAPE_IN_CELLS[Y] )

        """       
            X X X X X X X X X X X X X X X                           
            X X X X X X X X X X X X X X X       =>                  X X X  
            X X X X X X X X X X X X X X X                           

                      z                                            
                      ^                                            
                       -> y                                            
        """
        if orientation == (90, 90, 0):
            new_orientation = (Block.SHAPE_IN_CELLS[Y], Block.SHAPE_IN_CELLS[Z], Block.SHAPE_IN_CELLS[X])


        """   
        
            
            X X X X X X X X X X X X X X X                           
            X X X X X X X X X X X X X X X       =>                X X X X X X X X X X X X X X X
            X X X X X X X X X X X X X X X                           

                      z                                            
                      ^                                            
                       -> y                                            
        """
        if orientation == (0, 90, 0):
            new_orientation = (Block.SHAPE_IN_CELLS[Z], Block.SHAPE_IN_CELLS[Y], Block.SHAPE_IN_CELLS[X])

        return new_orientation

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str
        return self._repr

    def __hash__(self):
        return self._str.__hash__()

    def __eq__(self, other: 'Block'):
        return str(other) == str(self)

    def __lt__ (self, other: 'Block'):
        return str(self) < str(other)

    def __gt__(self, other: 'Block'):
        return str(self) > str(other)

    def __copy__(self):
        #TODO: can be made to go faster with some fancy copying
        return self
        # b = Block(self._original_shape, self.orientation, self.position)
        b = Block()
        b.render_mesh      = self._rendered_mesh
        b._original_shape  = self._original_shape
        b._spreads_memory  = self._spreads_memory
        b.SHAPE_IN_CELLS   = self.SHAPE_IN_CELLS
        b._cog             = self._cog
        b._memoized_aggregate = np.copy(self._memoized_aggregate)
        b._cells           = self._cells
        b._cover_cells     = self._cover_cells
        b._init_levels()

        # The following needs to be updated later by a larger scale block containing object
        b._block_above_me  = self._block_above_me
        b._blocks_below_me = self._blocks_below_me

        # A clean slate is created of block. This block is not responsible of recreating its tree of connectivity.
        #
        #   Responsibilities left over:
        #       blocks above
        #       blocks below
        #       spread neighbors
        #
        # The aggregate mesh can be innitiated

        return b

    def _set_spread(self, neighbor : 'Block', spread : Set):
        """
        Set the inner memory of spreads between object to save on later calculations
        :param neighbor: the block finished with calculating spread
        :param spread: the spread set calcualted
        """
        assert (neighbor not in self._spreads_memory)
        self._spreads_memory[neighbor] = spread

    def get_aggregate_mesh(self, state):
        """
        Returns a mesh of this object and everything above it.
        :return:
        """
        if self._memoized_aggregate:
            return self._memoized_aggregate
        data = self.get_aggregate_data(state)
        aggregate = mesh.Mesh(np.concatenate([m.data for m in data]))
        self._memoized_aggregate = aggregate
        mp = self._memoized_aggregate.get_mass_properties()
        # if mp[0] != 45:
        #     pp(mp)
        self._aggregate_cog = mp[COG]
        self._repr = "U" + self._get_repr()
        return aggregate

    def get_aggregate_data(self, state):
        data = [self._rendered_mesh]
        if state.get_blocks_above(self):
            for block in state.get_blocks_above(self):
                data.extend(block.get_aggregate_data(state))
        return data

    #TODO can memoize block who caused this reset
    # @memoized
    def reset_aggregate_mesh(self, state) -> None:
        """
        Signal to self to update the aggregate mesh of all blocks below me. Some change must have occurred above
        :return:
        """
        self._memoized_aggregate = None
        self._aggregate_cog      = None
        for block in state.get_blocks_below(self):
            block.reset_aggregate_mesh(state)

    def is_saturated(self, tower_state, no_changes=False):
        if self._saturated:
            return True
        else:
            # Refer to blocks directly above me and see if they fill a percentage of my cover space
            blocks_above = tower_state.get_blocks_above(self)
            cover_above_me = set()
            #perform set intersection for all blocks above me
            for block in blocks_above:
                cover_above_me  |= block._cover_cells
            covering_me = self._cover_cells & cover_above_me
            if len(covering_me) / len(self._cover_cells) > COVER_THRESHOLD:
                if no_changes:
                    return True
                self._saturated = True
            return self._saturated

    def gen_possible_block_descriptors(self, limit_orientation=lambda o: True, limit_len=60000, random_order=None) -> Generator[tuple, None, None]:
        """
        Generates a (orientation, position) map of possible sons of this block. A son is any block which can sit
        directly above this block, even if unstable.
        :param limit_orientation: function to limit the number of orientations that become sons.
                                    default behavior is no limitations
        :return:
        """
        if self._saturated:
            return
        i = 0
        seen_blocks = set()
        new_level = self.get_top_level() + 1
        cover_cells = list(self.get_cover_cells())
        if random_order:
            shuffle(cover_cells)
        for cell in cover_cells:
            relevant_keys = list(filter(limit_orientation, ORIENTATIONS.keys()))
            if random_order:
                shuffle(relevant_keys)
            for orientation in relevant_keys:
                if 'flat' in orientation:
                    offset = 0
                elif 'short' in orientation:
                    offset = 1
                elif 'tall' in orientation:
                    offset = 7
                else:
                    # should not reach a case with none recognizable orientation
                    raise AssertionError
                z = new_level + offset
                cell_orientation = Block.orient_cells(ORIENTATIONS[orientation])
                half_depth = cell_orientation[X] // 2
                half_width = cell_orientation[Y] // 2
                xrange = list(range(-half_depth + cell[X], (half_depth + 1) + cell[X]))
                yrange = list(range(-half_width + cell[Y], (half_width + 1) + cell[Y]))
                if random_order:
                    shuffle(xrange)
                    shuffle(yrange)
                for x in xrange:
                    for y in yrange:
                        if x == self._cog[X] or y == self._cog[Y]:
                            continue
                        candidate = (ORIENTATIONS[orientation], (x, y, z))
                        if candidate not in seen_blocks:
                            yield candidate
                            i += 1
                            if i >= limit_len:
                                return
                            if self._saturated:
                                return
                        seen_blocks.add(candidate)

    def _get_repr(self) -> str:
        """
        Heavier calculation of repr, do be done less often, only upon changes to COG.
        """
        if self._aggregate_cog is not None:
            return "Block: O{}, P{}, A_COG{}".format(str(self.orientation),
                                                     str(self.position),
                                                     str(tuple(self._aggregate_cog.astype(np.int))))
        return "Block: O{}, P{}, A_COG(N/A)".format(str(self.orientation),
                                                 str(self.position))

    @staticmethod
    def gen_str(descriptor) -> str:
        """
        publicly assailable block string from descriptor
        """
        orientation, position = descriptor
        return "Block: O{}, P{}".format(str(orientation), str(position))

    def render(self):
        """
        Draw the piece
        :return: A mesh oriented and positioned in 3D space
        """
        return self._rendered_mesh


class RingFloor(Block):
    def __init__(self, floor_mesh, size=30, ring_size=15, number_of_rings=1, distance_between_rings=10):
        self.SHAPE_IN_CELLS = (size, size, 1)
        self._size = size
        self._ring_size = ring_size
        self._number_of_rings = number_of_rings
        self._distance_between_rings = distance_between_rings
        self._str = "Ring Floor: size {}".format(size)

        super().__init__(shape=floor_mesh, orientation=(0, 0, 0 ), position=(0, 0, 0 ))
        self._rendered_mesh = floor_mesh

    def get_size(self):
        return self._size

    def _init_cells(self):
        #TODO: convert cells to np array
        # Set of all the cells contained within this block
        self._cells = set()
        # self._cells = np.array
        # Set of theoretical cells with only X and Y, that are this blocks footprint
        self._cover_cells = set()
        cog = tuple(int(i) for i in self.get_cog())

        half_depth = self._size // 2
        half_width = self._size // 2
        half_height = 0

        ring_distances = set()
        for i, l in enumerate(range(self._size//4, self._size, self._distance_between_rings)):
            ring_distances |= set(range(l - math.floor(self._ring_size / 2.0), l + math.ceil(self._ring_size / 2.0)))
            if i >= self._number_of_rings:
                break
        print(ring_distances)

        for x in range(-half_depth, half_depth + 1):
            for y in range(-half_width, half_width + 1):
                for z in range(-half_height, half_height + 1):
                    posish = (x, y, z)
                    dist = np.linalg.norm((posish, (0, 0, 0)))
                    # if dist >= self._size / 2 - 3 and dist <= self._size / 2:
                    if math.floor(dist) in ring_distances or math.ceil(dist) in ring_distances:
                        self._cells.add((cog[X] + x, cog[Y] + y, cog[Z] + z))
                        self._cover_cells.add((cog[X] + x, cog[Y] + y))

    def __repr__(self):
        return self._str

class Floor(Block):

    def __init__(self, floor_mesh, size=30):
        super().__init__(shape=floor_mesh, orientation=(0, 0, 0 ), position=(0, 0, 0 ))
        self.SHAPE_IN_CELLS = (size, size, 1)
        self._rendered_mesh = floor_mesh
        self._size = size
        self._init_cells()
        self._init_levels()
        self._str = "Floor: size {}".format(size)

    def get_size(self):
        return self._size

    def __repr__(self):
        return self._str





