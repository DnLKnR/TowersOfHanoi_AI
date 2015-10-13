##This file will contain the implementation for the towers of hanoi
from Stack import Stack

import queue,copy,sys

"""This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""
class Problem(object):
    
    def __init__(self, initial, goal=None):
        """This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""
        self.initial = initial
        self.goal = goal
    
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        action = []
        length = len(state)
        for i in range(length):
            if state[i].get_size() > 0:
                for j in range(length):
                    if i == j:
                        continue
                    elif state[j].get_size() == 0:
                        action.append([i,j])
                    elif state[i].peek() < state[j].peek():
                        action.append([i,j])
        print(action)
        return action
	
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state = []
        for tower in state:
            new_tower = tower.copy()
            new_state.append(new_tower)
        i,j = action
        value = new_state[i].pop()
        new_state[j].push(value)
        return new_state

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        height = 3
        if state[-1].get_size() != height:
            return False
        last_tower = state[-1].to_array()    
        for i in range(1,height + 1):
            if last_tower[i - 1] != i:
                return False
        return True
		
class Node(object):
	"""A node in a search tree. Contains a pointer to the parent (the node
	that this is a successor of) and to the actual state for this node. Note
	that if a state is arrived at by two paths, then there are two nodes with
	the same state.  Also includes the action that got us to this state"""

	def __init__(self, state, parent=None, action=None):
		"""Create a search tree Node, derived from a parent by an action.
		Update the node parameters based on constructor values"""
		self.state = state
		self.parent = parent
		self.action = action
		self.depth = 0
		# If depth is specified then depth of node will be 1 more than the depth of parent
		if parent:
			self.depth = parent.depth + 1

	def expand(self, problem):
		# List the nodes reachable in one step from this node.
		return [self.child_node(problem, action)
				for action in problem.actions(self.state)]

	def child_node(self, problem, action):
		next = problem.result(self.state, action)
		return Node(next, self, action)


def bidirectional_search(problem, solution):
    pass
    
def breadth_first_search(problem):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state):
        return node
    # Create a Queue to store all nodes of a particular level. Import QueueClass()
    frontier=queue.Queue()
    frontier.put_nowait(node)

    ## QUESTION 3 NODE QUANTIFIER ##
    ## node_counter = 1
    
    print_towers(node.state)
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while frontier:
        # if queue is empty, there is no solution
        if frontier.qsize() == 0:
            return None
        # Remove from frontier, for analysis
        node = frontier.get_nowait()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in node.expand(problem):

            ## QUESTION 3 NODE QUANTIFIER ##
            ## node_counter += 1

            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                print("Solution found: ")
                print_towers(child.state)
                ## QUESTION 3 NODE QUANTIFIER ##
                ## print("\n\nNodes Created: " + str(node_counter))

                return child
            # Add every new child to the frontier
            print("Mediary: ")
            print_towers(child.state)
            frontier.put_nowait(child)
    return None

def print_towers(towers):
    for tower in towers:
        print("| ",end="")
        tower.printStack()


def construct(number_towers=3,height=3):
    towers = []
    for i in range(number_towers):
        towers.append(Stack())
    for i in range(height,0,-1):
        towers[0].push(i)
    return towers


breadth_first_search(Problem(construct(3,3)))



