from copy import copy
from random import shuffle

from stl import mesh

from BlockSearch.search import SearchProblem
from BlockSearch.tower_state import Tower_State
from BlockSearch.block import Block
from typing import List, Set, Dict, Tuple, Optional, Generator
from BlockSearch import physics
from pprint import pprint as pp
from BlockSearch.render import display


X = 0
Y = 1
Z = 2
block_mesh = mesh.Mesh.from_file('kapla.stl')
DISPLAY = False

class Block_Search(SearchProblem):
    minus = [-1, 1, -1, 1]
    tinus = [-1, -1, 1, 1]

    @staticmethod
    def propagate(orientation : Tuple[int, int, int], position : Tuple[int, int, int], dist=6):
        if orientation == (90, 0, 0) or orientation == (90, 0, 90):
            dist_x = dist // 2
            dist_y = dist // 2

        elif orientation == (0, 90, 0) or orientation == (0, 0, 0):
            dist_x = dist
            dist_y = dist * 2

        else:
            dist_x = dist * 2
            dist_y = dist

        # add blocks to tower in some order, without creating collisions
        # Create i identical blocks
        positions = []
        for i in range(len(Block_Search.minus)):
            positions.append((position[X] + Block_Search.minus[i] * dist_x,
                              position[Y] + Block_Search.tinus[i] * dist_y,
                              position[Z]))
        block_descriptors = [(orientation, new_position) for new_position in positions]
        return block_descriptors

    def __init__(self,
                 floor_size=30,
                 limit_sons=500,
                 son_orientation_filter=lambda o: True,
                 random_order=True,
                 use_symmetry=False,
                 sym_son_threshold=2,
                 sym_base_dist=6,
                 limit_blocks_in_action=10,
                 limit_branching=10,
                 height_goal=30
                 ):
        self._floor_size = floor_size
        self._limit_sons = limit_sons
        self._son_orientation_filter = son_orientation_filter
        self._gen_randomly = random_order
        self._use_symmetry = use_symmetry
        self._sym_son_threshold = sym_son_threshold
        self._num_of_blocks_in_action = limit_blocks_in_action
        self._num_of_descriptors_disqualified = 0
        self._num_of_blocks_disqualified = 0
        self._symmetrical_base_distance = sym_base_dist
        self._limit_branching=limit_branching
        self._height_goal = height_goal

    def get_start_state(self):
        return Tower_State(self._floor_size)

    def get_successors(self, state: Tower_State):
        new_states = [copy(state) for _ in range(self._limit_branching)]
        successors = []
        pp(state)
        for new_state in new_states:
            num_of_blocks_added = 0
            actions = []
            for father_block in state.gen_blocks(no_floor=False):
                if len(actions) > self._num_of_blocks_in_action:
                    break
                son_descriptors = list(father_block.gen_possible_block_descriptors(
                    limit_len=self._limit_sons,
                    limit_orientation=self._son_orientation_filter,
                    random_order=self._gen_randomly
                ))
                if self._gen_randomly:
                    shuffle(son_descriptors)
                for desc in son_descriptors:
                    if len(actions) > self._num_of_blocks_in_action:
                        break
                    if state.is_bad_block(Block.get_str(desc)):
                        self._num_of_descriptors_disqualified += 1
                    else:  # good block description, lets try it out
                        blocks = [Block(block_mesh, *desc)]
                        if self._use_symmetry:
                            sub_descriptors = Block_Search.propagate(*desc, dist=self._symmetrical_base_distance)
                            # qualified_symmetrical_brothers = len(sub_descriptors)
                            for sym_desc in sub_descriptors:
                                if state.is_bad_block(Block.get_str(desc)):
                                    self._num_of_descriptors_disqualified += 1
                                    # qualified_symmetrical_brothers -= 1
                                else:
                                    blocks.append(Block(block_mesh, *sym_desc))
                        to_add = []
                        for candidate_block in blocks:
                            if new_state.can_add(candidate_block):
                                to_add.append(candidate_block)
                            else:
                                self._num_of_blocks_disqualified += 1
                            # else:
                            #     if self._use_symmetry:
                            #         qualified_symmetrical_brothers -= 1
                        if self._use_symmetry:
                            if len(to_add) >= self._sym_son_threshold:
                                for good_block in to_add:
                                    new_state.add(good_block)
                                    actions.append(good_block)
                                    num_of_blocks_added += 1

                            else:
                                for good_block in to_add:
                                    self._num_of_blocks_disqualified += 1
                                    new_state.disconnect(good_block)
                        else:
                            for good_block in to_add:
                                new_state.add(good_block)
                                actions.append(good_block)
                                num_of_blocks_added += 1
            successors.append((new_state, actions, len(actions)))
        # pp(successors)
        print("\tNum of desc disqualified:{}\tNum of blocks disqualified:{}".format(
            self._num_of_descriptors_disqualified,
            self._num_of_blocks_disqualified
        ))
        return successors

    def get_cost_of_actions(self, actions):
        return len(actions)

    def is_goal_state(self, state: Tower_State):
        if state._max_level >= self._height_goal:
            if DISPLAY:
                display([b.render() for b in state.gen_blocks()])
            return True
        return False






