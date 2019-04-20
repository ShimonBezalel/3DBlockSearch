

class Physics:
    def is_stable(self, block_state, new_block):
        """
        Boolean function that returns if the new block to be places in the
        scheme of the current block state will stand, or topple.
        :param block_state: A list of blocks
        :param new_block: potential block to add, organized in a dictionary with keys as levels and values list of blocks
                        level -> [block1, block2, ...]
        :return: True iff the new arrangement still stands
        """
        level = new_block.get_level()
        relevant_cells = new_block.get_cells()


    def calculate_supports(self, block, blocks):
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
        pass





