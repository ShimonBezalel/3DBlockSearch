"""
In search.py, you will implement generic search algorithms
"""
from copy import deepcopy

import util
from grid import Grid
from piece import Piece
from target import Target

STATE_INDEX = 0
ACTION_INDEX = 1
COST_INDEX = 2
HEUR_INDEX = 3


class HubSpreadProblem:

    def __init__(self, targets):
        self.expanded = 0
        self.targets = targets
        self.grid = Grid(targets=self.targets)
        starting_piece = Piece(position=targets[0].position)
        self.grid.add_piece(starting_piece)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.grid

    def is_goal_state(self, state : Grid):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        return (len(state.remaining_targets()) == 0)

    def get_successors(self, state : Grid):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        #state.display(all_white=True)
        print("expanded = {}...".format(self.expanded))
        self.expanded += 1
        successors = []
        for hub in state.open_hubs:
            for p in hub.get_connectible_pieces():
                if state.can_add_piece(p):
                    pcopy = deepcopy(p)
                    grid_with_piece = deepcopy(state)
                    grid_with_piece.add_piece(pcopy)
                    successors.append((grid_with_piece, pcopy, 1))
        return successors


    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)