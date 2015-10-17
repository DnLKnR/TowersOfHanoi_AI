##This file will contain the implementation for the towers of hanoi
from Stack import Stack
from Queue import Queue
import queue,copy,sys,timeit
from django.template.defaultfilters import length

class Towers_Of_Hanoi(object):
    
    def __init__(self, length=3, height=3, swap=False, explore=True):
        """This is the constructor for the Problem class. It specifies the initial state, and possibly a goal state, if there is a unique goal.  You can add other arguments if the need arises"""
        self.length     = length
        self.height     = height
        self.swap       = swap
        self.explore    = explore
        self.explored   = []
        
        self.__construct__(swap)
    
    def __construct__(self, swap):
        """This is the function that constructs the initial state and 
        the goal state for the towers of hanoi.  Note: One of the 
        Bidirectional's Towers of Hanoi setup needs the goal state and 
        the initial state swapped, thus there is an extra parameter to
        perform this action."""
        initial = []
        goal    = []
        for i in range(self.length):
            initial.append([])
            goal.append([])
        
        for i in range(self.height,0,-1):
            initial[0].append(i)
            goal[-1].append(i)
        
        if swap:
            self.initial    = goal
            self.goal       = initial
        else:
            self.initial    = initial
            self.goal       = goal
    
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        action = []
        if self.explore and self.is_explored(state):
            return action
        for i in range(self.length):
            if len(state[i]) > 0:
                for j in range(self.length):
                    if i == j:
                        continue
                    elif len(state[j]) == 0:
                        action.append([i,j])
                    elif state[i][-1] < state[j][-1]:
                        action.append([i,j])
        if self.explore:
            self.explored.insert(0,state)
        return action
    
    def copy(self, state):
        new_state = []
        for tower in state:
            new_tower = []
            for value in tower:
                new_tower.append(value)
            new_state.append(new_tower)
        return new_state
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state   = self.copy(state)
        i,j         = action
        value       = new_state[i].pop()
        
        new_state[j].append(value)
        
        return new_state
    
    def is_explored(self, state):
        for explored_state in self.explored:
            if self.compare(explored_state,state):
                return True
        return False
    
    def compare(self, state, other):
        for i,tower in enumerate(state):
            if len(other[i]) != len(tower):
                return False
            for j,value in enumerate(tower):
                if other[i][j] != value:
                    return False
        return True
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if self.compare(state, self.goal):
            return True
        else:
            return False


	
class Node(object):
	"""A node in a search tree. Contains a pointer to the parent (the node
	that this is a successor of) and to the actual state for this node. Note
	that if a state is arrived at by two paths, then there are two nodes with
	the same state.  Also includes the action that got us to this state"""

	def __init__(self, state, parent=None, action=None):
		"""Create a search tree Node, derived from a parent by an action.
		Update the node parameters based on constructor values"""
		self.state    = state
		self.parent   = parent
		self.action   = action
		self.depth    = 0
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


def bidirectional_search(problem, goal):
    # Start from first node of the problem Tree
    i_node  = Node(problem.initial)
    s_node  = Node(goal.initial)
    # Check if current node meets Goal_Test criteria
    if problem.compare(i_node.state,s_node.state):
        return top
    
    # Create a Queue to store all nodes of a particular level. Import QueueClass()
    initial,solution    = 0,        1
    explore             = [[i_node],[s_node]]
    frontier            = [[],      []]
    length              = [1,       1]
    
    ## QUESTION 3 NODE QUANTIFIER ##
    node_counter = 2
    
    #print_towers(node.state)
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while 0 not in length:
        #compare all parents from top and bottom against each other, 
        for init in explore[initial]:
            for sol in explore[solution]:
                # if two match, solution is found
                if problem.compare(init.state,sol.state):
                    print("Top Solution:\t",end="")
                    print_towers(init.state)
                    print("Bottom Solution: ",end="")
                    print_towers(sol.state)
                    print("Nodes Created:\t"+str(node_counter))
                    return [init,sol]
        
        #Generate all the initial side children
        length[initial] = 0
        for parent in explore[initial]:
            for child in parent.expand(problem):
                frontier[initial].append(child)
                length[initial] += 1
                node_counter += 1
        
        #Generate all the solution side children  
        length[solution] = 0
        for parent in explore[solution]:
            for child in parent.expand(goal):
                frontier[solution].append(child)
                length[solution] += 1
                node_counter += 1
        
        #Swap children to parent lists, then reset children
        explore    = frontier
        length      = [len(explore[initial]),len(explore[solution])]
        frontier    = [[],  []]
        
        
    return None
    
def breadth_first_search(problem):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state):
        return node
    # Create a Queue to store all nodes of a particular level. Import QueueClass()
    frontier    = [node]
    length      = 1
    
    ## QUESTION 3 NODE QUANTIFIER ##
    node_counter = 1
    
    print_towers(node.state)
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while length:
        # Remove from frontier, for analysis
        node = frontier.pop(0)
        length -= 1
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in node.expand(problem):

            ## QUESTION 3 NODE QUANTIFIER ##
            node_counter += 1

            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                print("Solution found: ")
                print_towers(child.state)
                ## QUESTION 3 NODE QUANTIFIER ##
                print("\n\nNodes Created:\t" + str(node_counter))

                return [child]
            # Add every new child to the frontier
            #print("Mediary: ")
            #print_towers(child.state)
            frontier.append(child)
            length += 1
            
    return None

def print_towers(towers):
    print(towers)
    print("_" * 2 * len(towers))
    for tower in towers:
        print("| ",end="")
        for value in tower:
            print(str(value) + " | ", end ="")
        print("")
    print("_" * 2 * len(towers))

def trace(solution):
    if solution == None:
        print("No solution exists: Parameter 1 is None-Type")
    elif len(solution) == 1:
        start = solution[0]
        actions = []
        while start != None:
            actions.insert(0, start.state)
            start = start.parent
        return actions
    else:
        start = [solution[0],solution[1].parent]
        actions = []
        while start[0] != None:
            actions.insert(0, start[0].state)
            start[0] = start[0].parent
        while start[1] != None:
            actions.append(start[1].state)
            start[1] = start[1].parent
        return actions
        
if __name__ == '__main__':
    #define base params
    LENGTH        = 3
    HEIGHT        = 4
    #Breadth-First-Search
    PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT)
    t1 = timeit.Timer('breadth_first_search(PROBLEM)',
                      setup="from __main__ import breadth_first_search, Towers_Of_Hanoi, PROBLEM")
    print("BFS:\t\t" + str(t1.timeit(1)))
    #Perform Trace, store actions
    PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT)
    BFS_ACTIONS = trace(breadth_first_search(PROBLEM))
    #Bidirectional Breadth-First-Search
    PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT)
    GOAL    = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT,swap=True)
    t2 = timeit.Timer('bidirectional_search(PROBLEM, GOAL)',
                      setup="from __main__ import bidirectional_search, Towers_Of_Hanoi, PROBLEM, GOAL")
    print("Bidirectional:\t" + str(t2.timeit(1)))
    PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT)
    GOAL    = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT,swap=True)
    BI_ACTIONS = trace(bidirectional_search(PROBLEM, GOAL))
    print("Bidirectional vs Breadth-First-Search Comparison")
    if len(BI_ACTIONS) != len(BFS_ACTIONS):
        print("Length Test failed\nBidirectional:\t\t"      + str(len(BI_ACTIONS)) + 
                                "\nBreadth-First-Search:\t" + str(len(BFS_ACTIONS)))
        print(BI_ACTIONS)
        print(BFS_ACTIONS)
    else:
        mismatch = 0
        for i in range(len(BI_ACTIONS)):
            if not PROBLEM.compare(BI_ACTIONS[i], BFS_ACTIONS[i]):
                mismatch += 1
        if mismatch:
            print("Match Test failed\n\tMismatch Count:\t" + str(mismatch))
            print(BI_ACTIONS)
            print(BFS_ACTIONS)
        else:
            print("All tests executed correctly")
    

