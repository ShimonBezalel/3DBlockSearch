from copy import deepcopy, copy
from unittest import TestCase

from display import display_meshes_with_colors
from hub import Hub, TYPE_END_1, TYPE_END_2, TYPE_CENTER
from piece import Piece


class Test_Hub(TestCase):
    def test_local_rotate_end_1_90_deg_x(self):
        A = Hub(TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B = deepcopy(A)

        meshes.append(B.get_mesh())
        color = 'green' if A.can_connect(B) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B.get_mesh()], ['grey', color])

    def test_can_connect_end_1_rot_90_180_0(self):
        A = Hub(TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B_close = Hub(TYPE_END_1, parent=Piece(position=(0, 0, 0),
                                                   rotation=(90, 180, 0)))
        meshes.append(B_close.get_mesh())
        color = 'green' if A.can_connect(B_close) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B_close.get_mesh()], ['grey', color])

    def test_can_connect_end_1_rot_0_180_90(self):
        A = Hub(TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B_close = Hub(TYPE_END_1, parent=Piece(position=(0, 0, 0),
                                                   rotation=(0, 180, 90)))
        meshes.append(B_close.get_mesh())
        color = 'green' if A.can_connect(B_close) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B_close.get_mesh()], ['grey', color])

    def test_can_connect_end_1_rot_180_90_90(self):
        A = Hub(TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        B_close = Hub(TYPE_END_1, parent=Piece(position=(0, 0, 0),
                                                   rotation=(180, 90, 90)))
        meshes.append(B_close.get_mesh())
        color = 'green' if A.can_connect(B_close) else 'red'
        colors.append(color)
        display_meshes_with_colors([A.get_mesh(), B_close.get_mesh()], ['grey', color])


    def test_can_connect_end_1_all(self):
        A = Hub(TYPE_END_1, parent=Piece())
        meshes = [A.get_mesh(),]
        colors = ['grey',]
        pos = 0
        for rot_x in range(4):
            for rot_y in range(4):
                for rot_z in range(4):
                    pos += 1
                    B = Hub(TYPE_END_1, parent=Piece(position=(50 * pos, 50 * pos, 50 * pos),
                                                         rotation=(90*rot_x, 90*rot_y, 90*rot_z)))
                    B_close = Hub(TYPE_END_1, parent=Piece(position=(50, 0, 0),
                                                               rotation=(90*rot_x, 90*rot_y, 90*rot_z)))
                    meshes.append(B.get_mesh())
                    color = 'green' if A.can_connect(B) else 'red'
                    colors.append(color)
                    print(B.orientation)
                    display_meshes_with_colors([A.get_mesh(),B_close.get_mesh()], ['grey', color])

        display_meshes_with_colors(meshes, colors)

    def test_can_connect_end_1_rotated_all(self):
        A = Hub(TYPE_END_1, parent=Piece(rotation=(0,0,0)))
        meshes = [A.get_mesh(),]
        colors = ['grey',]
        pos = 0
        for rot_x in range(4):
            for rot_y in range(4):
                for rot_z in range(4):
                    pos += 1
                    rotation = (90*rot_x, 90*rot_y, 90*rot_z)
                    B = Hub(TYPE_END_1, parent=Piece(rotation=(rotation)))
                    meshes.append(B.get_mesh())
                    color = 'green' if A.can_connect(B) else 'red'
                    colors.append(color)
                    print('\n ------ {} ------'.format('YES' if A.can_connect(B) else 'NOT'))
                    print(B.orientation)
                    print('driving rotation: ' , rotation)
                    print('driven rotation:  ' , B.orientation.to_rotation())
                    display_meshes_with_colors([A.get_mesh(),B.get_mesh()], ['grey', color])

        display_meshes_with_colors(meshes, colors)

    def test_can_connect_end_1_specific(self):
        A = Hub(TYPE_END_1, parent=Piece(rotation=(0,0,0)))
        meshes = [A.get_mesh(),]
        colors = ['grey',]
        pos = 0
        for rotation in [(90,90,90), (0,180,90)]:
            B = Hub(TYPE_END_1, parent=Piece(rotation=rotation))
            meshes.append(B.get_mesh())
            color = 'green' if A.can_connect(B) else 'red'
            colors.append(color)
            print(B.orientation)
            print(B.orientation.to_rotation())
            display_meshes_with_colors([A.get_mesh(),B.get_mesh()], ['grey', color])

        display_meshes_with_colors(meshes, colors)

    def test_get_connectible_pieces(self):
        import random
        r = lambda: random.randint(0, 255)
        random_color = lambda : '#%02X%02X%02X' % (r(), r(), r())

        A = Hub(TYPE_END_1, parent=Piece(rotation=(0, 0, 0)))
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        for p in A.get_connectible_pieces():
            meshes.append(p.get_mesh())
            color = random_color()
            colors.append(color)
            display_meshes_with_colors([A.get_mesh(), p.get_mesh()], ['grey', color])

        display_meshes_with_colors(meshes, colors)

    def test_get_connectible_pieces_hubs(self):
        import random
        r = lambda: random.randint(0, 255)
        random_color = lambda : '#%02X%02X%02X' % (r(), r(), r())

        A = Hub(TYPE_END_1, parent=Piece(rotation=(0, 0, 0)))
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        for p in A.get_connectible_pieces():
            piece_meshes = [A.get_mesh(),]
            piece_colors = ['grey',]
            #meshes.append(p.get_mesh())
            #piece_meshes.append(p.get_mesh())
            color = random_color()
            #colors.append('white')
            #piece_colors.append('white')
            for hub in p.get_hubs():
                piece_meshes.append(hub.get_mesh())
                meshes.append(hub.get_mesh())
                colors.append(color)
                piece_colors.append(color)
            display_meshes_with_colors(piece_meshes, piece_colors)

        display_meshes_with_colors(meshes, colors)

    def test_get_connectible_pieces_end2_hubs(self):
        import random
        r = lambda: random.randint(0, 255)
        random_color = lambda : '#%02X%02X%02X' % (r(), r(), r())

        A = Hub(TYPE_END_2, parent=Piece(rotation=(0, 0, 0)))
        meshes = [A.get_mesh(), ]
        colors = ['grey', ]
        for p in A.get_connectible_pieces():
            piece_meshes = [A.get_mesh(),]
            piece_colors = ['grey',]
            #meshes.append(p.get_mesh())
            #piece_meshes.append(p.get_mesh())
            color = random_color()
            #colors.append('white')
            #piece_colors.append('white')
            for hub in p.get_hubs():
                piece_meshes.append(hub.get_mesh())
                meshes.append(hub.get_mesh())
                colors.append(color)
                piece_colors.append(color)
            display_meshes_with_colors(piece_meshes, piece_colors)

        display_meshes_with_colors(meshes, colors)

    def test_get_connectible_pieces_center_hubs(self):
        import random
        r = lambda: random.randint(0, 255)
        random_color = lambda: '#%02X%02X%02X' % (r(), r(), r())

        P = Piece()
        A = P.get_hubs()[1] # center
        meshes = [P.get_mesh(), A.get_mesh(), ]
        colors = ['white', 'grey', ]
        for p in A.get_connectible_pieces():
            piece_meshes = [P.get_mesh(), A.get_mesh(), ]
            piece_colors = ['white', 'grey', ]
            # meshes.append(p.get_mesh())
            # piece_meshes.append(p.get_mesh())
            color = random_color()
            # colors.append('white')
            # piece_colors.append('white')
            for hub in p.get_hubs():
                piece_meshes.append(hub.get_mesh())
                meshes.append(hub.get_mesh())
                colors.append(color)
                piece_colors.append(color)
            display_meshes_with_colors(piece_meshes, piece_colors)

        display_meshes_with_colors(meshes, colors)

    def test_get_connectible_pieces_all(self):
        import random
        r = lambda: random.randint(0, 255)
        random_color = lambda: '#%02X%02X%02X' % (r(), r(), r())

        P = Piece()
        meshes = [P.get_mesh(),]
        colors = ['white', ]
        for hub in P.get_hubs():
            color = random_color()
            hub_meshes = [P.get_mesh(),]
            hub_meshes.append(hub.get_mesh())
            hub_colors = ['white', ]
            hub_colors.append(color)
            for O in hub.get_connectible_pieces():
                for O_hub in O.get_hubs():
                    hub_meshes.append(O_hub.get_mesh())
                    meshes.append(O_hub.get_mesh())
                    colors.append(color)
                    hub_colors.append(color)
            display_meshes_with_colors(hub_meshes, hub_colors)

        display_meshes_with_colors(meshes, colors)