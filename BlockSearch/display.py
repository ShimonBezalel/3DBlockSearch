import numpy

from matplotlib import pyplot
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Aliasing
np = numpy
plt = pyplot

# Constants
X = 0
Y = 1
Z = 2


new_color       = (0, 0, 1)
emphasis_color  = (1, 0, 0)
matte_color     = (0.8, 0.8, 0.8)

def display(meshes):
    # Optionally render the rotated cube faces
    # from matplotlib import pyplot
    # from mpl_toolkits import mplot3d

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Render the cube faces
    for i, m in enumerate(meshes):
        # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))
        i += 1
        mesh = Poly3DCollection(m.vectors, alpha=0.70)
        face_color = [(0.5 * i) % 1, (0.3 * i) % 1, (0.7 * i) % 1]
        mesh.set_facecolor(face_color)
        mesh.set_edgecolor('black')

        axes.add_collection3d(mesh)

    # Auto scale to the mesh size
    scale = numpy.concatenate([m.points for m in meshes]).flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()

def display_cells( cells ):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


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

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markers = [".", ",", "o", "v", "^", "<", ">", "1", "2" ]
    for i, cells in enumerate(cells_list):
        color = colors[i % len(colors)]
        marker = markers[i % len(markers)]
        xs = [cell[X] for cell in cells]
        ys = [cell[Y] for cell in cells]


        ax.scatter(xs, ys, c=color, marker=marker)

    ax.set_xlabel('X ')
    ax.set_ylabel('Y ')

    plt.show()


def display_colored(meshes, colors, centers=None):

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Render the cube faces
    for i, m in enumerate(meshes):
        # i += 1
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
    pyplot.show()

def display_board(board_state : dict, support_blocks : list, new_block):
    blocks = []
    for block_list in board_state.values():
        blocks += list(filter(lambda b: b not in support_blocks + [new_block], block_list))
    meshes = [b.render() for b in blocks] + [b.render() for b in support_blocks] + [new_block.render()]
    cogs = [b.get_aggregate_cog() for b in blocks] + [b.get_aggregate_cog() for b in support_blocks] + [new_block.get_aggregate_cog()]
    colors = ([matte_color] * len(blocks)) + ([emphasis_color] * len(support_blocks)) + [new_color]
    display_colored(meshes, colors, cogs)

