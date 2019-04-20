

class Physics:
    def isStable(self, block_state, new_block):
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



