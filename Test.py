from TowersOfHanoi import Towers_Of_Hanoi, breadth_first_search, bidirectional_search, trace
import timeit, argparse, sys

## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program checks the run time for Towers of Hanoi in terms of seconds")
parser.add_argument("--min",    metavar="INT", dest="min",    nargs=1, default=[3], type=int,  help="Minimum Tower Height for Analysis (default is 3)")
parser.add_argument("--max",    metavar="INT", dest="max",    nargs=1, default=[10], type=int, help="Maximum Tower Height for Analysis (default is 6)")
parser.add_argument("--runs",   metavar="INT", dest="runs",   nargs=1, default=[10],type=int,  help="Number of executions per Height (default is 10)")
parser.add_argument("--towers", metavar="INT", dest="towers", nargs=1, default=[3], type=int,  help="Number of Towers (default is 3)")
parser.add_argument("--log",    metavar="FILE", dest="file",  nargs=1, default=[""],type=str,  help="Specify a log file (default will print to terminal)")
parser.add_argument("--no-explore",dest="explore",action='store_false',default=True, help="Disable using explored set")
parser.add_argument("-A",          dest="all",    action='store_true', default=False,help="Execute Run-Time, Memory Usage, and Solution analysis")
parser.add_argument("-rt",         dest="rt",     action='store_true', default=False,help="Execute Run-Time analysis")
parser.add_argument("-mu",         dest="mu",     action='store_true', default=False,help="Execute Memory Usage analysis")


if __name__ == '__main__':
    ## PARSE COMMAND LINE ARGUMENTS AND STORE VALUES IN inputs OBJECT ##
    inputs = Inputs()
    parser.parse_args(sys.argv[1:], namespace=inputs)
    ## GET COMMAND LINE ARGUMENTS ##
    LENGTH  = inputs.towers[0]
    LOW     = inputs.min[0]
    HIGH    = inputs.max[0]
    COUNT   = inputs.runs[0]
    EXPLORE = inputs.explore
    LOGFILE = inputs.file[0]
    RUN_ALL = inputs.all
    RUN_RT  = inputs.rt
    RUN_MU  = inputs.mu
    ## CHECK VALIDITY OF COMMAND LINE ARGS ##
    invalid = 0
    if LOW > HIGH:
        print("Invalid Min-Max Range: Minimum height cannot be greater than maximum")
        invalid += 1
    if LENGTH < 3:
        print("Invalid Tower Count: Number of Towers must be greater than 2 to be solvable")
        invalid += 1
    if COUNT < 1 and (RUN_ALL or RUN_RT):
        print("Invalid Execution Count: Number of executions must be greater than 1 to actually run")
        invalid += 1
    extension = LOGFILE.split(".")[-1]
    if LOGFILE != "" and extension not in ["txt","log"]:
        print("Invalid Log Extension: Log files should either be of *.txt or *.log")
        invalid += 1
    if invalid:
        print("\n...Program Exiting")
        sys.exit(1)
    
    #INITIALIZE GLOBALS
    _BFS,_BI    = 0, 1
    TIME_OF     = [[],[]]
    NODE_OF     = [[],[]]
    HEIGHT      = range(LOW, HIGH + 1)
    
    ## FORMAT OUTPUT FOR ANALYSIS HEADER ##
    table  = "Towers Of Hanoi Analysis\n"
    seper  = "-" * len(table) + "\n"
    table += seper
    table += "\nTEST SETTINGS\n"
    table += "\tUse Explored Set:\t\t" + str(EXPLORE) + "\n"
    table += "\tNumber Of Towers:\t\t" + str(LENGTH) + "\n"
    table += "\tNumber Of Executions:\t" + str(COUNT) + "\n"
    table += "\tTower Height Range:\t\t" + str(LOW) + " to " + str(HIGH) + "\n\n"
    
    if RUN_ALL or RUN_RT:
        ## EXECUTE BREADTH FIRST SEARCH RUN-TIME ANALYSIS ##
        for h in HEIGHT:
            ## SETUP AND RUN TIMEIT INSTANCE FOR RUNTIME FOR HEIGHT h over COUNT repetitions ##
            t = timeit.Timer('breadth_first_search(Towers_Of_Hanoi(length=LENGTH,height=h,explore=EXPLORE))',
                              setup="from __main__ import Towers_Of_Hanoi, breadth_first_search, LENGTH, h, EXPLORE")
            ## GET AND COMPUTE AVERAGE RUN-TIME THEN STORE IT ##
            average_time = round(t.timeit(COUNT)/COUNT, 5)
            TIME_OF[_BFS].append(average_time)
        
        ## EXECUTE BIDIRECTIONAL SEARCH RUN-TIME ANALYSIS ##
        for h in HEIGHT:
            ## SETUP AND RUN TIMEIT INSTANCE FOR RUNTIME FOR HEIGHT h over COUNT repetitions ##
            t = timeit.Timer('bidirectional_search(Towers_Of_Hanoi(length=LENGTH,height=h,explore=EXPLORE),' +
                                                  'Towers_Of_Hanoi(length=LENGTH,height=h,swap=True,explore=EXPLORE))',
                              setup="from __main__ import Towers_Of_Hanoi, bidirectional_search, LENGTH, h, EXPLORE")
            ## GET AND COMPUTE AVERAGE RUN-TIME THEN STORE IT ##
            average_time = round(t.timeit(COUNT)/COUNT, 5)
            TIME_OF[_BI].append(average_time)
        
        ## CREATE OUTPUT RUN-TIME ANALYSIS ##
        table += seper
        table += "Run-Time Test Results\n\n"
        for i,h in enumerate(HEIGHT):
            table += "\tFor Height = " + str(h) + ":\n"
            table += "\t\tBreadth-First-Search:\t" + str(TIME_OF[_BFS][i]) + "s\n" 
            table += "\t\tBidirectional:\t\t\t" + str(TIME_OF[_BI][i]) + "s\n\n"
    
    if RUN_ALL or RUN_MU:
        ## EXECUTE BREADTH FIRST SEARCH MEMORY-USAGE ANALYSIS ##
        for h in HEIGHT:
            ## SETUP AND STORE INSTANCE FOR MEMORY USAGE FOR HEIGHT h ##
            answer = breadth_first_search(Towers_Of_Hanoi(length=LENGTH,height=h,explore=EXPLORE),
                                             return_mem_usage=True)
            ## GET AND STORE MEMORY USAGE METRICS ##
            mem_usage = answer[1]
            NODE_OF[_BFS].append(mem_usage)
        
        ## EXECUTE BIDIRECTIONAL SEARCH MEMORY-USAGE ANALYSIS ##
        for h in HEIGHT:
            ## SETUP AND STORE INSTANCE FOR MEMORY USAGE FOR HEIGHT h ##
            answer = bidirectional_search(Towers_Of_Hanoi(length=LENGTH,height=h,explore=EXPLORE),
                                          Towers_Of_Hanoi(length=LENGTH,height=h,swap=True,explore=EXPLORE),
                                          return_mem_usage=True)
            
            ## GET AND STORE MEMORY USAGE METRICS ##
            mem_usage = answer[2]
            NODE_OF[_BI].append(mem_usage)
        
        ## FORMAT OUTPUT FOR MEMORY USAGE ##
        table += seper
        table += "Memory Usage Test Results\n\n"
        for i,h in enumerate(HEIGHT):
            table += "\tFor Height = " + str(h) + ":\n"
            table += "\t\tBreadth-First-Search sizes:\n"
            table += "\t\t  Graph:\t\t"        + str(NODE_OF[_BFS][i][0]) + "\n"
            if EXPLORE:
                table += "\t\t  Explored:\t\t" + str(NODE_OF[_BFS][i][1]) + "\n"
            table += "\t\t  Frontier Max:\t"   + str(NODE_OF[_BFS][i][2]) + "\n"
            table += "\t\tBidirectional sizes:\n"
            table += "\t\t  Graph:\t\t"        + str(NODE_OF[_BI][i][0]) + "\n"
            if EXPLORE:
                table += "\t\t  Explored:\t\t" + str(NODE_OF[_BI][i][1]) + "\n"
            table += "\t\t  Frontier Max:\t"   + str(NODE_OF[_BI][i][2]) + "\n"
        table += seper
    
    ## CHECK PATH TO SOLUTION SIZE ##
    for h in HEIGHT:
        PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=h)
        BFS_STATES = trace(breadth_first_search(PROBLEM))
        #Bidirectional Breadth-First-Search
        PROBLEM = Towers_Of_Hanoi(length=LENGTH,height=h)
        GOAL    = Towers_Of_Hanoi(length=LENGTH,height=h,swap=True)
        BI_STATES = trace(bidirectional_search(PROBLEM, GOAL))
        
        table += "Trace Solution Path Analysis"
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
                
    if LOGFILE == "":
        print(table)
    else:
        #If file exists, append to it, otherwise create it
        try:
            log = open(LOGFILE, 'a')
        except:
            log = open(LOGFILE, 'w')
        log.write(table)
        log.close()
        print("Results output to " + LOGFILE)
            
