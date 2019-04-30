import numpy as np
from stl import mesh

from display import display_parts, display_meshes_with_colors, display_meshes
from grid import GRID_UNIT_IN_MM, Grid
from hub import Hub, TYPE_END_1
from orientation import orient_mesh
from piece import Piece  # , orient_mesh
from unittest import TestCase

class Test_Parts(TestCase):
    def setUp(self) -> None:
        print("Setup!")

    def test_single_piece(self):
        piece_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        p = Piece(rotation, position, piece_mesh)
        display_parts([p,])

    def test_single_piece_rotated_x_90(self):
        piece_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((90, 0, 0))
        position = np.array((0, 0, 0))
        p = Piece(rotation, position, piece_mesh)
        display_parts([p,])

    def test_hub_orientation(self):
        meshes = []
        colors = []
        pos = 0
        for x_rot in range(4):
            for y_rot in range(4):
                for z_rot in range(4):
                    end1_mesh = mesh.Mesh.from_file('stl/hub_end_1.stl')
                    rotation = np.array((90*x_rot, 90*y_rot, 90*z_rot))
                    print(rotation)
                    position = np.array([0, 0, 0])
                    orient_mesh(end1_mesh, rotation=rotation, translation=position)
                    p = Piece(position=position, rotation=rotation)
                    end1_piece = Hub(TYPE_END_1,parent=p)
                    meshes.append(end1_mesh)
                    meshes.append(p.get_mesh())
                    meshes.append(end1_piece.get_mesh())
                    colors.append('red')
                    colors.append('white')
                    colors.append('blue')
                    #p = Piece(rotation, position, end1_mesh)
                    pos += 1
                    display_meshes_with_colors([end1_mesh, p.get_mesh(),end1_piece.get_mesh()], ['red', 'white', 'blue'])

    def test_rotate_separately(self):
        end1 = Hub(TYPE_END_1, Piece())
        end2 = Hub(TYPE_END_2, Piece())
        center = Hub(TYPE_CENTER, Piece())
        display_meshes([p.get_mesh() for p in [end1, end2, center]])


    def test_single_moved_piece(self):
        piece_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 50, 0))
        p = Piece(rotation, position, piece_mesh)
        display_parts([p,])

    def single_transformed_piece(self):
        piece_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((-90, 180, 270))
        position = np.array((-30, 50, -100))
        return [Piece(rotation, position, piece_mesh), ]

    def all_meshes(self):
        piece_mesh = mesh.Mesh.from_file('stl/piece.stl')
        end1_mesh =  mesh.Mesh.from_file('stl/hub_end_1.stl')
        end2_mesh =  mesh.Mesh.from_file('stl/hub_end_2.stl')
        center_mesh =  mesh.Mesh.from_file('stl/hub_center.stl')
        return [piece_mesh, end1_mesh, end2_mesh, center_mesh]

    def fix_mesh(self, name, shift, rotation):
        mesh_data = mesh.Mesh.from_file(name)
        # Translate to correct position. Translations happens from center of the mesh's mass to the objects location
        orient_mesh(mesh_data, rotation, shift)
        mesh_data.save(name+"_fixed.stl")


    def positioned_pieces(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        original = Piece(rotation, position, hub_mesh)
        x1 = Piece(rotation, position + np.array((GRID_UNIT_IN_MM, 0, 0)), hub_mesh)
        xm1 = Piece(rotation, position + np.array((-1 * GRID_UNIT_IN_MM, 0, 0)), hub_mesh)
        y1 = Piece(rotation, position + np.array((0, GRID_UNIT_IN_MM, 0)), hub_mesh)
        z1 = Piece(rotation, position + np.array((0, 0, GRID_UNIT_IN_MM)), hub_mesh)
        # rx1 = Piece(hub_mesh, rotation + (90, 0, 0), position)
        return [original, x1, xm1, y1, z1]


    def rotated_pieces(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        original = Piece(hub_mesh, rotation, position)
        rx1 = Piece(rotation + (90, 0, 0), position + np.array((GRID_UNIT_IN_MM, 0, 0)), hub_mesh)
        ry1 = Piece(rotation + (0, 90, 0), position + np.array((-1 * GRID_UNIT_IN_MM, 0, 0)), hub_mesh)
        rz1 = Piece(rotation + (0, 0, 90), position + np.array((2 * GRID_UNIT_IN_MM, 0, 0)), hub_mesh)
        return [original, rx1, ry1, rz1]


    def connected_pieces_center_1(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        original = Piece(rotation, position, hub_mesh)
        rx1 = Piece(rotation + (90, 180, 0), position, hub_mesh)
        return [original, rx1]


    def connected_pieces_center_2(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        original = Piece(rotation, position, hub_mesh)
        rx1 = Piece(rotation + (-90, 0, 180), position, hub_mesh)
        return [original, rx1]


    def connected_pieces_center_3(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        original = Piece(rotation, position, hub_mesh)
        rx1 = Piece((90, 90, 0), position, hub_mesh)
        return [original, rx1]


    def grid_pieces(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        pieces = []
        original = Piece(rotation, position, hub_mesh)
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    piece = Piece(rotation + (90 * x, 90 * y, 90 * z), position + (120 * x, 120 * y, 120 * z), hub_mesh)
                    pieces.append(piece)
        return pieces


    def sandbox_pieces(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((0, 0, 0))
        position = np.array((0, 0, 0))
        piece_list = [
            Piece(rotation + np.array((90 * i, 90 * i, 90 * i)), position + np.array((10 * i, 10 * i, 10 * i)), hub_mesh)
            for i in range(4)]
        return piece_list


    def test_targets(self):
        grid = Grid([(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (1, 2, 3), ])
        t100 = grid.get_voxel_at_coords((1, 0, 0))
        t101 = grid.get_voxel_at_coords((1, 0, 1))
        tm100 = grid.get_voxel_at_coords((-1, 0, 0))
        print("Is (1,0,0) a target? {}".format(t100.is_target))
        print("Is (1,0,1) a target? {}".format(t101.is_target))
        print("Is (-1,0,0) a target? {}".format(tm100.is_target))
        return grid.get_targets_meshes()


    def connectable_pieces(self):
        hub_mesh = mesh.Mesh.from_file('stl/piece.stl')
        rotation = np.array((90, 0, 0))
        position = np.array((0, 0, 0))
        original = Piece(rotation, position, hub_mesh)
        print("Original orientation: {}".format(original.orientation))
        rx1 = Piece(rotation + (0, 180, 90), position + (1.5 * GRID_UNIT_IN_MM, -1.5 * GRID_UNIT_IN_MM, 0), hub_mesh)
        print("RX1 orientation: {}".format(rx1.orientation))
        print("Original[end1] {} connect to RX1[end1]".format(
            "CAN" if original.get_hubs()[0].can_connect(rx1.get_hubs()[0]) else "CANNOT"))
        # rx2 = Piece(hub_mesh, rotation + (0, 180, 0), position + (1.5 * GRID_UNIT_IN_MM, -1.5 * GRID_UNIT_IN_MM, 0))
        # print("Original[end1] {} connect to RX2[end1]".format("CAN" if original.get_hubs()[0].can_connect(rx2.get_hubs()[0]) else "CANNOT"))
        return [original, rx1]  # , rx2]
