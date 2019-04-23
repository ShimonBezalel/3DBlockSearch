import numpy as np

from matplotlib import pyplot
from mpl_toolkits import mplot3d
from stl import mesh

GRID_UNIT_IN_MM = 20


class Voxel:
    def __init__(self, is_target=False):
        self.is_target = is_target
        self.hubs = [None, None]


class Grid:
    I = 0
    J = 1
    W = 2

    def __init__(self, targets):
        """
        Initialize a 3D grid with given target coordinates
        :param targets: array of size 3*n of n targets by coordinates
                        [[t1_i, t1_j, t1_w],
                         [t2_i, t2_j, t2_w],
                         ...
                         [tn_i, tn_j, tn_w]]
        """

        # Verify targets were given as a list (even if single)
        assert hasattr(targets, '__iter__'), "targets must come as a list"

        self.targets = targets
        mins, maxs = np.min(targets, axis=0), np.max(targets, axis=0)
        i_min, i_max = mins[Grid.I], maxs[Grid.I]
        j_min, j_max = mins[Grid.J], maxs[Grid.J]
        w_min, w_max = mins[Grid.W], maxs[Grid.W]
        self._grid = np.zeros(shape=(i_max - i_min, j_max - j_min, w_max - w_min), dtype=Voxel)
        self._mins = mins

        # Init grid with empty voxels
        for i in range(i_max - i_min):
            for j in range(j_max - j_min):
                for w in range(w_max - w_min):
                    self._grid[i, j, w] = Voxel()

        # Init targets
        for target in targets:
            target_voxel = self.get_voxel_at_coords(target)
            if not target_voxel:
                self.set_voxel_at_coords(target, Voxel(is_target=True))
            else:
                target_voxel.is_target = True

    def get_targets_meshes(self):

        # Create cube mesh for each target
        cubes = []

        for target in self.targets:
            # Create 3 faces of a cube
            data = np.zeros(6, dtype=mesh.Mesh.dtype)

            # Top of the cube
            data['vectors'][0] = np.array([[0, 1, 1],
                                           [1, 0, 1],
                                           [0, 0, 1]])
            data['vectors'][1] = np.array([[1, 0, 1],
                                           [0, 1, 1],
                                           [1, 1, 1]])
            # Front face
            data['vectors'][2] = np.array([[1, 0, 0],
                                           [1, 0, 1],
                                           [1, 1, 0]])
            data['vectors'][3] = np.array([[1, 1, 1],
                                           [1, 0, 1],
                                           [1, 1, 0]])
            # Left face
            data['vectors'][4] = np.array([[0, 0, 0],
                                           [1, 0, 0],
                                           [1, 0, 1]])
            data['vectors'][5] = np.array([[0, 0, 0],
                                           [0, 0, 1],
                                           [1, 0, 1]])
            # Center cube on grid
            data['vectors'] -= 0.5

            # Generate 2 different meshes so we can rotate them later
            meshes = [mesh.Mesh(data.copy()) for _ in range(2)]

            # meshes[0] is the original half-cube
            # meshes[1] is rotated to the opposite hald-cube
            meshes[1].rotate([0, 1, 0], np.deg2rad(180))
            meshes[1].rotate([0, 0, 1], np.deg2rad(90))

            cube = mesh.Mesh(np.concatenate([m.data for m in meshes]))

            # Scale faces
            cube.data['vectors'] *= GRID_UNIT_IN_MM

            # Scale coordinates
            target_coords = np.array(target) * GRID_UNIT_IN_MM * 1.5
            cube.data['vectors'] += target_coords

            cubes.append(cube)
            # return the merged mesh-cube

        return cubes

    def get_voxel_at_coords(self, coordinates):
        """
        Get the voxel at the given coordinates
        :param coordinates: tuple (i,j,w)
        :return: Voxel at the given coordinates on the grid
        """
        shifted_coords = tuple(coordinates - self._mins - 1)
        return self._grid[shifted_coords]  # convert imaginary boundaries to start at (0,0,0)

    def set_voxel_at_coords(self, coordinates, voxel):
        """
        Set the voxel at the given coordinates to the given voxel
        :param coordinates: tuple (i,j,w)
        :param voxel: Voxel to set at given coordinates
        """
        shifted_coords = tuple(coordinates - self._mins - 1)
        self._grid[shifted_coords] = voxel

    def add_move(self, move):
        """
        Apply the given move to self.
        This method modifies this grid object.

        :param move:    Move object to apply to this grid.
        """
        # TODO
        pass

    def new_grid_after_move(self, move):
        """
        Return a copy of this grid after the given move was applied to it.
        This method does NOT modify this grid object.

        :param move:    Move object to apply to the copied grid.
        :return:        A copy of this grid, with the given move applied to it.
        """
        # TODO
        pass

    def get_possible_moves(self):
        """
        Returns a list of all the moves possible on the current grid.
        :return:        List of moves possible on this grid.
        """
        # TODO
        pass

    def check_move_valid(self, move):
        """
        Return True if the given move can be legally applied to this grid,
        otherwise return False.

        :param move:    Move object to try applying to this grid.
        :return:        True if move possible, otherwise False.
        """
        # TODO
        pass

    def get_voxel_at_position(self, x, y, z):
        """
        Return the voxel object at coordinates (x,y,z)

        :param x:   Voxel's X coordinate.
        :param y:   Voxel's Y coordinate.
        :param z:   Voxel's Z coordinate.
        :return:    Voxel object at given coordinates.
        """
        # TODO
        pass

    def __eq__(self, other):
        """
        Check if this grid is identical to other.
        :param other:   Grid object to check if identical.
        :return:        True if grids contain the same pieces at the same
                        orientations and positions, otherwise False.
        """
        # TODO
        pass

    def __hash__(self):
        """
        Return a lightweight, hashed representation of this grid.
        :return: Lightweight, hashed representation of this grid.
        """
        # TODO
        pass

    def __str__(self):
        """
        Return a string describing this grid.
        :return: String describing this grid.
        """
        # TODO
        pass

    def __copy__(self):
        """
        Return a copy object of this grid, descend into pieces etc.
        The returned object should:
            * Have the same __hash__ as ours
            * Not point to or modify any of our internal objects, ever.
        :return:
        """
        # TODO
        pass

    def render(self):
        """
        Renders all the pieces on the grid.
        :return:
        """
        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        # Render all pieces
        for piece in self.pieces:
            mesh = piece.get_mesh()
            axes.add_collection(mplot3d.art3d.Poly3DCollection(mesh.vectors))

        # Auto scale to mesh size
        scale = numpy.concatenat([piece.points for piece in self.pieces]).flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()
