from unittest import TestCase
from BlockSearch.block_search import Block_Search
from BlockSearch.search import a_star_search, null_heuristic
from pprint import pprint as pp
from BlockSearch.tower_state import Tower_State
from BlockSearch.render import save_by_orientation, save_by_orientation_blocks


def dist_heuristic(state: Tower_State, block_search: Block_Search):
    return (block_search._height_goal - state._max_level)

SAVE = False

class Block_Search_Test(TestCase):

    def test_null_heuristic(self):
        print("Null heuristic test")
        s = a_star_search(Block_Search(height_goal=20, floor_size=7))
        pp(s)
        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="null_heuristic20")


    def test_distance_from_max_heuristic20(self):
        print("max dist 20 height")
        s = a_star_search(Block_Search(height_goal=20, floor_size=7), dist_heuristic)
        pp(s)
        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="search_result_20")

    def test_distance_from_max_heuristic100(self):
        print("max dist 100 height")
        s = a_star_search(Block_Search(height_goal=100, floor_size=5), dist_heuristic)
        pp(s)

        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="search_result_100")

    def test_distance_from_max_heuristic50sym(self):
        print("max dist 50 height, symmetrical")

        s = a_star_search(Block_Search(use_symmetry=True, height_goal=50, floor_size=5), dist_heuristic)
        pp(s)

        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="search_result_50_sym")





