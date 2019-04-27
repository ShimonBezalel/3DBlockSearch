from copy import copy, deepcopy

from stl import mesh

from display import display_meshes_with_colors_and_alphas
from orientation import orient_mesh
from voxel import Voxel

GRID_UNIT_IN_MM = 20
GRID_UNIT_WITH_SPACING = 1.5 * GRID_UNIT_IN_MM


class Grid:

    def __init__(self, targets=((0,0,0),)):
        """
        Initialize empty grid with targets given in coordinates
        :param targets: list of tuples [(ci1, cj1, cw1), ... ,(ciN, cjN, cwN)]
        """
        self._grid = dict()
        self.pieces = list()
        self.targets = targets
        for target in self.targets:
            pos = target.position
            if not (pos in self._grid):
                self._grid[pos] = Voxel(target=target)


    def remaining_targets(self):
        return [target for target in self.targets if not target.is_reached]


    def add_piece(self, piece):
        hubs = end1, center, end2 = piece.get_hubs()
        for hub in hubs:
            pos = tuple(hub.position)
            if not (pos in self._grid):
                self._grid[pos] = Voxel(hub1=hub)
            elif not self._grid[pos].is_full():
                self._grid[pos].add_hub(hub)
            else:
                raise AssertionError("Can't add piece to a full voxel at {}!".format(pos))
        self.pieces.append(piece)

    def can_add_piece(self, piece):
        for hub in piece.get_hubs():
            pos = tuple(hub.position)
            if not (pos in self._grid):
                # Empty voxel? good
                continue
            elif not self._grid[pos].is_full():
                # Can connect to other hub in the voxel?
                other = self._grid[pos].hub1
                if not hub.can_connect(other):
                    return False
            else:
                # Voxel is already full
                return False
        return True

    def display(self, meshes=None, colors=None, alphas=None, all_white=False, scale=None, filename=None):
        if not meshes:
            meshes = []
        else:
            meshes = copy(meshes)
        if not colors:
            colors = []
        else:
            colors = copy(colors)
        if not alphas:
            alphas = []
        else:
            alphas = copy(alphas)
        for piece in self.pieces:
            meshes.append(piece.get_mesh())
            if all_white:
                colors.append('white')
            else:
                colors.append(piece.color)
            alphas.append(piece.alpha)
            for hub in piece.get_hubs():
                meshes.append(hub.get_mesh())
                if all_white:
                    colors.append('white')
                else:
                    colors.append(hub.color)
                alphas.append(hub.alpha)
        for target in self.targets:
            meshes.append(target.get_mesh())
            colors.append(target.color)
            alphas.append(target.alpha)
        display_meshes_with_colors_and_alphas(meshes, colors, alphas, scale, filename)

    def display_with_candidate(self, candidate_piece, scale=None, filename=None):
        meshes = [candidate_piece.get_mesh(), ]
        color = 'green' if self.can_add_piece(candidate_piece) else 'red'
        colors = [color, ]
        alphas = [candidate_piece.alpha]
        self.display(meshes, colors, alphas, all_white=True, scale=scale, filename=filename)
