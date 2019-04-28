import time
import uuid
import os
import numpy
import numpy as np

from matplotlib import pyplot
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh

ORIENTATIONS = {
    'short_wide'    : (0, 0, 0),
    'tall_wide'     : (90, 0, 0),
    'short_thin'    : (0, 0, 90),
    'tall_thin'     : (90, 0, 90),
    'flat_thin'     : (90, 90, 0),
    'flat_wide'     : (0, 90, 0)
}

# Aliasing
plt = pyplot

# Constants
X = 0
Y = 1
Z = 2


new_color       = (0, 0, 1)
emphasis_color  = (1, 0, 0)
matte_color     = (0.8, 0.8, 0.8)

GRID = False  #True # on

def save(meshes, subfolder="default", subfolders=None):
    if subfolders:
        for mesh, second in zip(meshes, subfolders):
            mesh.save(os.path.join("saved_stls", subfolder, second, str(uuid.uuid4())) + ".stl")
    else:
        for mesh in meshes:
            mesh.save(os.path.join("saved_stls", subfolder, str(uuid.uuid4())) +  ".stl")

def combine(meshes):
    return mesh.Mesh(np.concatenate([m.data for m in meshes]))

def save_by_orientation(tower_state, subfolder="default", seperate_orientations=True):
    by_orientation = []
    order = []
    for key, orientation in ORIENTATIONS.items():
        order.append(key)
        meshes = [b.render() for b in filter(lambda b: b.orientation == orientation, tower_state.gen_blocks())]
        if meshes:
            single_mesh = combine(meshes)
            by_orientation.append(single_mesh)

    subfolders = order if seperate_orientations else None

    save(by_orientation, subfolder, subfolders)

def save_by_orientation_blocks(blocks, subfolder="default", seperate_orientations=True):
    by_orientation = []
    order = []
    for key, orientation in ORIENTATIONS.items():
        order.append(key)
        meshes = [b.render() for b in filter(lambda b: b.orientation == orientation, blocks)]
        if meshes:
            single_mesh = combine(meshes)
            by_orientation.append(single_mesh)

    subfolders = order if seperate_orientations else None

    save(by_orientation, subfolder, subfolders=subfolders)


def display(meshes, scale=None, to_file=False, file_name="BlockSearch/plots/default.png", auto_close=False):
    # Optionally render the rotated cube faces
    # from matplotlib import pyplot
    # from mpl_toolkits import mplot3d

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    if not GRID:
        hide_grid(axes)

    if scale:
        axes.set_xlim(-scale, scale)
        axes.set_ylim(-scale, scale)
        axes.set_zlim(0, 2*scale)

    # Render the cube faces
    for i, m in enumerate(meshes):
        # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))
        i += 1
        mesh = Poly3DCollection(m.vectors, alpha=0.70)
        face_color = [(0.7 * i) % 1, (0.5 * i) % 1, (0.3 * i) % 1]
        mesh.set_facecolor(face_color)
        mesh.set_edgecolor('black')

        axes.add_collection3d(mesh)

    # Auto scale to the mesh size
    scale = numpy.concatenate([m.points for m in meshes]).flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    if to_file:
        pyplot.savefig(file_name, orientation='portrait')
    else:
        if not auto_close:
            pyplot.show()
        else:
            assert False, "Not implemented"
            # import os
            # def info(title):
            #     print(title)
            #     print ('module name:', __name__)
            #     if hasattr(os, 'getppid'):  # only available on Unix
            #         print('parent process:', os.getppid())
            #     print('process id:', os.getpid())
            #
            # def close_after( sec=5):
            #     info("close after")
            #     time.sleep(sec)
            #     plt.close('all')
            #
            # def open_immidiately(plot=pyplot):
            #     info("open_immidiately")
            #     plt.show()
            #
            #
            # p1 = multiprocessing.Process(name="closes window", target=close_after)
            # p2 = multiprocessing.Process(name="shows window", target=open_immidiately)
            # p1.start()
            # p2.start()
            # p1.join()
            # p2.join()
            # # open_immidiately()

def display_cells( cells ):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if not GRID:
        hide_grid(ax)


    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    # for color, marker, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    color, marker = ('r', 'o')
    xs = [cell[X] for cell in cells]
    ys = [cell[Y] for cell in cells]
    zs = [cell[Z] for cell in cells]


    ax.scatter(xs, ys, zs, c=color, marker=marker)

    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')
    ax.set_zlabel('Z ')

    plt.show()

def display_multiple_cells(cells_list, scale = 50):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if not GRID:
        hide_grid(ax)

    plt.xlim(-scale, scale)
    plt.ylim(-scale, scale)
    # force scaling in z axis
    ax.scatter([0, 0], [0, 0], [-scale, scale], c='w', marker='.')

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markers = [".", ",", "o", "v", "^", "<", ">", "1", "2" ]
    for i, cells in enumerate(cells_list):
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        xs = [cell[X] for cell in cells]
        ys = [cell[Y] for cell in cells]
        zs = [cell[Z] for cell in cells]


        ax.scatter(xs, ys, zs, c=color, marker=marker)

    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')
    ax.set_zlabel('Z ')

    plt.show()

def display_multiple_grids(cells_list, scale=50):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.xlim(-scale, scale)
    plt.ylim(-scale, scale)

    if not GRID:
        hide_grid(ax)

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markers = [".", ",", "o", "v", "^", "<", ">", "1", "2" ]
    if type(cells_list) == np.ndarray:
        xs = cells_list[..., X]
        ys = cells_list[..., Y]
        ax.scatter(xs, ys)

    else:
        for i, cells in enumerate(cells_list):
            color = colors[i % len(colors)]
            marker = markers[i % len(markers)]
            xs = [cell[X] for cell in cells]
            ys = [cell[Y] for cell in cells]


            ax.scatter(xs, ys, c=color, marker=marker)

    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')

    plt.show()


def display_colored(meshes, colors, centers=None, scale=None, to_file=False, file_name="BlockSearch/plots/default.png"):

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    if scale:
        axes.set_xlim(-scale, scale)
        axes.set_ylim(-scale, scale)
        axes.set_zlim(0, 2*scale)

    if not GRID:
        hide_grid(axes)

    # Render the cube faces
    for i, m in enumerate(meshes):
        mesh = Poly3DCollection(m.vectors, alpha=0.70)
        mesh.set_facecolor(colors[i])
        mesh.set_edgecolor('black')

        axes.add_collection3d(mesh)

    if centers:
        xs = [c[X] for c in centers]
        ys = [c[Y] for c in centers]
        zs = [c[Z] for c in centers]

        axes.scatter(xs, ys, zs, c='black', marker='v')
        axes.scatter(xs, ys, [-3]*len(xs), c=colors, marker='^')

    # Auto scale to the mesh size
    scale = numpy.concatenate([m.points for m in meshes]).flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    if to_file:
        pyplot.savefig(file_name, orientation='portrait', quality=100, dpi=300)
    else:
        pyplot.show()

def display_board(board_state : dict, support_blocks : list, new_block):
    blocks = []
    for block_list in board_state.values():
        blocks += list(filter(lambda b: b not in support_blocks + [new_block], block_list))
    meshes = [b.render() for b in blocks] + [b.render() for b in support_blocks] + [new_block.render()]
    cogs = [b.get_aggregate_cog() for b in blocks] + [b.get_aggregate_cog() for b in support_blocks] + [
        new_block.get_aggregate_cog()]
    colors = ([matte_color] * len(blocks)) + ([emphasis_color] * len(support_blocks)) + [new_color]
    display_colored(meshes, colors, cogs)

def hide_grid(ax):
    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.set_zticks([])

