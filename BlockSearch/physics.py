from BlockSearch.block import Block
from typing import List, Set, Dict, Tuple, Optional

X = 0
Y = 1
Z = 2

class Physics:

    @staticmethod
    def is_stable(block_state: Dict[int, Block], new_block : Block):
        """
        Boolean function that calculates if the new block to be places in the
        scheme of the current block state will stand, or topple.
        :param block_state: A list of blocks
        :param new_block: potential block to add, organized in a dictionary with keys as levels and values list of blocks
                        level -> [block1, block2, ...]
        :return: True iff the new arrangement still stands
        """
        level = new_block.get_bottom_level()
        # The first level sits on an infinite stable ground and needs no further calculation
        if level == 1:
            return True

        # Initiate the support block list if necessary (genuinely new block)
        support_blocks: List[Block] = new_block.get_supports()
        if support_blocks == None:
            new_block.set_supports(Physics.calculate_supports(new_block, block_state[level - 1]))
            support_blocks = new_block.get_supports()

        # Empty set means block is floating in air
        if support_blocks != []:
            center_x, center_y, center_z = new_block.get_cog()
            for i, block1 in enumerate(support_blocks):
                for j, block2 in enumerate(support_blocks[i:]):
                    # If the center of gravity falls above a theoretically supported cell of two support blocks,
                    # then *all* these blocks support the new block, and we must recalculate each center of gravity for
                    # further recursive stability calculations.
                    if (center_x, center_y) in block1.get_spread(block2):
                        stable = True
                        for block in support_blocks:
                            # Recursively shift gravities and recalculate stability
                            block.shift_cog([new_block])
                            stable &= Physics.is_stable(block_state, block)
                            if not stable:
                                return False
                        # Found that this new block sits on solid ground and shifted centers of gravity do not
                        # hurt stability
                        return True


        return False



    @staticmethod
    def calculate_supports(block : Block, blocks : List[Block]):
        """
        Calculated which of a given list of blocks are strictly under this given sample block.
        :param block: a single block with a level L
        :param blocks: A list of blocks, all level L-1

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
        supports = []

        cells = block.get_cells()
        for cell in cells:
            for potential_support in blocks:
                # Check is this cell is above under a cell from another block
                if (cell[X], cell[Y]) in ((c[X], c[Y]) for c in potential_support.get_cells()):
                    supports.append(potential_support)
        return supports






