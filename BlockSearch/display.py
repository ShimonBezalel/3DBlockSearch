from time import sleep

import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random
plt = pyplot

DISPLAY = True

r = lambda: random.randint(0, 255)
random_color = lambda: '#%02X%02X%02X' % (r(), r(), r())

def display_parts(pieces):
    if not DISPLAY:
        return

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    meshes = []

    # Render the pieces and their hubs
    for i, piece in enumerate(pieces):
        i += 1

        # Render piece
        piece_mesh = piece.get_mesh()
        piece_poly3d = Poly3DCollection(piece_mesh.vectors, alpha=0.20)
        #piece_color = (0.8, 0.8, 0.8)  # [(0.5 * i) % 1, (0.3 * i) % 1, (0.7 * i) % 1]
        piece_color = (0.1, 0.1, 0.1)  # [(0.5 * i) % 1, (0.3 * i) % 1, (0.7 * i) % 1]
        piece_poly3d.set_facecolor(piece_color)
        piece_poly3d.set_edgecolor('grey')
        axes.add_collection3d(piece_poly3d)
        meshes.append(piece_mesh)

        # Render its hubs
        for j, hub in enumerate(piece.get_hubs()):
            hub_mesh = hub.get_mesh()
            hub_poly3d = Poly3DCollection(hub_mesh.vectors, alpha=0.70)
            hub_color = [(0.5 * (i + j)) % 1, (0.3 * (i + j)) % 1, (0.7 * (i + j)) % 1]
            hub_poly3d.set_facecolor(hub_color)
            hub_poly3d.set_edgecolor('black')
            axes.add_collection3d(hub_poly3d)
            meshes.append(hub_mesh)

    # Auto scale to the mesh size
    scale = np.concatenate([m.points for m in meshes]).flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()

def display_meshes_with_colors_and_alphas(meshes, corresponding_colors, corresponding_alphas, scale=None, filename=None):
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    if scale:
        #plt.xlim(-scale, scale)
        #plt.ylim(-scale, scale)
        axes.set_xlim(-scale, scale)
        axes.set_ylim(-scale, scale)
        axes.set_zlim(-scale, scale)
        #axes.scatter([0, 0], [0, 0], [-scale, scale], c='w', marker='.')
    else:
        raise AssertionError('you gave me no scale!!!!')

    # Render the cube faces
    for i, m in enumerate(meshes):
        # axes.add_collection3d(mplot3d.art3d.Poly3DCollection(m.vectors))
        mesh = Poly3DCollection(m.vectors, alpha=corresponding_alphas[i])
        face_color = corresponding_colors[i]
        mesh.set_facecolor(face_color)
        mesh.set_edgecolor('black')

        axes.add_collection3d(mesh)

    if meshes:
        # Auto scale to the mesh size
        scale = np.concatenate([m.points for m in meshes]).flatten(-1)
        axes.auto_scale_xyz(scale, scale, scale)

    if filename:
        pyplot.savefig(filename)
        print("saving {}...".format(filename))

    # Show the plot to the screen
    else:
        pyplot.show()


def display_meshes_with_colors(meshes, corresponding_colors):
    return display_meshes_with_colors_and_alphas(meshes, corresponding_colors, [0.70,] * len(corresponding_colors))

def display_meshes(meshes):
    colors = [((0.5 * i) % 1, (0.3 * i) % 1, (0.7 * i) % 1) for i in range(1,len(meshes)+1)]
    display_meshes_with_colors(meshes, colors)
