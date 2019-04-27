"""
In search.py, you will implement generic search algorithms
"""
#import sys
import heapq

from BlockSearch import util as util

STATE_INDEX     = 0
ACTION_INDEX    = 1
COST_INDEX      = 2
HEUR_INDEX      = 3

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


class SearchNode:
    def __init__(self, state, cost, heur=0):
        self.state = state
        self.cost = cost
        self.heur = heur

    def heucost(self):
        return self.cost + self.heur

def generic_first_search(problem, fringe):
    """
    Search the nodes in the search tree first according to the given fringe
    (Stack for DFS, Queue for BFS).
    """
    start_state = problem.get_start_state()
    backtrace = {start_state:(None,None)}
    fringe.push(start_state)

    while not fringe.isEmpty():
        state = fringe.pop()

        if problem.is_goal_state(state):
            return construct_path(state, backtrace)

        for child, action, _ in problem.get_successors(state):
            if child not in backtrace:
                backtrace[child] = (state, action)
                fringe.push(child)
    raise Exception("There is no solution for this problem")

def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    #path = dfs_recursion(problem, problem.get_start_state())
    #return path
    return generic_first_search(problem, util.Stack())

def dfs_recursion(problem, state, visited=set()):
    """
    Recursive implementation of DFS algorithm.
    :param problem: search problem to find a goal for
    :param state: current state from which a goal is sought
    :param visited: a set of visited states to avoid duplications
    :return: a list of actions to reach a goal from the given state (if
    possible), otherwise None.
    """
    visited.add(state)
    if problem.is_goal_state(state):
        return []
    else:
        next_moves = problem.get_successors(state)
        if next_moves == []:
            # No next moves and not a goal state?
            # This state is useless and should return None.
            return None
        else:
            for child, action, _ in next_moves:
                if child not in visited:
                    path = dfs_recursion(problem, child, visited)
                    if path != None:
                        return [action] + path
            # No successor of this state reaches the goal?
            # This state is useless and should return None.
            return None

def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return generic_first_search(problem, util.Queue())

def construct_path(state, backtrace):
    """
    Trace the path back to start from the current state
    :param state:
    :param backtrace: dict {state: (parent, action[, cost_to_child])}
    :return: list of actions from start to state
    """
    action_list = list()

    while state in backtrace:
        trace = backtrace[state]
        state, action = trace[STATE_INDEX], trace[ACTION_INDEX]
        action_list.append(action)
    action_list.reverse()
    return action_list[1:] # ignore action_list[0], garbage


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    return a_star_search(problem, null_heuristic)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    fringe = util.PriorityQueueWithFunction(lambda node: node.heucost())
    backtrace = dict() # {child_state : (parent, action, cost_to_child, heur_from_child) }

    start_state = problem.get_start_state()
    start_heur = heuristic(start_state, problem)
    fringe.push(SearchNode(start_state, 0, start_heur))
    backtrace[start_state] = (None, None, 0, start_heur)

    while not fringe.isEmpty():
        node = fringe.pop()
        state = node.state
        cost_to_parent = node.cost

        if problem.is_goal_state(state):
            return construct_path(state, backtrace)

        for child, action, _ in problem.get_successors(state):
            cost_to_child = cost_to_parent + problem.get_cost_of_actions([action])
            visited = (child in backtrace)
            shorter = (visited) and (cost_to_child < backtrace[child][COST_INDEX])
            if (not visited) or shorter:
                if visited:
                    heur_from_child = backtrace[child][HEUR_INDEX]
                else:
                    heur_from_child = heuristic(child, problem)
                backtrace[child] = (state, action, cost_to_child, heur_from_child)
                child_node = SearchNode(child, cost_to_child,
                                        heur_from_child)
                fringe.push(child_node)
    raise Exception("There is no solution for this problem")


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
