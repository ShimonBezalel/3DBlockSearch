from copy import copy, deepcopy

from matplotlib import pyplot
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh

from display import display_meshes_with_colors_and_alphas, np, plt
import piece
from target import Target
from voxel import Voxel

# Grid constants
GRID_UNIT_IN_MM = 20
GRID_UNIT_WITH_SPACING = 1.5 * GRID_UNIT_IN_MM

# Display constants
OPEN_HUB_COLOR = "#4455FF"
CURRENT_PIECE_COLOR = "#33FF11"
START_POS = 0
END_POS = 1
COLOR_POS = 2
X = 0
Y = 1
Z = 2


class Grid:

    def __init__(self, targets=(Target((0, 0, 0)),)):
        """
        Initialize empty grid with targets given in coordinates
        :param targets: list of tuples [(ci1, cj1, cw1), ... ,(ciN, cjN, cwN)]
        """
        self._grid = dict()
        self.pieces = list()
        self.targets = list()
        self.open_hubs = set()
        for target in targets:
            self.add_target(target)

        # Stuff for displaying max_mindist heuristic
        self.lines = None
        self.max_target = None
        self.labels = None

    def add_target(self, target: Target):
        pos = target.position
        if not (pos in self._grid):
            self._grid[pos] = Voxel(target=target)
        self.targets.append(target)

    def remaining_targets(self):
        return [target for target in self.targets if not target.is_reached]

    def add_piece(self, piece):
        hubs = end1, center, end2 = piece.get_hubs()
        for hub in hubs:
            pos = tuple(hub.position)
            if not (pos in self._grid):
                self._grid[pos] = Voxel()
            if not self._grid[pos].is_full():
                self._grid[pos].add_hub(hub)
                # The other hub in this voxel is no longer open
            if self._grid[pos].is_full():
                self.open_hubs.remove(self._grid[pos].hub1)
            else:
                self.open_hubs.add(hub)
        self.pieces.append(piece)

    def can_add_piece(self, piece):
        for hub in piece.get_hubs():
            pos = tuple(hub.position)
            if not (pos in self._grid) or (self._grid[pos].no_hubs()):
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

    def display(self, scale=100, filename=None, dirname=None, heur=None,
                cost=None, all_white=True):
        # Create a new plot
        fig = pyplot.figure()
        axes = mplot3d.Axes3D(fig)

        # Define plot scale
        if scale:
            axes.set_xlim(-scale, scale)
            axes.set_ylim(-scale, scale)
            axes.set_zlim(-scale, scale)
        else:
            raise AssertionError('you gave me no scale!!!!')

        # Collect meshes to render
        meshes = []
        colors = []
        alphas = []
        for piece in self.pieces[:-1]:
            meshes.append(piece.get_mesh())
            if all_white:
                colors.append('white')
            else:
                colors.append(piece.color)
            alphas.append(piece.alpha)
            for hub in piece.get_hubs():
                meshes.append(hub.get_mesh())
                if all_white:
                    if hub in self.open_hubs:
                        colors.append(OPEN_HUB_COLOR)
                    else:
                        colors.append('white')
                else:
                    colors.append(hub.color)
                alphas.append(hub.alpha)

        # Render last piece with special color
        if len(self.pieces) >= 1:
            piece = self.pieces[-1]
            meshes.append(piece.get_mesh())
            colors.append(CURRENT_PIECE_COLOR)
            alphas.append(piece.alpha)
            for hub in piece.get_hubs():
                meshes.append(hub.get_mesh())
                colors.append(CURRENT_PIECE_COLOR)
                alphas.append(hub.alpha)

        if self.max_target:
            self.max_target.highlight_on()
        for target in self.targets:
            meshes.append(target.get_mesh())
            colors.append(target.color)
            alphas.append(target.alpha)
        if self.max_target:
            self.max_target.highlight_off()

        # Render the cube faces
        for i, m in enumerate(meshes):
            # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))
            mesh = Poly3DCollection(m.vectors, alpha=alphas[i])
            face_color = colors[i]
            mesh.set_facecolor(face_color)
            mesh.set_edgecolor('black')
            axes.add_collection3d(mesh)

        if meshes:
            # Auto scale to the mesh size
            scale = np.concatenate([m.points for m in meshes]).flatten(-1)
            axes.auto_scale_xyz(scale, scale, scale)

        if self.lines:
            for line in self.lines:
                axes.plot([line[START_POS][X], line[END_POS][X]],
                          [line[START_POS][Y], line[END_POS][Y]],
                          zs=[line[START_POS][Z], line[END_POS][Z]], color=line[COLOR_POS])

        if self.labels:
            for label in self.labels:
                axes.text3D(label[X], label[Y], label[Z], label[-1])

        if not cost:
            cost = len(self.pieces)
        total_cost = (cost + heur) if ((cost) and (heur)) else None
        axes.text2D(0.05, 0.8, "GRID STATS \n"
                               "pieces     : {}\n"
                               "heuristic : {}\n"
                               "total       : {}\n".format(
            "{:.1f}".format(cost) if cost else 'NaN',
            "{:.1f}".format(heur) if heur else 'NaN',
            "{:.1f}".format(total_cost) if total_cost else 'NaN'), transform=axes.transAxes)
        # Save to file OR Show the plot to the screen
        if filename:
            pyplot.savefig(filename)
            print("saving {}...".format(filename))
        elif dirname:
            global count
            pyplot.savefig("{}/{}.png".format(dirname, count))
            count += 1
        else:
            plt.draw()
            plt.pause(0.2)
            # plt.close()

    # def display(self, meshes=None, colors=None, alphas=None, all_white=True, scale=100, filename=None, lines=None,
    #             labels=None, dirname=None):
    #     if not meshes:
    #         meshes = []
    #     else:
    #         meshes = copy(meshes)
    #     if not colors:
    #         colors = []
    #     else:
    #         colors = copy(colors)
    #     if not alphas:
    #         alphas = []
    #     else:
    #         alphas = copy(alphas)
    #     if not lines:
    #         lines = self.lines
    #     if not labels:
    #         labels = self.labels
    #     for piece in self.pieces[:-1]:
    #         meshes.append(piece.get_mesh())
    #         if all_white:
    #             colors.append('white')
    #         else:
    #             colors.append(piece.color)
    #         alphas.append(piece.alpha)
    #         for hub in piece.get_hubs():
    #             meshes.append(hub.get_mesh())
    #             if all_white:
    #                 if hub in self.open_hubs:
    #                     colors.append(OPEN_HUB_COLOR)
    #                 else:
    #                     colors.append('white')
    #             else:
    #                 colors.append(hub.color)
    #             alphas.append(hub.alpha)
    #     if len(self.pieces) > 1:
    #         piece = self.pieces[-1]
    #         meshes.append(piece.get_mesh())
    #         colors.append(CURRENT_PIECE_COLOR)
    #         alphas.append(piece.alpha)
    #         for hub in piece.get_hubs():
    #             meshes.append(hub.get_mesh())
    #             colors.append(CURRENT_PIECE_COLOR)
    #             alphas.append(hub.alpha)
    #     if self.max_target:
    #         self.max_target.highlight_on()
    #     for target in self.targets:
    #         meshes.append(target.get_mesh())
    #         colors.append(target.color)
    #         alphas.append(target.alpha)
    #     if self.max_target:
    #         self.max_target.highlight_off()
    #     display_meshes_with_colors_and_alphas(meshes, colors, alphas, scale=scale, filename=filename, lines=lines,
    #                                           labels=labels, dirname=dirname)

    def display_with_candidate(self, candidate_piece, scale=None, filename=None):
        meshes = [candidate_piece.get_mesh(), ]
        color = 'green' if self.can_add_piece(candidate_piece) else 'red'
        colors = [color, ]
        alphas = [candidate_piece.alpha]
        self.display(meshes, colors, alphas, all_white=True, scale=scale, filename=filename)

    def from_str(self, grid_str):
        self._grid = dict()
        self.pieces = list()
        self.targets = list()
        self.open_hubs = set()

        parsed = grid_str.split('=')
        targets_str = parsed[2][2:-2]  # drop '\n' at start and end
        targets = targets_str.split('\n*')
        for t_str in targets:
            target = Target()
            target.from_str(t_str)
            self.add_target(target)

        pieces_str = parsed[4]
        pieces = pieces_str.split('\n* ')[1:]
        for p_str in pieces:
            p = piece.Piece()
            p.from_str(p_str)
            self.add_piece(p)

        # Stuff for displaying max_mindist heuristic
        self.lines = None
        self.max_target = None
        self.labels = None

        # self.display()

    def __str__(self):
        sorted_pieces = sorted(self.pieces, key=lambda piece: (tuple(piece.position), str(piece.orientation)))
        sorted_targets = sorted(self.targets, key=lambda target: target.position)
        targets_str = ('* ' + "\n* ".join([str(target) for target in sorted_targets])) if self.targets else ''
        pieces_str = ('* ' + "\n* ".join([str(piece) for piece in sorted_pieces])) if self.pieces else ''
        return "=TARGETS=\n{}\n=PIECES=\n{}\n".format(targets_str, pieces_str)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))
