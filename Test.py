from TowersOfHanoi import Towers_Of_Hanoi, breadth_first_search, bidirectional_search, trace
import timeit, argparse

## ARGPARSE ARGUMENTS ##
LENGTH  = 3
HEIGHT  = 10






if __name__ == '__main__':
    
    
    PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT)
    BFS_STATES = trace(breadth_first_search(PROBLEM))
    #Bidirectional Breadth-First-Search
    PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT)
    GOAL    = Towers_Of_Hanoi(length=LENGTH,height=HEIGHT,swap=True)
    BI_STATES = trace(bidirectional_search(PROBLEM, GOAL))
    print("Bidirectional vs Breadth-First-Search Comparison")
    if len(BI_STATES) != len(BFS_STATES):
        print("Length Test failed\nBidirectional:\t\t"      + str(len(BI_STATES)) + 
                                "\nBreadth-First-Search:\t" + str(len(BFS_STATES)))
        print(BI_STATES)
        print(BFS_STATES)
    else:
        mismatch = 0
        for i in range(len(BI_STATES)):
            if not PROBLEM.compare(BI_STATES[i], BFS_STATES[i]):
                mismatch += 1
        if mismatch:
            print("Match Test failed\n\tMismatch Count:\t" + str(mismatch))
            print(BI_STATES)
            print(BFS_STATES)
        else:
            print("All tests executed correctly")
            
