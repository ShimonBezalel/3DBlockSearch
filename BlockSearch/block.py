from copy import deepcopy
from enum import Enum
from random import shuffle

from memoized import memoized

from BlockSearch.piece import Piece
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
block_mesh = mesh.Mesh.from_file('kapla.stl')

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
        super().__init__()
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
        self._str = Block.get_str((orientation, position))
        self._repr = self._get_repr()

        self._h = self._quick_data.__hash__

    def _init_translation(self):
        # Translate to correct position. Translations happens from center of the mesh's mass to the objects location
        for i, translation_obj in enumerate([self._rendered_mesh.x, self._rendered_mesh.y, self._rendered_mesh.z]):
            translation_obj += self.position[i]


    def get_blocks_below(self) -> Set['Block']:
        """
        Returns a list of the blocks placed strictly under this block, which are supporting it
        :return: An empty list if no blocks are defined.
        """
        return self._blocks_below_me

    def set_blocks_below(self, blocks: Set['Block']):
        """
        Permanently links this block to a set of blocks strictly under it, which support it in the air.
        The scheme is assumed to be stable.

        X - Segment of this block
        S - Support blocks
        N - Non support blocks

                        Front View      |            Side View     |          Top View
                        ----------------------------------------------------------------------
                            XXXXXX      |                X         |      NNNNNN
                        N    S   S      |       NNNNNN SSSSSS      |
                                        |                          |                X
                                        |                          |              SSXSSS
                                        |                          |                X
                                        |                          |              SSXSSS

        :param blocks: A list of existing blocks to link as supports
        :return:
        """
        self._blocks_below_me = blocks

    def get_blocks_above(self) -> Set['Block']:
        return self._block_above_me

    def set_blocks_above(self, blocks : Set['Block']):
        self._block_above_me = blocks

    def get_cog(self):
        """
        Returns this blocks center of gravity as a point
        :return:
        """
        return self._cog

    def get_aggregate_cog(self):
        """
        Returns the center of gravity for all the blocks above this (recursively), included this block
        :return:
        """
        if self._aggregate_cog is None:
            self.get_aggregate_mesh()
        return self._aggregate_cog

    def is_perpendicular(self, other : Piece):
        """
        Returns if this block is perpendicular to a given block, in some axis
        :param other: a block
        :return: True iff these two blocks are not have parallel orientations on the XY plane
        """
        return self.orientation != other.orientation

    def is_overlapping(self, other : 'Block'):
        """
        Returns true if these two blocks occupy the same place, meaning a least one of thier cells sit in the same location.
        :param other: A seperate block to check
        :return:
        """
        # todo: improve time!
        return (self.get_cells() & other.get_cells()) != set()

    def get_spread(self, other: 'Block'):
        """
        Retrieves the space between two blocks that can support blocks above, should their center of gravity
        sit within them.

        Spread should only be calculated between blocks that have already been recognized as close enough to hold
        another block above them, otherwise behavior is not defined, or in the best case an assertion will fail.
        This is garenteed by only calling get_spread on blocks both directly under the same piece.
        :param other:
        :return:
        """
        assert self.get_top_level() == other.get_top_level()

        if other is self:
            return self.get_cover_cells()

        if other in self._spreads_memory:
            return self._spreads_memory[other]

        my_cover_x =    {cell[X] for cell in self.get_cover_cells()}
        other_cover_x = {cell[X] for cell in other.get_cover_cells()}

        my_cover_y =    {cell[Y] for cell in self.get_cover_cells()}
        other_cover_y = {cell[Y] for cell in other.get_cover_cells()}

        inter_x = my_cover_x & other_cover_x
        inter_y = my_cover_y & other_cover_y

        spread = set()
        if (inter_x):
            union_y = my_cover_y | other_cover_y
            min_y = int(min(union_y))
            max_y = int(max(union_y))
            for y in range(min_y, max_y + 1):
                for x in inter_x:
                    spread.add((x, y))

        elif (inter_y):
            union_x = my_cover_x | other_cover_x
            min_x = int(min(union_x))
            max_x = int(max(union_x))
            for x in range(min_x, max_x + 1):
                for y in inter_y:
                    spread.add((x, y))

        else: # no common pieces - skew lines
            """
                                                    X                   XXXXXXX
            XXXXXXX                                 X                               X
                                            or              X       or              X
                    XXXXXXXX                                X                       X
                        
            
            Relevant for flat pieces only.
            """
            pass
        spread |= self.get_cover_cells()
        spread |= other.get_cover_cells()
        candidate_blocks = self.get_blocks_above() & other.get_blocks_above()

        if candidate_blocks:
            flat_block = candidate_blocks.pop()
            # if DEBUG:
            #     display([self.render(), other.render(), flat_block.render()])
            # assert (flat_block.orientation in (ORIENTATIONS['flat_thin'], ORIENTATIONS['flat_wide']))
            center_x, center_y, _ = tuple(flat_block.get_cog())
            skew_center = set()
            for cell in spread:
                new_cell = ((cell[X] + center_x)//2, (cell[Y] + center_y)//2)
                skew_center.add(new_cell)
            spread |= skew_center
        self._spreads_memory[other] = spread
        other._set_spread(self, spread)
        return spread

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

    def is_placed(self) -> bool:
        """
        Returns true iff this block has been situated permanently in a block structure
        :return:
        """
        #todo: define what it means to be placed
        pass

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

        half_depth = self.SHAPE_IN_CELLS[X] // 2
        half_width = self.SHAPE_IN_CELLS[Y] // 2
        half_height = self.SHAPE_IN_CELLS[Z] // 2

        for x in range(-half_depth, half_depth + 1):
            for y in range(-half_width, half_width + 1):
                cog = tuple(int(i) for i in self.get_cog())
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
        return self._repr

    def __hash__(self):
        return self._str.__hash__()

    def __eq__(self, other : 'Block'):
        return other.__hash__() == self.__hash__()

    def __copy__(self):
        #TODO: can be made to go faster with some fancy copying
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

    def get_aggregate_mesh(self):
        """
        Returns a mesh of this object and everything above it.
        :return:
        """
        if self._memoized_aggregate:
            return self._memoized_aggregate
        data = self.get_aggregate_data()
        aggregate = mesh.Mesh(np.concatenate([m.data for m in data]))
        self._memoized_aggregate = aggregate
        self._aggregate_cog = self._memoized_aggregate.get_mass_properties()[COG]
        self._repr = "U" + self._get_repr()
        return aggregate

    def get_aggregate_data(self):
        data = [self._rendered_mesh]
        if self.get_blocks_above():
            for block in self.get_blocks_above():
                data.extend(block.get_aggregate_data())
        return data

    #TODO can memoize block who caused this reset
    # @memoized
    def reset_aggregate_mesh(self, catalyst : 'Block' = None) -> None:
        """
        Signal to self to update the aggregate mesh of all blocks below me. Some change must have occurred above
        :return:
        """
        self._memoized_aggregate = None
        self._aggregate_cog      = None
        for block in self.get_blocks_below():
            block.reset_aggregate_mesh()

    def update_aggregate_mesh(self, new_mesh) -> None:
        """
        Deprecated - 100 times slower than reset
        Signal to self to update the aggregate mesh of all blocks above me. Some change occurred above
        """
        meshes = [new_mesh]
        if self._memoized_aggregate:
            meshes += [self._memoized_aggregate]

        self._memoized_aggregate = mesh.Mesh(np.concatenate((new_mesh.data, self._memoized_aggregate.data)))
        self._aggregate_cog      = self._memoized_aggregate.get_mass_properties()[COG]
        self._repr               = self._get_repr()

        if self.get_blocks_below():
            for block in self.get_blocks_below():
                block.update_aggregate_mesh(new_mesh)

    def gen_possible_block_descriptors(self, limit_orientation=lambda o: True, limit_len=60000, random_order=None) -> Generator[tuple, None, None]:
        """
        Generates a (orientation, position) map of possible sons of this block. A son is any block which can sit
        directly above this block, even if unstable.
        :param limit_orientation: function to limit the number of orientations that become sons.
                                    default behavior is no limitations
        :return:
        """
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
                        candidate = (ORIENTATIONS[orientation], (x, y, z))
                        if candidate not in seen_blocks:
                            yield candidate
                            i += 1
                            if i >= limit_len:
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
    def get_str(descriptor) -> str:
        """
        publicly assailable block string from descriptor
        """
        orientation, position = descriptor
        return "Block: O{}, P{}".format(str(orientation), str(position))

    def confirm(self):
        """
        Make changes made by this block permanent
        :return:
        """
        pass

    def disconnect(self):
        """
        Undo changes possibly made by connect
        :return:
        """
        # Reset changes downwards in the block tower  (recursively)
        #           | | |
        #           V V V
        for neighbor_block in self.get_blocks_below():
            neighbor_block._block_above_me.remove(self)

            # resetting the cog's and aggregate meshes is expensive and may be redundant
            neighbor_block.reset_aggregate_mesh()

        # Reset changes upwards in the block tower  (1 level)
        #           ^ ^ ^
        #           | | |
        for neighbor_block in self.get_blocks_above():
            neighbor_block._blocks_below_me.remove(self)

    def connect(self):
        # Make changes downwards in the block tower  (recursively)
        #           | | |
        #           V V V
        for neighbor_block in self.get_blocks_below():
            neighbor_block._block_above_me.add(self)
            neighbor_block.reset_aggregate_mesh()

        # Make changes upwards in the block tower  (1 level)
        #           ^ ^ ^
        #           | | |
        for neighbor_block in self.get_blocks_above():
            neighbor_block._blocks_below_me.add(self)
        pass

    def render(self):
        """
        Draw the piece
        :return: A mesh oriented and positioned in 3D space
        """
        return self._rendered_mesh


class Floor(Block):

    def __init__(self, floor_mesh, size=30):
        super().__init__(shape=floor_mesh, orientation=(0, 0, 0 ), position=(0, 0, 0 ))
        self.SHAPE_IN_CELLS = (size, size, 1)
        self._init_cells()
        self._init_levels()
        self._str = "Floor: size {}".format(size)

    def __repr__(self):
        return self._str





