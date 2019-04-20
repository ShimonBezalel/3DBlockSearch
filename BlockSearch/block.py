from BlockSearch.piece import Piece
import math
import numpy as np
from stl import mesh
from typing import List, Set, Dict, Tuple, Optional


X = 0
Y = 1
Z = 2

ORIENTATIONS = {
    (0, 0, 0),
    (90, 0, 0),
    (0, 0, 90),
    (90, 0, 90),
    (90, 90, 0),
    (0, 90, 0)
}

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

    def __init__(self, shape : mesh.Mesh, orientation, position):
        assert orientation in ORIENTATIONS
        super().__init__(shape, orientation, position)
        self._init_shape()
        self._init_cog()
        self._init_cells()
        self._init_levels()
        self._shifted_cog = self._cog
        self.num_of_suportees = 0
        self.supporting_me = None
        self.supported_by_me = None


    def get_supports(self):
        """
        Returns a list of the blocks placed strictly under this block, which are supporting it
        :return: An empty list if no blocks are defined.
        """
        return self.supporting_me

    def set_supports(self, blocks):
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
        self.supporting_me = blocks

    def get_cog(self):
        """
        Returns this blocks center of gravity as a point
        :return:
        """
        return self._cog

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
        return self.get_cells() & other.get_cells() != {}
        # for cell in self._cells:
        #     for other_cell in other.get_cells():
        #         if cell == other_cell:
        #             return True
        # return False

    def shift_cog(self, block):
        """
        Moves the shifted center of gravity for this block, influenced by blocks placed above it recursively.
        :param block:
        :return:
        """
        assert self._cog == self._shifted_cog
        average_cog = np.average((block.get_cog(), self._cog))
        #todo complete

    # @staticmethod
    # def memoize(f):
    #     memo = {}
    #
    #     def helper(x):
    #         if x not in memo:
    #             memo[x] = f(x)
    #         return memo[x]
    #
    #     return helper

    # TODO: @memoize
    def get_spread(self, other: 'Block'):
        """
        Retrieves the space between two blocks that can support blocks above, should their center of gravity
        sit within them.
        :param other:
        :return:
        """
        assert self._top_level == other.get_top_level()

        my_cover_x =    {cell[X] for cell in self.get_cover_cells()}
        other_cover_x = {cell[X] for cell in other.get_cover_cells()}

        my_cover_y =    {cell[Y] for cell in self.get_cover_cells()}
        other_cover_y = {cell[Y] for cell in other.get_cover_cells()}

        inter_x = my_cover_x & other_cover_x
        inter_y = my_cover_y & other_cover_y

        spread = set()
        if (inter_x):
            union_y = my_cover_y | other_cover_y
            min_y = min(union_y)
            max_y = max(union_y)
            for y in range(min_y, max_y + 1):
                for x in inter_x:
                    spread.add((x, y))

        elif (inter_y):
            union_x = my_cover_x | other_cover_x
            min_x = min(union_x)
            max_x = max(union_x)
            for x in range(min_x, max_x + 1):
                for y in inter_y:
                    spread.add((x, y))

        assert (inter_x or inter_y)
        return spread

    def get_bottom_level(self) -> float:
        """
        Return the lowest level this block sits in. Anything under this level supports this block

        """
        return self._bottom_level

    def get_top_level(self) -> float:
        """
        Return the highest level this block sits in. Anything above this level can be supported by this block.

        """
        return self._top_level

    def get_cover_cells(self) -> Set[Tuple[float, float]]:
        """
        :return: Return a set of 2D cells on XY plane covered by this block
        """
        return self._cover_cells

    def get_cells(self) -> Set[Tuple[float, float, float]]:
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
        # Set of all the cells contained within this block
        self._cells = set()

        # Set of theoretical cells with only X and Y, that are this blocks footprint
        self._cover_cells = set()
        for x in range(-Block.SHAPE_IN_CELLS[X], Block.SHAPE_IN_CELLS[X]):
            for y in range(-Block.SHAPE_IN_CELLS[Y], Block.SHAPE_IN_CELLS[Y]):
                for z in range(-Block.SHAPE_IN_CELLS[Z], Block.SHAPE_IN_CELLS[Z]):
                    self._cells.add((self._cog[X] / 2 + x, self._cog[Y] / 2 + y, self._cog[Z] / 2 + z))
                self._cover_cells.add((self._cog[X] / 2 + x, self._cog[Y] / 2 + y))

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

        self._bottom_level  = min_z
        self._top_level     = max_z

    def _init_cog(self):
        _, self._cog, _ = self.rendered_mesh.get_mass_properties()

    def _init_shape(self):
        """
            X X X X X X X X X X X X X X X
            X X X X X X X X X X X X X X X       =>              NO CHANGE
            X X X X X X X X X X X X X X X

        :return:
        """

        if self.orientation == (0, 0, 0):
            return
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
        if self.orientation == (90, 0, 0):
            self.SHAPE_IN_CELLS = (self.SHAPE_IN_CELLS[X], self.SHAPE_IN_CELLS[Z], self.SHAPE_IN_CELLS[Y] )
            return


        """       
            X X X X X X X X X X X X X X X                           X
            X X X X X X X X X X X X X X X       =>                  X  
            X X X X X X X X X X X X X X X                           X

                      z                                            
                      ^                                            
                       -> y                                            
        """
        if self.orientation == (0, 0, 90):
            self.SHAPE_IN_CELLS = (self.SHAPE_IN_CELLS[Y], self.SHAPE_IN_CELLS[X], self.SHAPE_IN_CELLS[Z])
            return

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
        if self.orientation == (90, 0, 90):
            self.SHAPE_IN_CELLS = (self.SHAPE_IN_CELLS[Z], self.SHAPE_IN_CELLS[X], self.SHAPE_IN_CELLS[Y] )
            return

        """       
            X X X X X X X X X X X X X X X                           
            X X X X X X X X X X X X X X X       =>                  X X X  
            X X X X X X X X X X X X X X X                           

                      z                                            
                      ^                                            
                       -> y                                            
        """
        if self.orientation == (90, 90, 0):
            self.SHAPE_IN_CELLS = (self.SHAPE_IN_CELLS[Y], self.SHAPE_IN_CELLS[Z], self.SHAPE_IN_CELLS[X])
            return


        """   
        
            
            X X X X X X X X X X X X X X X                           
            X X X X X X X X X X X X X X X       =>                X X X X X X X X X X X X X X X
            X X X X X X X X X X X X X X X                           

                      z                                            
                      ^                                            
                       -> y                                            
        """
        if self.orientation == (0, 90, 0):
            self.SHAPE_IN_CELLS = (self.SHAPE_IN_CELLS[Z], self.SHAPE_IN_CELLS[Y], self.SHAPE_IN_CELLS[X])
            return

    def __str__(self):
        cells = list(self._cells)
        cells.sort()
        st = "Block:\n["
        for cell in cells:
            st += "\t({},{},{}), ".format(cell[X], cell[Y], cell[Z])
        st += "]"

        return st

