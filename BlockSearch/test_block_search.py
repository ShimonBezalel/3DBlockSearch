from unittest import TestCase
from uuid import uuid4

from BlockSearch.block_search import Block_Search, Cover_Block_Search
from BlockSearch.search import a_star_search, null_heuristic
from pprint import pprint as pp
from BlockSearch.tower_state import Tower_State
from BlockSearch.render import save_by_orientation, save_by_orientation_blocks, save
from BlockSearch.physics import combine
from BlockSearch.block import ORIENTATIONS
import os


def dist_heuristic(state: Tower_State, block_search: Block_Search):
    return (block_search._height_goal - state._max_level)

def cover_heuristic(state: Tower_State, block_search: Block_Search):
    starting_point = state._starting_cover_size
    end_goal = state._starting_cover_size / block_search._height_goal
    proportional_height = state._max_level / block_search._height_goal
    desired_cover = state._starting_cover_size / proportional_height
    actual_cover = state.get_cover_at_level(state._max_level - 1)
    if actual_cover > desired_cover:
        # encourage building tall
        return (block_search._height_goal - state._max_level)
    else:
        #encourage bulding wide
        return (block_search._height_goal - state._max_level)/15

    # return (block_search._height_goal - state._max_level)/15
    # pass

def save_process(actions, subfolder="default", translation = (0,0,0), seperate_by_orientation=True):
    try:
        os.mkdir(os.path.join("saved_stls", subfolder))
    except Exception as e:
        print(e)
    if seperate_by_orientation:
        try:
            for orientation in ORIENTATIONS.keys():
                os.mkdir(os.path.join("saved_stls", subfolder, orientation))
        except  Exception as e:
            print(e)
    if translation == (0,0,0):
        block_aggregation = []
        for i, block_list in enumerate(actions):
            block_aggregation += block_list
            if seperate_by_orientation:
                save_by_orientation_blocks(block_aggregation, subfolder=subfolder)
            else:
                m = combine([b.render() for b in block_aggregation])
                save([m], subfolder=subfolder)
    # else:
    #     block_aggregation = []
    #     for i, block_list in enumerate(actions):
    #         block_aggregation += block_list
    #         meshes = [translate(b.render() +
    #         mesh_aggregation = combine(])
    #         save_by_orientation_blocks(block_aggregation, subfolder=subfolder)


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

class Cover_Block_Search_Test(TestCase):

    def test_null_heuristic(self):
        print("Null heuristic test")
        s = a_star_search(Cover_Block_Search(height_goal=16, floor_size=50))
        pp(s)
        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="null_heuristic20")

    def test_null_heuristic_less_branch(self):
        print("Null heuristic test with smaller branching factor")
        s = a_star_search(Cover_Block_Search(height_goal=16, floor_size=50, limit_branching=5, limit_sons=200))
        pp(s)
        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="null_heuristic20")


    def test_distance_from_max_heuristic20(self):
        print("max dist 20 height")
        s = a_star_search(Cover_Block_Search(height_goal=20, floor_size=20, limit_branching=5, limit_sons=500), dist_heuristic)
        pp(s)
        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="search_result_20")

    def test_distance_from_max_heuristic100(self):
        print("max dist 100 height")
        s = a_star_search(Cover_Block_Search(height_goal=31,
                                             floor_size=30,
                                             limit_branching=1000,
                                             limit_sons=500,
                                             limit_blocks_in_action=2,
                                             random_order=False


                                             ), dist_heuristic)
        pp(s)

        blocks = []
        for action in s:
            blocks.extend(action)
        print(len(blocks))
        SAVE = True
        if SAVE:
            save_process(actions=s, subfolder="cover_tower_30_no_rand_low_thresh_1000branches", seperate_by_orientation=False)

    def test_distance_from_max_heuristic50sym(self):
        print("max dist 50 height, symmetrical")

        s = a_star_search(Block_Search(use_symmetry=True, height_goal=50, floor_size=5), dist_heuristic)
        pp(s)

        blocks = []
        for action in s:
            blocks.extend(action)
        if SAVE:
            save_by_orientation_blocks(blocks=blocks, subfolder="search_result_50_sym")






