from copy import copy, deepcopy

import numpy
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh
import math

from grid import GRID_UNIT_IN_MM, Grid
from piece import Piece  # , orient_mesh


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


def single_piece():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    return [Piece(hub_mesh, rotation, position), ]


def positioned_pieces():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    original = Piece(hub_mesh, rotation, position)
    x1 = Piece(hub_mesh, rotation, position + np.array((GRID_UNIT_IN_MM, 0, 0)))
    xm1 = Piece(hub_mesh, rotation, position + np.array((-1 * GRID_UNIT_IN_MM, 0, 0)))
    y1 = Piece(hub_mesh, rotation, position + np.array((0, GRID_UNIT_IN_MM, 0)))
    z1 = Piece(hub_mesh, rotation, position + np.array((0, 0, GRID_UNIT_IN_MM)))
    # rx1 = Piece(hub_mesh, rotation + (90, 0, 0), position)
    return [original, x1, xm1, y1, z1]


def rotated_pieces():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    original = Piece(hub_mesh, rotation, position)
    rx1 = Piece(hub_mesh, rotation + (90, 0, 0), position + np.array((GRID_UNIT_IN_MM, 0, 0)))
    ry1 = Piece(hub_mesh, rotation + (0, 90, 0), position + np.array((-1 * GRID_UNIT_IN_MM, 0, 0)))
    rz1 = Piece(hub_mesh, rotation + (0, 0, 90), position + np.array((2 * GRID_UNIT_IN_MM, 0, 0)))
    return [original, rx1, ry1, rz1]


def connected_pieces_center_1():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    original = Piece(hub_mesh, rotation, position)
    rx1 = Piece(hub_mesh, rotation + (90, 180, 0), position)
    return [original, rx1]


def connected_pieces_center_2():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    original = Piece(hub_mesh, rotation, position)
    rx1 = Piece(hub_mesh, rotation + (-90, 0, 180), position)
    return [original, rx1]


def connected_pieces_center_3():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    original = Piece(hub_mesh, rotation, position)
    rx1 = Piece(hub_mesh, (90, 90, 0), position)
    return [original, rx1]


def grid_pieces():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    pieces = []
    original = Piece(hub_mesh, rotation, position)
    for x in range(4):
        for y in range(4):
            for z in range(4):
                piece = Piece(hub_mesh, rotation + (90 * x, 90 * y, 90 * z), position + (120 * x, 120 * y, 120 * z))
                pieces.append(piece)
    return pieces


def sandbox_pieces():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((0, 0, 0))
    position = np.array((0, 0, 0))
    piece_list = [
        Piece(hub_mesh, rotation + np.array((90 * i, 90 * i, 90 * i)), position + np.array((10 * i, 10 * i, 10 * i)))
        for i in range(4)]
    return piece_list


def test_targets():
    grid = Grid([(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (1, 2, 3), ])
    t100 = grid.get_voxel_at_coords((1,0,0))
    t101 = grid.get_voxel_at_coords((1,0,1))
    tm100 = grid.get_voxel_at_coords((-1,0,0))
    print("Is (1,0,0) a target? {}".format(t100.is_target))
    print("Is (1,0,1) a target? {}".format(t101.is_target))
    print("Is (-1,0,0) a target? {}".format(tm100.is_target))
    return grid.get_targets_meshes()

def connectable_pieces():
    hub_mesh = mesh.Mesh.from_file('hub.stl')
    rotation = np.array((90, 0, 0))
    position = np.array((0, 0, 0))
    original = Piece(hub_mesh, rotation, position)
    print("Original orientation: {}".format(original.orientation))
    rx1 = Piece(hub_mesh, rotation + (0, 180, 90), position + (1.5*GRID_UNIT_IN_MM,-1.5 * GRID_UNIT_IN_MM,0))
    print("RX1 orientation: {}".format(rx1.orientation))
    print("Original[end1] {} connect to RX1[end1]".format("CAN" if original.get_hubs()[0].can_connect(rx1.get_hubs()[0]) else "CANNOT"))
    #rx2 = Piece(hub_mesh, rotation + (0, 180, 0), position + (1.5 * GRID_UNIT_IN_MM, -1.5 * GRID_UNIT_IN_MM, 0))
    #print("Original[end1] {} connect to RX2[end1]".format("CAN" if original.get_hubs()[0].can_connect(rx2.get_hubs()[0]) else "CANNOT"))
    return [original, rx1]#, rx2]

def main():
    # pieces = sandbox_pieces()
    #pieces = single_piece()
    # pieces = positioned_pieces()
    #pieces = rotated_pieces()
    # pieces = grid_pieces()
    # meshes = [p.get_mesh() for p in pieces]
    #targets = test_targets()
    #targets.extend([p.get_mesh() for p in pieces])
    #display(targets)
    pieces = connectable_pieces()
    meshes = [p.get_mesh() for p in pieces]
    display(meshes)

    pass

if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
