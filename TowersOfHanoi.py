class Towers_Of_Hanoi(object):
    
    def __init__(self, length=3, height=3, swap=False, explore=True):
        """This is the constructor for the Problem class. It specifies 
        the initial state, and possibly a goal state, if there is a 
        unique goal.  You can add other arguments if the need arises"""
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
        #If swap is true, swap the two states 
        #so that it can be worked backwards
        if swap:
            self.initial    = goal
            self.goal       = initial
        #Else maintain the current setup
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
                    #If the tower is empty, add a ring
                    elif len(state[j]) == 0:
                        action.append([i,j])
                    #If the tower's ring is greater than currents, add the ring
                    elif state[i][-1] < state[j][-1]:
                        action.append([i,j])
        # Add the state to the front of the explored set
        if self.explore:
            self.explored.insert(0,state)
        # Return the actions generated
        return action
    
    def copy(self, state):
        """Returns a copy of the multidimensional array that is
        the towers of hanoi board state.  The parameter state is
        the multidimensional array being copied"""
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
        """Check if the state passed in as a parameter is already
        a part of the explored set."""
        for explored_state in self.explored:
            if self.compare(explored_state,state):
                return True
        return False
    
    def compare(self, state, other):
        """Compare two states (state and other) to see if they are
        the same in configuration.  If they are, return True, else
        is they are different, return false"""
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


def bidirectional_search(problem, goal,return_mem_usage=False):
    """This function uses two different problems, one starting from
    the goal, the other starting from the problem. When the two sides
    meet at an equivalent node, a solution is found. The parameter 
    return_mem_usage allows for appending to the answer the memory
    usage metrics"""
    # Initialize variables and lists
    initial,solution    = 0,1
    explore             = [[Node(problem.initial)],[Node(goal.initial)]]
    frontier            = [[],[]]
    length              = [1,1]
    # Check if problem is equivalent to goal
    if problem.compare(explore[initial][0].state, explore[solution][0].state):
        return [explore[initial][0], explore[solution][0]]
    
    ## MEMORY USAGE QUANTIFIER ##
    node_counter    = 2
    max_length      = 2
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while 0 not in length:
        
        #Generate all the initial side children
        length[initial] = 0
        for parent in explore[initial]:
            for child in parent.expand(problem):
                frontier[initial].append(child)
                length[initial] += 1
                ## MEMORY USAGE QUANTIFIER ##
                node_counter += 1
        
        #Update max length if new total length is larger
        if max_length < length[initial] + length[solution]:
            max_length = length[initial] + length[solution]
            
        #Swap initial-side children to parent lists, then reset children
        explore[initial]    = frontier[initial]
        frontier[initial]   = []
        
        #compare all parents from problem-side and bottom-side
        for init in explore[initial]:
            for sol in explore[solution]:
                # if two match, solution is found
                if problem.compare(init.state,sol.state):
                    answer = [init,sol]
                    #Include memory usage values if requested
                    if return_mem_usage:
                        explored_length = len(problem.explored) + len(goal.explored)
                        answer.append([node_counter, explored_length, max_length])
                    
                    return answer 
        
        #Generate all the solution side children  
        length[solution] = 0
        for parent in explore[solution]:
            for child in parent.expand(goal):
                frontier[solution].append(child)
                length[solution] += 1
                ## MEMORY USAGE QUANTIFIER ##
                node_counter += 1
        
        #Update max length if new total length is larger
        if max_length < length[initial] + length[solution]:
            max_length = length[initial] + length[solution]
        
        #Swap solution-side children to parent lists, then reset children
        explore[solution]   = frontier[solution]
        frontier[solution]  = []
                
    return None
    
def breadth_first_search(problem,return_mem_usage=False):
    """breadth_first_search takes atleast one parameter which is
    the problem object containing a problem in which a solution
    can be search for.  parameter return_mem_usage adds onto the
    returned answer the memory usage details"""
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state):
        return node
    # The queue that will be used is pythons built-in list
    frontier    = [node]
    length      = 1
    
    ## MEMORY USAGE QUANTIFIER ##
    node_counter = 1
    max_length   = 1
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while length:
        # If max_length is smaller than current length, update it
        if max_length < length:
            max_length = length
        # Remove from frontier, for analysis
        node = frontier.pop(0)
        length -= 1
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in node.expand(problem):
            ## MEMORY USAGE QUANTIFIER ##
            node_counter += 1

            # If child node meets Goal_Test criteria, we've found our answer
            if problem.goal_test(child.state):
                answer = [child]
                if return_mem_usage:
                    explored_length = len(problem.explored)
                    answer.append([node_counter,explored_length,max_length])
                
                return answer
            #if goal critieria was not met, add child and continue forward
            frontier.append(child)
            length += 1
        
    return None

def print_towers(towers):
    """This function prints the towers in basic,
    but readable format"""
    print(towers)
    print("_" * 2 * len(towers))
    for tower in towers:
        print("| ",end="")
        for value in tower:
            print(str(value) + " | ", end ="")
        print("")
    print("_" * 2 * len(towers))

def trace(solution):
    """This function traces the return value of either the
    breadth_first_search or bidirectional_search functions.
    This function collects all the states from the initial
    state to the goal state"""
    if solution == None:
        print("No solution exists: Parameter 1 is None-Type")
    # Breadth-First-Search 
    elif len(solution) == 1:
        start = solution[0]
        actions = []
        while start != None:
            actions.insert(0, start.state)
            start = start.parent
        return actions
    # Bidirectional Search
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
    

