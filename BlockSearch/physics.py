import math
import numpy as np
from memoized import memoized

from stl import mesh

from BlockSearch.block          import Block
from typing                     import List, Set, Dict, Tuple, Optional
from BlockSearch.display        import display_board
from BlockSearch.tower_state    import Tower_State

X = 0
Y = 1
Z = 2


DEBUG = False

FLOOR_LEVEL = 0

def is_stable(tower_state: Tower_State, new_block : Block):
    """
    Boolean recursive function that calculates if the new block to be places in the
    scheme of the current block state will stand, or topple.
    :param tower_state: A state of the block tower.
    :param new_block: potential block to add, organized in a dictionary with keys as levels and values list of blocks
                    level -> [block1, block2, ...]
    :return: True iff the new arrangement still stands
    """
    bottom_level = new_block.get_bottom_level()
    block_state = tower_state.get_blocks_by_top_level()

    # Initiate the relation to surrounding blocks in the tower
    if (bottom_level - 1) in block_state:
        new_block.set_blocks_below(calculate_below(new_block, block_state[bottom_level - 1]))
    new_block.set_blocks_above(calculate_above(new_block, block_state))

    # Clean up changes made downwards in the block tower
    for block in new_block.get_blocks_below():
        old = block.get_blocks_above()
        old.add(new_block)
        block.set_blocks_above(old)

        # Todo: choose one of the following recursive strategies.
        block.reset_aggregate_mesh()
        # block.update_aggregate_mesh(new_block.render())

    # memoized_helper = memoize(is_stable_helper)
    # return memoized_helper(tower_state, new_block)
    return is_stable_helper((tower_state, new_block))

# def memoize(f):
#     memo = {}
#
#     def helper(arg1, arg2):
#         x = hash(str(arg1) + str(arg2))
#         if x not in memo:
#             print("{} : found new x: {}".format(len(memo), x))
#             memo[x] = f(arg1, arg2)
#         return memo[x]
#
#     return helper

# def is_stable_helper(tower_state: Tower_State, new_block: Block):


@memoized
def is_stable_helper(arg):
    tower_state, new_block = arg
    bottom_level = new_block.get_bottom_level()
    # top_level = new_block.get_top_level()
    block_state = tower_state.get_blocks_by_top_level()

    # The first level sits on an infinite stable ground and needs no further calculation
    if bottom_level == FLOOR_LEVEL:
        if DEBUG:
            display_board(block_state, [], new_block)

        return True

    # Initiate the support block list. Assumed to exist
    blocks_below: Set[Block] = new_block.get_blocks_below()
    blocks_above: Set[Block] = new_block.get_blocks_above()

    if DEBUG:
        display_board(block_state, list(blocks_below), new_block)

    # Empty set means block is floating in air. This is considered a bug in case new blocks
    # are only spawned off others
    assert blocks_below
    if blocks_below != []:

        # The aggregate center of gravity will take into consideration any support from above
        center_x, center_y, center_z = new_block.get_aggregate_cog()

        # We iterate twice over to compare within every two combinations of blocks, without order being important
        for i, block1 in enumerate(blocks_below):
            for block2 in list(blocks_below)[i:]:

                # If the center of gravity falls above a theoretically supported cell of two support blocks,
                # then *all* these blocks support the new block, and we must recalculate each center of gravity for
                # further recursive stability calculations.

                # COG's can have floating point values not alligned with the grid, we therefore check the four cells
                # borders.
                COG_candidates = [(math.floor(center_x), math.floor(center_y)),
                                  (math.floor(center_x), math.ceil(center_y)),
                                  (math.ceil(center_x), math.floor(center_y)),
                                  (math.ceil(center_x), math.ceil(center_y))]

                # At least one pair of support blocks is enough
                supported = False
                for cog in COG_candidates:
                    supported |= cog in block1.get_spread(block2)

                if supported:

                    # Now that we know this block's center of gravity sits above at least two blocks's spread
                    # Recursively continue stability check downwards
                    for block in blocks_below:
                        supported &= is_stable_helper((tower_state, block))
                        # One unstable block below (recursively) is enough to disqualify this block
                        if not supported:
                            return False
                    # Found that this new block sits on solid ground and shifted centers of gravity do not
                    # hurt stability
                    return True

    return False


def calculate_below(block : Block, blocks : List[Block]) -> Set[Block]:
    """
    Calculated which of a given list of blocks are strictly under this given sample block.
    :param block: a single block with a bottom level L
    :param blocks: A list of blocks, all top level L-1

    X - Segment of initial block
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

    :return: A list of 1 or more blocks that are strictly under the given block,
            or an empty list if no such blocks exist
    """
    supports = set()

    cells = block.get_cover_cells()
    for potential_support in blocks:
        for cell in cells:
            # Check if this cell is above under a cell from another block
            if cell in potential_support.get_cover_cells():
                supports.add(potential_support)
                break
    return supports

def calculate_above(block : Block, block_state : Tower_State or dict[int : List[Block]]) -> Set[Block]:
    """
    Calculated which of a given blocks are strictly above this given sample block.
    :param block: a single block with a bottom level L
    :param block_state: A full dictionary of blocks organized by thier top levels

    X - Segment of initial block
    A - Above (Suportee) blocks
    N - Non above blocks

                    Front View      |            Side View     |          Top View
                    ----------------------------------------------------------------------
                        AAAAAA      |                A         |      NNNNNN
                    N    X   N      |       NNNNNN XXXXXX      |
                                    |                          |                A
                                    |                          |              XXAXXX
                                    |                          |                A
                                    |                          |              NNANNN

    :return: A list of 1 or more blocks that are strictly above the given block,
            or an empty list if no such blocks exist
    """
    supported = set()

    cover_cells = block.get_cover_cells()
    relevant_levels = filter(lambda level: level > block.get_top_level(), block_state.keys())
    for level in relevant_levels:
        for candidate in block_state[level]:
            # If this candidate block sits one level above our block's top level, it may be directly above as well
            if candidate.get_bottom_level() - block.get_top_level() == 1:
                for cell in cover_cells:
                    # Check if this cell is below a cell from another candidate block
                    if cell in candidate.get_cover_cells():
                        supported.add(candidate)
                        break
    return supported

def combine(meshes):
    return mesh.Mesh(np.concatenate([m.data for m in meshes]))

# class Physics:
#     FLOOR_LEVEL = 0
#     # def is_stable(block_state: Dict[float or int, List[Block]], new_block : Block):
#
#     @staticmethod
#     def is_stable(tower_state: Tower_State, new_block : Block):
#         """
#         Boolean recursive function that calculates if the new block to be places in the
#         scheme of the current block state will stand, or topple.
#         :param tower_state: A state of the block tower.
#         :param new_block: potential block to add, organized in a dictionary with keys as levels and values list of blocks
#                         level -> [block1, block2, ...]
#         :return: True iff the new arrangement still stands
#         """
#         bottom_level = new_block.get_bottom_level()
#         block_state = tower_state.get_blocks_by_top_level()
#
#         # Initiate the relation to surrounding blocks in the tower
#         if (bottom_level - 1) in block_state:
#             new_block.set_blocks_below(Physics.calculate_below(new_block, block_state[bottom_level - 1]))
#         new_block.set_blocks_above(Physics.calculate_above(new_block, block_state))
#
#         # Clean up changes made downwards in the block tower
#         for block in new_block.get_blocks_below():
#             old = block.get_blocks_above()
#             old.add(new_block)
#             block.set_blocks_above(old)
#
#             # Todo: choose one of the following recursive stradegies.
#             # block.reset_aggregate_mesh()
#             block.update_aggregate_mesh(new_block.render())
#
#         memoized_helper = Physics.memoize(Physics.is_stable_helper)
#         return memoized_helper(tower_state, new_block)
#         # return Physics.is_stable_helper(block_state, new_block)
#
#     @staticmethod
#     def memoize(f):
#         memo = {}
#
#         def helper(arg1, arg2):
#             x = (arg1, arg2)
#             if x not in memo:
#                 memo[x] = f(arg1, arg2)
#             return memo[x]
#
#         return helper
#
#
#     @staticmethod
#     def is_stable_helper(tower_state: Tower_State, new_block: Block):
#         bottom_level = new_block.get_bottom_level()
#         # top_level = new_block.get_top_level()
#         block_state = tower_state.get_blocks_by_top_level()
#
#         # The first level sits on an infinite stable ground and needs no further calculation
#         if bottom_level == Physics.FLOOR_LEVEL:
#             if DEBUG:
#                 display_board(block_state, [], new_block)
#
#             return True
#
#         # Initiate the support block list. Assumed to exist
#         blocks_below: Set[Block] = new_block.get_blocks_below()
#         blocks_above: Set[Block] = new_block.get_blocks_above()
#
#         if DEBUG:
#             display_board(block_state, list(blocks_below), new_block)
#
#         # Empty set means block is floating in air. This is considered a bug in case new blocks
#         # are only spawned off others
#         # assert blocks_below
#         if blocks_below != []:
#
#             # The aggregate center of gravity will take into consideration any support from above
#             center_x, center_y, center_z = new_block.get_aggregate_cog()
#
#             # We iterate twice over to compare within every two combinations of blocks, without order being important
#             for i, block1 in enumerate(blocks_below):
#                 for block2 in list(blocks_below)[i:]:
#
#                     # If the center of gravity falls above a theoretically supported cell of two support blocks,
#                     # then *all* these blocks support the new block, and we must recalculate each center of gravity for
#                     # further recursive stability calculations.
#
#                     # COG's can have floating point values not alligned with the grid, we therefore check the four cells
#                     # borders.
#                     COG_candidates = [(math.floor(center_x), math.floor(center_y)),
#                                       (math.floor(center_x), math.ceil(center_y)),
#                                       (math.ceil(center_x), math.floor(center_y)),
#                                       (math.ceil(center_x), math.ceil(center_y))]
#
#                     # At least one pair of support blocks is enough
#                     supported = False
#                     for cog in COG_candidates:
#                         supported |= cog in block1.get_spread(block2)
#
#                     if supported:
#
#                         # Now that we know this block's center of gravity sits above at least two blocks's spread
#                         # Recursively continue stability check downwards
#                         for block in blocks_below:
#                             supported &= Physics.is_stable_helper(tower_state, block)
#                             # One unstable block below (recursively) is enough to disqualify this block
#                             if not supported:
#                                 return False
#                         # Found that this new block sits on solid ground and shifted centers of gravity do not
#                         # hurt stability
#                         return True
#
#         return False
#
#
#
#     @staticmethod
#     def calculate_below(block : Block, blocks : List[Block]) -> Set[Block]:
#         """
#         Calculated which of a given list of blocks are strictly under this given sample block.
#         :param block: a single block with a bottom level L
#         :param blocks: A list of blocks, all top level L-1
#
#         X - Segment of initial block
#         S - Support blocks
#         N - Non support blocks
#
#                         Front View      |            Side View     |          Top View
#                         ----------------------------------------------------------------------
#                             XXXXXX      |                X         |      NNNNNN
#                         N    S   S      |       NNNNNN SSSSSS      |
#                                         |                          |                X
#                                         |                          |              SSXSSS
#                                         |                          |                X
#                                         |                          |              SSXSSS
#
#         :return: A list of 1 or more blocks that are strictly under the given block,
#                 or an empty list if no such blocks exist
#         """
#         supports = set()
#
#         cells = block.get_cover_cells()
#         for potential_support in blocks:
#             for cell in cells:
#                 # Check if this cell is above under a cell from another block
#                 if cell in potential_support.get_cover_cells():
#                     supports.add(potential_support)
#                     break
#         return supports
#
#     @staticmethod
#     def calculate_above(block, block_state) -> Set[Block]:
#         """
#         Calculated which of a given blocks are strictly above this given sample block.
#         :param block: a single block with a bottom level L
#         :param block_state: A full dictionary of blocks organized by thier top levels
#
#         X - Segment of initial block
#         A - Above (Suportee) blocks
#         N - Non above blocks
#
#                         Front View      |            Side View     |          Top View
#                         ----------------------------------------------------------------------
#                             AAAAAA      |                A         |      NNNNNN
#                         N    X   N      |       NNNNNN XXXXXX      |
#                                         |                          |                A
#                                         |                          |              XXAXXX
#                                         |                          |                A
#                                         |                          |              NNANNN
#
#         :return: A list of 1 or more blocks that are strictly above the given block,
#                 or an empty list if no such blocks exist
#         """
#         supported = set()
#
#         cover_cells = block.get_cover_cells()
#         relevant_levels = filter(lambda level: level > block.get_top_level(), block_state.keys())
#         for level in relevant_levels:
#             for candidate in block_state[level]:
#                 # If this candidate block sits one level above our block's top level, it may be directly above as well
#                 if candidate.get_bottom_level() - block.get_top_level() == 1:
#                     for cell in cover_cells:
#                         # Check if this cell is below a cell from another candidate block
#                         if cell in candidate.get_cover_cells():
#                             supported.add(candidate)
#                         break
#         return supported
#
#     @staticmethod
#     def combine(meshes):
#         return mesh.Mesh(np.concatenate([m.data for m in meshes]))


def is_overlapping(block_tower : Tower_State, new_block : Block):
    """
    Check if new block clashes (physically overlaps) with the rest of the block tower
    :param block_tower: A tower state
    :param new_block: either a new object or just it's string representation
    :return:
    """
    #todo: if we implement this step elsewhere, before creating the object, then erase this
    if block_tower.is_bad_block(new_block):
        return True

    bottom_level : int = new_block.get_bottom_level()
    top_level    : int = new_block.get_top_level()
    blocks_by_top_level = block_tower.get_blocks_by_top_level()
    """
    Only scan blocks with top levels above my bottom level.
    X - Block. B - Bottom layer. T - Top layer
    
                        XXXXXXX          
    new block           XXXXXXX         others  TTTTTTTT     others
                        BBBBBBB           in    XXXXXXXX       out
                                                                        TTTT
                                                                        XXXX
    
    """
    for level in filter(lambda l: l >= bottom_level, blocks_by_top_level.keys()):
        for other_block in blocks_by_top_level[level]:
            """
            Diqualify for overlap any block with a bottom above our top
            X - Block. B - Bottom layer. T - Top layer

                                            others  XXXXXXXX      others    XXXXX
                                              in    XXXXXXXX       out      BBBBB
                                TTTTTTT             BBBBBBBB
            new block           XXXXXXX               
                                XXXXXXX           


            """
            if other_block.get_bottom_level() <= top_level and other_block.is_overlapping(new_block):
                # perform a memoization of bad blocks we've seen
                block_tower.add_bad_block(new_block)
                return True
    return False