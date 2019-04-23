from unittest import TestCase

from display import display_meshes_with_colors
from hub import Hub
from piece import Piece


class Test_Hub(TestCase):
    def test_can_connect_end_1_rot_90_180_0(self):
        A = Hub(Hub.TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B_close = Hub(Hub.TYPE_END_1, parent=Piece(position=(0, 0, 0),
                                                   rotation=(90, 180, 0)))
        meshes.append(B_close.get_mesh())
        color = 'green' if A.can_connect(B_close) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B_close.get_mesh()], ['grey', color])

    def test_can_connect_end_1_rot_0_180_90(self):
        A = Hub(Hub.TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B_close = Hub(Hub.TYPE_END_1, parent=Piece(position=(0, 0, 0),
                                                   rotation=(0, 180, 90)))
        meshes.append(B_close.get_mesh())
        color = 'green' if A.can_connect(B_close) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B_close.get_mesh()], ['grey', color])

    def test_can_connect_end_1_rot_180_90_90(self):
        A = Hub(Hub.TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B_close = Hub(Hub.TYPE_END_1, parent=Piece(position=(0, 0, 0),
                                                   rotation=(180, 90, 90)))
        meshes.append(B_close.get_mesh())
        color = 'green' if A.can_connect(B_close) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B_close.get_mesh()], ['grey', color])


    def test_can_connect_end_1_all(self):
        A = Hub(Hub.TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(),]
        colors = ['grey',]
        pos = 0
        for rot_x in range(4):
            for rot_y in range(4):
                for rot_z in range(4):
                    pos += 1
                    B = Hub(Hub.TYPE_END_1, parent=Piece(position=(50 * pos, 50 * pos, 50 * pos),
                                                         rotation=(90*rot_x, 90*rot_y, 90*rot_z)))
                    B_close = Hub(Hub.TYPE_END_1, parent=Piece(position=(50, 0, 0),
                                                               rotation=(90*rot_x, 90*rot_y, 90*rot_z)))
                    meshes.append(B.get_mesh())
                    color = 'green' if A.can_connect(B) else 'red'
                    colors.append(color)
                    print(B.orientation)
                    display_meshes_with_colors([A.get_mesh(),B_close.get_mesh()], ['grey', color])

        display_meshes_with_colors(meshes, colors)