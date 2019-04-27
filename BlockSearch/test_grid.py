from unittest import TestCase

import piece
from grid import Grid
from target import Target


class Test_Hub(TestCase):
    def test_add_one_piece_and_render(self):
        P = piece.Piece()
        G = Grid()
        G.add_piece(P)
        G.display()

    def test_add_one_piece_and_all_connecatable_and_render(self):
        P = piece.Piece()
        G = Grid()
        G.add_piece(P)
        for hub in P.get_hubs():
            for p in hub.get_connectible_pieces():
                if G.can_add_piece(p):
                    G.add_piece(p)
        G.display()

    def test_add_one_piece_and_all_connecatable_3_and_render(self):
        scale = 100
        count = 0
        basename = lambda : '../{}/{}.png'.format('screenshots', count)
        G = Grid()
        G.display(scale=scale, filename=basename())
        count += 1
        P1 = piece.Piece()
        G.add_piece(P1)
        G.display(scale=scale, filename=basename(), all_white=True)
        count += 1
        for H1 in P1.get_hubs():
            for P2 in H1.get_connectible_pieces():
                G.display_with_candidate(P2, scale=scale, filename=basename())
                count += 1
                if G.can_add_piece(P2):
                    G.add_piece(P2)
                    for H2 in P2.get_hubs():
                        for P3 in H2.get_connectible_pieces():
                            G.display_with_candidate(P3, scale=scale, filename=basename())
                            count += 1
                            if G.can_add_piece(P3):
                                G.add_piece(P3)
        G.display(scale=scale, filename=basename())
        count+=1

    def test_add_one_piece_and_targets(self):
        scale = 100
        G = Grid([Target((0, 0, 0)),
                  Target((1, 0, 0)),
                  Target((-1, 0, 0)),
                  Target((0, 1, 0)),
                  Target((1, 2, 3)), ])
        G.display(scale=scale)
        P1 = piece.Piece()
        G.add_piece(P1)
        G.display(scale=scale, all_white=True)

    def test_targets(self):
        grid = Grid([(0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (1, 2, 3), ])
        t100 = grid.get_voxel_at_coords((1, 0, 0))
        t101 = grid.get_voxel_at_coords((1, 0, 1))
        tm100 = grid.get_voxel_at_coords((-1, 0, 0))
        self.assertTrue(t100.is_target)
        self.assertFalse(t101.is_target)
        self.assertTrue(tm100.is_target)