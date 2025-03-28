import sys 
from collections import deque
from utils import *

class Problem:
    """The abstract class for a formal problem. You should subclass 
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions"""

    def __init__(self, initial, goal =None):
        """The constructor specifies the initial state,a nd possibly a goal 
        state, if there is aunique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial 
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given state
        The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an 
        iterator, rather than building them all at once"""
        raise NotImplementedError
    
    def result(self, state, action):
        """Return the state that results from ecevuting the given
        action in the given state. The action must be one of 
        self.actions(state)"""
        raise NotImplementedError
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the 
        state to self.goal or checks for state in self.goal if it is a list
        as specified in the constructor. Ovveride this method if checking against a single self.goal is not enough"""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal
        
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from state1 via ction, assuming cost c to get up to state 1.
        If the problem is such that the path doesnt matter, this function will only look at state2
        If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path"""
        return c + 1
    
    def value(self, state):
        """For optimization problems, each state has a value/ Hill Climbing and realted algortithms try to maximize this value"""
        raise NotImplementedError
    
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node that this is a successor of)
    and to the actual state for this node. Note that if a state is arrived at by tow paths, then there are two nodes
    with the same state. Also includes the action that got us to this state, and the total path_cost (also know as g )
    to reach the node. Other function s may add an f and h value; see best-first-graph-search and astar_search for an explanation 
    of how the f and h values are handled. You will not need to subclass this class"""

    def __init__(self, state, parent = None, action = None, path_cost = 0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action 
        self.path_cost = path_cost
        self.depth = 0
        if parent: 
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)
    
    def __lt__(self, node):
        return self.state < node.state
    
    def expand(self, problem):
        """List the nodes reachable in one step from this node"""
        return [self.child_node(problem, action)
        for action in problem.actions(self.state)]
    
    def child_node(self, problem, action):
        next_state = problem.result(self.state, action )
        mext_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node""" 
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
    
    def __hash__(self):
        return hash(self.state)

    def best_first_graph_search(problem, f, display = False):
        """Search the nodes with the lowest f score first.
        You specify the function f(node) that you want to minimize, for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is asubtlety: the line"f = memoize(f, 'f') means that the f values
        will be cached on the nodes as they are computed. So after doing a best frist search you can examine the f values of the path returned"""

        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier),
                    "paths remain in the frontier")
                return node
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        return None

        
