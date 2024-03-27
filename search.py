from util import Stack, Queue, PriorityQueue
from game import Directions
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def getPath(start, end, connections):
    current = end
    queue = Queue()

    while current != start:
        queue.push(connections[current][1])
        current = connections[current][0]

    return queue.list

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    stack       = Stack()
    visited     = []
    connections = {}

    start  = problem.getStartState()
    connections[start] = None

    stack.push(start)

    while not stack.isEmpty():
        current = stack.pop()

        if problem.isGoalState(current):
            break

        if current not in visited:
            visited.append(current)
            for state, direction, _ in problem.getSuccessors(current):
                if state not in visited:
                    connections[state] = (current, direction)
                    stack.push(state)

    return getPath(start, current, connections)

def breadthFirstSearch(problem: SearchProblem):
    queue = Queue()
    visited = []
    connections = {}

    start = problem.getStartState()
    connections[start] = None

    queue.push(start)
    visited.append(start)

    while not queue.isEmpty():
        current = queue.pop()

        if problem.isGoalState(current):
            break

        for state, direction, _ in problem.getSuccessors(current):
            if state not in visited:
                visited.append(state)
                connections[state] = (current, direction)
                queue.push(state)

    return getPath(start, current, connections)


def uniformCostSearch(problem: SearchProblem):
    pqueue = PriorityQueue()
    costs = {}                             # (state : minumum current cost to get to state)
    connections = {}                       # (cur : (prev, direction)) pairs

    start = problem.getStartState()
    connections[start] = None              # no previous state

    pqueue.push(start, 0)
    costs[start] = 0

    while not pqueue.isEmpty():
        current = pqueue.pop()

        if problem.isGoalState(current):
            break

        for state, direction, cost in problem.getSuccessors(current):
            path_cost = cost + costs[current]

            # only enqueue and update if not visited or current cost < previous cost
            if state not in costs or path_cost < costs[state]:
                connections[state] = (current, direction)
                costs[state] = path_cost
                pqueue.update(state, path_cost)


    return getPath(start, current, connections)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    pqueue = PriorityQueue()
    costs = {}                             # (state : minumum current cost to get to state)
    connections = {}                       # (cur : (prev, direction)) pairs

    start = problem.getStartState()
    connections[start] = None              # no previous state

    pqueue.push(start, 0)                  # no reason to calculate start heuristic
    costs[start] = 0

    while not pqueue.isEmpty():
        current = pqueue.pop()

        if problem.isGoalState(current):
            break

        for state, direction, cost in problem.getSuccessors(current):
            path_cost = cost + costs[current]

            # only enqueue and update if not visited or current cost < previous cost
            if state not in costs or path_cost < costs[state]:
                connections[state] = (current, direction)
                costs[state] = path_cost
                pqueue.update(state, path_cost + heuristic(state, problem))

    return getPath(start, current, connections)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
