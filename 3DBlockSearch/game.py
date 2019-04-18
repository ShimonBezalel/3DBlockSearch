import numpy
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from stl import mesh


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

def main():
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
    meshes = [mesh.Mesh(data.copy()) for _ in range(4)]
    display(meshes)

    pass

if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
