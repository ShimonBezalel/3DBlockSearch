from unittest import TestCase

from display import display_meshes_with_colors_and_alphas, random_color
from grid import Grid, OPEN_HUB_COLOR
from hub_spread_search import HubSpreadProblem, maximal_mindist_heuristic, sum_mindist_heuristic
from piece import Piece
from search import breadth_first_search, a_star_search
from target import Target


class Test_Block_Search(TestCase):

    def test_ucs(self):
        t1 = Target((5, 0, 0))
        t2 = Target((0, 5, 0))
        t3 = Target((0, 0, 5))
        problem = HubSpreadProblem(targets=[t1, t2, t3])
        problem.grid.display(scale=200)

    def test_dfs(self):
        t1 = Target((0, 0, 0))
        t2 = Target((2, 0, 0))
        t3 = Target((0, 0, 2))
        t4 = Target((-2, 0, 2))
        empty_grid = Grid([t1, t2, t3, t4])
        empty_grid.display(filename="../screenshots/dfs3/0.png", all_white=True)
        problem = HubSpreadProblem(targets=[t1, t2, t3, t4])
        # problem.grid.display(scale=200, all_white=True)

        path = breadth_first_search(problem)
        grid = problem.get_start_state()
        count = 1
        grid.display(filename="../screenshots/dfs3/{}.png".format(count), all_white=True)
        count += 1
        for piece in path:
            grid.add_piece(piece)
            grid.display(filename="../screenshots/dfs3/{}.png".format(count), all_white=True)
            count += 1

    def test_dfs_show(self):
        t1 = Target((0, 0, 0))
        t2 = Target((2, 0, 0))
        t3 = Target((0, 0, 2))
        t4 = Target((-2, 0, 2))
        empty_grid = Grid([t1, t2, t3, t4])
        empty_grid.display(all_white=True)
        problem = HubSpreadProblem(targets=[t1, t2, t3, t4])
        # problem.grid.display(scale=200, all_white=True)

        path = breadth_first_search(problem)
        grid = problem.get_start_state()
        count = 1
        grid.display(all_white=True)
        count += 1
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=True)
            count += 1

    def test_maximal_mindist_heuristic(self):
        t1 = Target((0, 2, 0))
        t2 = Target((2, 0, 0))
        t3 = Target((0, 0, 2))
        t4 = Target((-2, 2, 2))
        t5 = Target((-2, 3, 4))
        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5])
        state = problem.get_start_state()
        print("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))

    def test_maximal_mindist_heuristic(self):
        t1 = Target((0, 2, 0))
        t2 = Target((2, 0, 0))
        t3 = Target((0, 0, 2))
        t4 = Target((-2, 2, 2))
        t5 = Target((-2, 3, 4))
        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5])
        state = problem.get_start_state()
        # print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = a_star_search(problem, maximal_mindist_heuristic)

    def test_maximal_mindist_heuristic_small(self):
        OUT_DIR_A_STAR = None  # '../screenshots/a_star'
        t1 = Target((-2, 0, 0))
        t2 = Target((0, 2, 0))
        t3 = Target((0, 0, 0))
        empty_grid = Grid([t1, t2, t3])
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_STAR, scale=50)

        problem = HubSpreadProblem(targets=[t1, t2, t3])  # t4, t5])
        state = problem.get_start_state()
        # print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = a_star_search(problem, maximal_mindist_heuristic, outdir=OUT_DIR_A_STAR)
        grid = problem.get_start_state()
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)

    def test_dfs_vs_astar(self):
        # OUT_DIR_A_DFS = '../screenshots/a_dfs'
        t1 = Target((-2, 0, 0))
        t2 = Target((0, 2, 0))
        t3 = Target((0, 0, 0))
        empty_grid = Grid([t1, t2, t3])
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_DFS, scale=50)

        problem = HubSpreadProblem(targets=[t1, t2, t3])  # t4, t5])
        state = problem.get_start_state()
        # print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = breadth_first_search(problem, outdir=OUT_DIR_A_DFS)
        grid = problem.get_start_state()
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_DFS)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_DFS)

    def test_maximal_mindist_heuristic_medium(self):
        OUT_DIR_A_STAR = None
        t1 = Target((-5, 0, 0))
        t2 = Target((0, 5, 0))
        t3 = Target((0, 0, -5))
        t4 = Target((-5, 5, 0))
        t5 = Target((4, 3, 0))
        t6 = Target((2, 0, -3))
        empty_grid = Grid([t1, t2, t3, t4, t5, t6])
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_STAR, scale=100)

        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5, t6])  # t4, t5])
        # print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = a_star_search(problem, maximal_mindist_heuristic, outdir=OUT_DIR_A_STAR)
        grid = problem.get_start_state()
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)

    def test_sum_mindist_heuristic_medium(self):
        OUT_DIR_A_STAR = None
        t1 = Target((-5, 0, 0))
        t2 = Target((0, 5, 0))
        t3 = Target((0, 0, -5))
        t4 = Target((-5, 5, 0))
        t5 = Target((4, 3, 0))
        t6 = Target((2, 0, -3))
        empty_grid = Grid([t1, t2, t3, t4, t5, t6])
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_STAR, scale=100)

        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5, t6])  # t4, t5])
        path = a_star_search(problem, sum_mindist_heuristic, outdir=OUT_DIR_A_STAR)
        grid = problem.get_start_state()
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)


    def test_sum_mindist_heuristic_medium(self):
        OUT_DIR_A_STAR = None
        t1 = Target((-5, 0, 0))
        t2 = Target((1, 0, 0))
        t3 = Target((-5, 6, 0))
        t4 = Target((1, 6, 0))
        t5 = Target((4, 3, 0))
        t6 = Target((2, 0, -3))
        targets = [t1,t2,t3,t4, t5, t6]
        empty_grid = Grid(targets)
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_STAR, scale=100)

        problem = HubSpreadProblem(targets)  # t4, t5])
        path = a_star_search(problem, maximal_mindist_heuristic, outdir=OUT_DIR_A_STAR)

        grid = empty_grid
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)

    def test_sum_mindist_heuristic_targets(self, targets, outdir=None):
        OUT_DIR_A_STAR=outdir
        empty_grid = Grid(targets)
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_STAR, scale=100)

        problem = HubSpreadProblem(targets)  # t4, t5])
        path = a_star_search(problem, sum_mindist_heuristic, outdir=OUT_DIR_A_STAR)

        grid = empty_grid
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)

    def test_sum_mindist_heuristic(self):
        t1 = Target((-3, 0, -5))
        t2 = Target((1, 0, -5))
        t3 = Target((-3, 5, -5))
        t4 = Target((1, 5, -5))
        t9 = Target([-1,0,0])
        return self.test_sum_mindist_heuristic_targets([t1,t2,t3,t4,t9])#t5,t6,t7,t8])

    def test_sum_mindist_heuristic(self):
        t1 = Target((-1, 2, -6))
        t2 = Target((-1, 6 ,-6))
        t3 = Target((-1, 4, 0))
        return self.test_sum_mindist_heuristic_targets([t1, t2, t3])  # t5,t6,t7,t8])

    def test_chair(self):
        targets = [

        # LEG LEFT BACK
        Target((-2,2,-5)),
        Target((-2,2,-3)),
        Target((-2,2,-1)),
        Target((-2,2, 1)),
        Target((-2, 2, 3)),

        # LEG RIGHT BACK
        Target((0, 2, -5)),
        Target((0, 2, -3)),
        Target((0, 2, -1)),
        Target((0, 2, 1)),
        Target((0, 2, 3)),

        # LEG LEFT FRONT
        Target((-2, 0, -5)),
        Target((-2, 0, -3)),
        Target((-2, 0, -1)),

        # LEG RIGHT FRONT
        Target((0, 0, -5)),
        Target((0, 0, -3)),
        Target((0, 0, -1)),

        ]
        self.test_sum_mindist_heuristic_targets(targets)

    def test_single_piece(self):
        p = Piece(rotation=(90,0,90),color='white')
        g = Grid(targets = [])
        g.add_piece(p)
        g.display(scale=50,all_white=False)

    def test_all_connectable(self):
        p = Piece(rotation=(90,0,90),color='white')
        for hub  in p.get_hubs():
            hub.color = OPEN_HUB_COLOR
        g = Grid(targets = [])
        g.add_piece(p)
        g.display(scale=50,all_white=False)

        meshes, colors, alphas = [p.get_mesh(),], [p.color,], [p.alpha,]
        c = ['red', 'green', 'blue']
        for i, hub in enumerate(p.get_hubs()):
            color = random_color()
            for piece in hub.get_connectible_pieces():
                meshes.append(piece.get_mesh())
                colors.append(c[i])
                alphas.append(0.1)

        display_meshes_with_colors_and_alphas(meshes=meshes, corresponding_colors=colors, corresponding_alphas=alphas, scale=50)

