from TowersOfHanoi import Towers_Of_Hanoi, breadth_first_search, bidirectional_search, trace
import timeit, argparse, sys

## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program checks the run time for Towers of Hanoi in terms of seconds")
parser.add_argument("--min",       metavar="INT", dest="min",    nargs=1, default=[3], type=int, help="Minimum Tower Height for Analysis (default is 3)")
parser.add_argument("--max",       metavar="INT", dest="max",    nargs=1, default=[6], type=int, help="Maximum Tower Height for Analysis (default is 6)")
parser.add_argument("--runs",      metavar="INT", dest="runs",   nargs=1, default=[10],type=int, help="Number of executions per Height (default is 10)")
parser.add_argument("--towers",    metavar="INT", dest="towers", nargs=1, default=[3], type=int, help="Number of Towers (default is 3)")
parser.add_argument("--log",    metavar="STRING", dest="file",   nargs=1, default=[""],type=str, help="Specify a log file (default will print to terminal)")
parser.add_argument("--no-explore",dest="explore",action='store_false',  default=True,help="Disable using explored set")


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
    ## CHECK VALIDITY OF COMMAND LINE ARGS ##
    invalid = 0
    if LOW > HIGH:
        print("Invalid Min-Max Range: Minimum height cannot be greater than maximum")
        invalid += 1
    if LENGTH < 3:
        print("Invalid Tower Count: Number of Towers must be greater than 2 to be solvable")
        invalid += 1
    if COUNT < 1:
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
    HEIGHT      = range(LOW, HIGH + 1)
    
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
    table     = "Towers Of Hanoi Test: Run-Time Analysis\n"
    seper  = "-" * len(table) + "\n"
    table += seper
    table   += "\nTEST SETTINGS\n"
    table   += "\tUse Explored Set:\t" + str(EXPLORE) + "\n"
    table   += "\tNumber Of Towers:\t" + str(LENGTH) + "\n"
    table   += "\tNumber Of Executions:\t" + str(COUNT) + "\n"
    table   += "\nTEST RESULTS (by height)\n"
    for i,h in enumerate(HEIGHT):
        table += "\tFor Height = " + str(h) + ":\n"
        table += "\t\tBreadth-First-Search:\t" + str(TIME_OF[_BFS][i]) + "s\n" 
        table += "\t\tBidirectional:\t\t\t" + str(TIME_OF[_BI][i]) + "s\n\n"
    
    table += "\n" + seper + "\n"
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
        print("Results were output to: " + LOGFILE)
