import numpy
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from stl import mesh
import math
from piece import Piece

def display(meshes):
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

def populate_pieces():
    shape = mesh.Mesh.from_file('3DBlockSearch/hub.stl')
    orientation = (0, 0, 0)
    position = (0, 0, 0)
    piece_list = [Piece(shape, orientation + (10 * i, 10 * i , 10 * i), position + (10 * i, 10 * i , 10 * i)) for i in range(4)]
    return piece_list

def main():
    pieces = populate_pieces()
    meshes = [p.render() for p in pieces]
    # Create 3 faces of a cube
    data = numpy.zeros(6, dtype=mesh.Mesh.dtype)

    # Top of the cube
    data['vectors'][0] = numpy.array([[0, 1, 1],
                                      [1, 0, 1],
                                      [0, 0, 1]])
    data['vectors'][1] = numpy.array([[1, 0, 1],
                                      [0, 1, 1],
                                      [1, 1, 1]])
    # Front face
    data['vectors'][2] = numpy.array([[1, 0, 0],
                                      [1, 0, 1],
                                      [1, 1, 0]])
    data['vectors'][3] = numpy.array([[1, 1, 1],
                                      [1, 0, 1],
                                      [1, 1, 0]])
    # Left face
    data['vectors'][4] = numpy.array([[0, 0, 0],
                                      [1, 0, 0],
                                      [1, 0, 1]])
    data['vectors'][5] = numpy.array([[0, 0, 0],
                                      [0, 0, 1],
                                      [1, 0, 1]])

    # Since the cube faces are from 0 to 1 we can move it to the middle by
    # substracting .5
    data['vectors'] -= .5

    # Generate 4 different meshes so we can rotate them later
    # meshes = [mesh.Mesh(data.copy()) for _ in range(4)]



    # axis = np.array([1, 0, 0])
    # theta = math.radians(90)
    # point = np.array([10, 10, 10])

    # meshes[0].rotate([0, 0, 1], theta)
    # meshes[0].x += 10
    # meshes[0].y += 10

    display(meshes)

    pass

if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
