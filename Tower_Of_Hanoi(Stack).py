from Stack import Stack
from Queue import Queue
import queue,copy,sys,timeit

"""This is where the problem is defined. Initial state, goal state and other information that can be got from the problem"""
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
            initial.append(Stack())
            goal.append(Stack())
        for i in range(self.height,0,-1):
            initial[0].push(i)
            goal[-1].push(i)
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
            if state[i].get_size() > 0:
                for j in range(self.length):
                    if i == j:
                        continue
                    elif state[j].is_empty():
                        action.append([i,j])
                    elif state[i].peek() < state[j].peek():
                        action.append([i,j])
        if self.explore:
            self.explored.append(state)
        return action
    
    def copy(self, state):
        new_state = []
        for tower in state:
            new_tower = tower.copy()
            new_state.append(new_tower)
        return new_state
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        new_state   = self.copy(state)
        i,j         = action
        value       = new_state[i].pop()
        
        new_state[j].push(value)
        
        return new_state
    
    def is_explored(self, state):
        for explored_state in self.explored[::-1]:
            if self.compare(explored_state,state):
                return True
        return False
    
    def compare(self, state, other):
        for i in range(self.length):
            if not state[i].compare(other[i]):
                return False
        return True
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough.
        This must be written by students"""
        if not self.compare(state, self.goal):
            return False
        return True
    
def bidirectional_search(problem):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state):
        return node
    # Create a Queue to store all nodes of a particular level. Import QueueClass()
    frontier = Stack()
    frontier.queue(node)

    ## QUESTION 3 NODE QUANTIFIER ##
    node_counter = 1
    
    #print_towers(node.state)
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while frontier:
        # if queue is empty, there is no solution
        if frontier.get_size() == 0:
            return None
        # Remove from frontier, for analysis
        node = frontier.pop()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in node.expand(problem):

            ## QUESTION 3 NODE QUANTIFIER ##
            node_counter += 1

            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                #print("Solution found: ")
                #print_towers(child.state)
                ## QUESTION 3 NODE QUANTIFIER ##
                #print("\n\nNodes Created: " + str(node_counter))

                return child
            # Add every new child to the frontier
            #print("Mediary: ")
            #print_towers(child.state)
            frontier.queue(child)
    return None
 
def breadth_first_search(problem):
    # Start from first node of the problem Tree
    node = Node(problem.initial)
    # Check if current node meets Goal_Test criteria
    if problem.goal_test(node.state):
        return node
    # Create a Queue to store all nodes of a particular level. Import QueueClass()
    frontier = Queue()
    frontier.queue(node)

    ## QUESTION 3 NODE QUANTIFIER ##
    node_counter = 1
    
    #print_towers(node.state)
    # Loop until all nodes are explored(frontier queue is empty) or Goal_Test criteria are met
    while frontier:
        # if queue is empty, there is no solution
        if frontier.get_size() == 0:
            return None
        # Remove from frontier, for analysis
        node = frontier.pop()
        # Loop over all children of the current node
        # Note: We consider the fact that a node can have multiple child nodes here
        for child in node.expand(problem):

            ## QUESTION 3 NODE QUANTIFIER ##
            node_counter += 1

            # If child node meets Goal_Test criteria
            if problem.goal_test(child.state):
                #print("Solution found: ")
                #print_towers(child.state)
                ## QUESTION 3 NODE QUANTIFIER ##
                #print("\n\nNodes Created: " + str(child.state))

                return child
            # Add every new child to the frontier
            #print("Mediary: ")
            #print_towers(child.state)
            frontier.queue(child)
    return None


def print_towers(towers):
    print("_" * 2 * len(towers))
    for tower in towers:
        print("| ",end="")
        tower.print_stack()
    print("_" * 2 * len(towers))

if __name__ == '__main__':
    
    t1 = timeit.Timer('breadth_first_search(Towers_Of_Hanoi2(length=3,height=8))',setup="from __main__ import breadth_first_search, Towers_Of_Hanoi2")
    print("My Stack: " + str(t1.timeit(10)/10))
    t2 = timeit.Timer('bidirectional_search(Towers_Of_Hanoi(length=3,height=8))',setup="from __main__ import bidirectional_search, Towers_Of_Hanoi")
    print("QueueClass: " + str(t2.timeit(10)/10))