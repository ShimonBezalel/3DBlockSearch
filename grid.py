
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

    def get_voxel_at_position(self, x, y, z):
        """
        Return the voxel object at coordinates (x,y,z)

        :param x:   Voxel's X coordinate.
        :param y:   Voxel's Y coordinate.
        :param z:   Voxel's Z coordinate.
        :return:    Voxel object at given coordinates.
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

    def display(self):
        """
        Display this board nicely
        """
        # Optionally render the rotated cube faces
        # from matplotlib import pyplot
        # from mpl_toolkits import mplot3d

        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        # Render the cube faces
        for m in meshes:
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))

        # Auto scale to the mesh size
        scale = numpy.concatenate([m.points for m in meshes]).flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()
