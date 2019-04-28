from unittest import TestCase

from grid import Grid
from hub_spread_search import HubSpreadProblem, maximal_mindist_heuristic, sum_mindist_heuristic
from search import breadth_first_search, a_star_search
from target import Target


class Test_Block_Search(TestCase):

    def test_ucs(self):
        t1 = Target((5,0,0))
        t2 = Target((0,5,0))
        t3 = Target((0,0,5))
        problem = HubSpreadProblem(targets=[t1,t2,t3])
        problem.grid.display(scale=200)

    def test_dfs(self):
        t1 = Target((0, 0, 0))
        t2 = Target((2, 0, 0))
        t3 = Target((0, 0, 2))
        t4 = Target((-2, 0, 2))
        empty_grid = Grid([t1, t2, t3, t4])
        empty_grid.display(filename="../screenshots/dfs3/0.png", all_white=True)
        problem = HubSpreadProblem(targets=[t1, t2, t3, t4])
        #problem.grid.display(scale=200, all_white=True)

        path = breadth_first_search(problem)
        grid = problem.get_start_state()
        count=1
        grid.display(filename="../screenshots/dfs3/{}.png".format(count), all_white=True)
        count +=1
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
        print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))

    def test_maximal_mindist_heuristic(self):
        t1 = Target((0, 2, 0))
        t2 = Target((2, 0, 0))
        t3 = Target((0, 0, 2))
        t4 = Target((-2, 2, 2))
        t5 = Target((-2, 3, 4))
        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5])
        state = problem.get_start_state()
        #print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = a_star_search(problem, maximal_mindist_heuristic)

    def test_maximal_mindist_heuristic_small(self):
        OUT_DIR_A_STAR = '../screenshots/a_star'
        t1 = Target((-2, 0, 0))
        t2 = Target((0, 2, 0))
        t3 = Target((0, 0, 0))
        empty_grid = Grid([t1, t2, t3])
        empty_grid.display(all_white=True, dirname=OUT_DIR_A_STAR, scale=50)

        problem = HubSpreadProblem(targets=[t1, t2, t3])# t4, t5])
        state = problem.get_start_state()
        #print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = a_star_search(problem, maximal_mindist_heuristic, outdir=OUT_DIR_A_STAR)
        grid = problem.get_start_state()
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)

    def test_dfs_vs_astar(self):
        OUT_DIR_A_DFS = '../screenshots/a_dfs'
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

        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5, t6])# t4, t5])
        state = problem.get_start_state()
        #print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
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

        problem = HubSpreadProblem(targets=[t1, t2, t3, t4, t5, t6])# t4, t5])
        state = problem.get_start_state()
        #print ("MAXIMAL MINDIST = ", maximal_mindist_heuristic(state))
        path = a_star_search(problem, sum_mindist_heuristic, outdir=OUT_DIR_A_STAR)
        grid = problem.get_start_state()
        grid.lines = None
        grid.labels = None

        grid.display(all_white=True, dirname=OUT_DIR_A_STAR)
        for piece in path:
            grid.add_piece(piece)
            grid.display(all_white=False, dirname=OUT_DIR_A_STAR)
