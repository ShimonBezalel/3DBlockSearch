from piece import Piece

class Block (Piece):

    def __init__(self):
        super().__init__()

    def get_supports(self):
        """
        Returns a list of the blocks placed strictly under this block, which are supporting it
        :return: An empty list if no blocks are defined.
        """
        pass

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
        pass

    def get_cog(self):
        """
        Returns this blocks center of gravity as a point
        :return:
        """
        pass
