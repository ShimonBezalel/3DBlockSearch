"""
In search.py, you will implement generic search algorithms
"""
from copy import deepcopy

import numpy as np

import util
from grid import Grid, GRID_UNIT_WITH_SPACING
from piece import Piece
from target import Target

STATE_INDEX = 0
ACTION_INDEX = 1
COST_INDEX = 2
HEUR_INDEX = 3


class HubSpreadProblem:

    def __init__(self, targets, heuristic=None):
        self.expanded = 0
        self.targets = targets
        self.grid = Grid(targets=self.targets)

    def get_start_state(self, heuristic=None, display=False):
        """
        Returns the start state for the search problem
        """
        # if not heuristic:
        #     starting_piece = Piece(position=self.targets[0].position)
        # else:
        #     starting_piece = self.choose_starting_piece(self.grid, heuristic, display)
        # start = deepcopy(self.grid)
        # start.add_piece(starting_piece)
        return self.grid
        #return start

    def is_goal_state(self, state: Grid):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        return (len(state.remaining_targets()) == 0)

    def get_successors(self, state: Grid, outdir=None, heuristic=lambda x:0):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Return starting piece on first call
        if not state.pieces:
            p = self.choose_starting_piece(state, heuristic=heuristic,display=False)
            grid_with_piece = deepcopy(state)
            grid_with_piece.add_piece(p)
            return [(grid_with_piece, p, 1),]
        # Then return successors
        successors = []
        for hub in state.open_hubs:
            for p in hub.get_connectible_pieces():
                if state.can_add_piece(p):
                    pcopy = deepcopy(p)
                    grid_with_piece = deepcopy(state)
                    grid_with_piece.add_piece(pcopy)
                    successors.append((grid_with_piece, pcopy, 1))
        return successors

    def choose_starting_piece(self, empty_grid : Grid, heuristic, display):
        min_piece = None
        min_heur = float('inf')
        for target in self.targets:
            for rot_x in range(0,180,90):
                for rot_y in range(0, 180, 90):
                    for rot_z in range(0, 180, 90):
                        p = Piece(rotation=(rot_x,rot_y,rot_z), position=target.position)
                        grid = deepcopy(empty_grid)
                        grid.add_piece(p)
                        h = heuristic(grid, self)
                        if display:
                            grid.display(heur=h)
                        if h < min_heur:
                            min_heur = h
                            min_piece = p
        return min_piece

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


def maximal_mindist_heuristic(state: Grid, problem: HubSpreadProblem, outdir=None):
    max_mindist = float('-inf')
    min_lines = []
    labels = []
    if not state.remaining_targets():
        return 0

    max_target = state.remaining_targets()[0]
    for target in state.remaining_targets():
        mindist = float('inf')
        min_start, min_end = target.position, None
        for hub in state.open_hubs:
            dist = np.linalg.norm(target.position - hub.position)
            grid_dist = dist / (3*GRID_UNIT_WITH_SPACING)
            if (grid_dist < mindist):
                mindist = grid_dist
                min_end = hub.position
        # add line from target to closest hub
        if not (min_end is None):
            min_lines.append([min_start, min_end, 'grey'])
        # highlight target with maximal mindist
        if mindist > max_mindist:
            max_mindist = mindist
            max_target = target

        # add label of mindist above target
        label_pos = (target.position[0], target.position[1], target.position[2] + GRID_UNIT_WITH_SPACING / 2)
        labels.append((*label_pos, str("{0:.1f}".format(mindist))))

    state.labels = labels
    state.lines = min_lines
    state.max_target = max_target

    return round(max_mindist,1)


def sum_mindist_heuristic(state: Grid, problem: HubSpreadProblem, outdir=None):
    sum_mindist = 0
    min_lines = []
    labels = []
    if not state.remaining_targets():
        return 0

    for target in state.remaining_targets():
        mindist = float('inf')
        min_start, min_end = target.position, None
        for hub in state.open_hubs:
            dist = np.linalg.norm(target.position - hub.position)
            grid_dist = dist / (3*GRID_UNIT_WITH_SPACING)
            if (grid_dist < mindist):
                mindist = grid_dist#*50
                min_end = hub.position
        # add line from target to closest hub
        if not (min_end is None):
            min_lines.append([min_start, min_end, 'grey'])

        # accumulate mindist
        sum_mindist += mindist*5

        # add label of mindist above target
        label_pos = (target.position[0], target.position[1], target.position[2] + GRID_UNIT_WITH_SPACING / 2)
        labels.append((*label_pos, str("{0:.2f}".format(mindist))))

    state.labels = labels
    state.lines = min_lines

    return sum_mindist + len(state.remaining_targets())*50
