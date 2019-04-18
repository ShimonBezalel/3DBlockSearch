
class Grid:

    def __init__(self):
        pass

    def add_move(self, move):
        """
        Apply the given move to self.
        This method modifies this grid object.

        :param move:    Move object to apply to this grid.
        """
        #TODO
        pass

    def new_grid_after_move(self, move):
        """
        Return a copy of this grid after the given move was applied to it.
        This method does NOT modify this grid object.

        :param move:    Move object to apply to the copied grid.
        :return:        A copy of this grid, with the given move applied to it.
        """
        #TODO
        pass

    def get_possible_moves(self):
        """
        Returns a list of all the moves possible on the current grid.
        :return:        List of moves possible on this grid.
        """
        #TODO
        pass

    def check_move_valid(self, move):
        """
        Return True if the given move can be legally applied to this grid,
        otherwise return False.

        :param move:    Move object to try applying to this grid.
        :return:        True if move possible, otherwise False.
        """
        #TODO
        pass

    def get_cell_at_position(self, x, y, z):
        """
        Return the cell object at coordinates (x,y,z)

        :param x:   Cell's X coordinate.
        :param y:   Cell's Y coordinate.
        :param z:   Cell's Z coordinate.
        :return:    Cell object at given coordinates.
        """
        #TODO
        pass

    def __eq__(self, other):
        """
        Check if this grid is identical to other.
        :param other:   Grid object to check if identical.
        :return:        True if grids contain the same pieces at the same
                        orientations and positions, otherwise False.
        """
        #TODO
        pass

    def __hash__(self):
        """
        Return a lightweight, hashed representation of this grid.
        :return: Lightweight, hashed representation of this grid.
        """
        #TODO
        pass

    def __str__(self):
        """
        Return a string describing this grid.
        :return: String describing this grid.
        """
        #TODO
        pass

    def __copy__(self):
        """
        Return a copy object of this grid, descend into pieces etc.
        The returned object should:
            * Have the same __hash__ as ours
            * Not point to or modify any of our internal objects, ever.
        :return:
        """
        #TODO
        pass


class Move:
    """
    A Move describes how one of the players is going to spend their move.

    It contains:
    - Piece: the ID of the piece being used
    - x/y: the center coordinates of the piece [0-19)
    - Rotation: how many times the piece should be rotated CW [0-3]
    - Flip: whether the piece should be flipped (True/False)
    """

    def __init__(self, piece, piece_index, orientation, x=0, y=0):
        self.piece = piece
        self.piece_index = piece_index
        self.x = x
        self.y = y
        self.orientation = orientation

    def __str__(self):
        out_str = [[' ' for _ in range(5)] for _ in range(5)]
        for (x, y) in self.orientation:
            out_str[x][y] = '0'
        out_str = '\n'.join(
            [''.join([x_pos for x_pos in out_str[y_val]])
             for y_val in range(5)]
        )
        return ''.join(out_str) + "x: " + str(self.x) + " y: " + str(self.y)
