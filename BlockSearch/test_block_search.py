from unittest import TestCase

from hub_spread_search import HubSpreadProblem
from search import breadth_first_search
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
        t2 = Target((0, -5, 0))
        t3 = Target((0, 0, 5))
        problem = HubSpreadProblem(targets=[t1, t2, t3])
        #problem.grid.display(scale=200, all_white=True)

        path = breadth_first_search(problem)
        grid = problem.get_start_state()
        grid.display()
        for piece in path:
            grid.add_piece(piece)
            grid.display()