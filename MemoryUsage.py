from TowersOfHanoi import Towers_Of_Hanoi, breadth_first_search, bidirectional_search, trace
import timeit, argparse, sys

## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program checks the memory usage for Towers of Hanoi in terms of Nodes")
parser.add_argument("--min",    metavar="INT", dest="min",    nargs=1, default=[3], type=int, help="Minimum Tower Height for Analysis (default is 3)")
parser.add_argument("--max",    metavar="INT", dest="max",    nargs=1, default=[6], type=int, help="Maximum Tower Height for Analysis (default is 6)")
parser.add_argument("--towers", metavar="INT", dest="towers", nargs=1, default=[3], type=int, help="Number of Towers (default is 3)")
parser.add_argument("--log", metavar="STRING", dest="file",   nargs=1, default=[""],type=str, help="Specify a log file (default will print to terminal)")
parser.add_argument("--no-explore",dest="explore",action='store_false',  default=True,help="Disable using explored set")


if __name__ == '__main__':
    ## PARSE COMMAND LINE ARGUMENTS AND STORE VALUES IN inputs OBJECT ##
    inputs = Inputs()
    parser.parse_args(sys.argv[1:], namespace=inputs)
    ## GET COMMAND LINE ARGUMENTS ##
    LENGTH  = inputs.towers[0]
    LOW     = inputs.min[0]
    HIGH    = inputs.max[0]
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
    extension = LOGFILE.split(".")[-1]
    if LOGFILE != "" and extension not in ["txt","log"]:
        print("Invalid Log Extension: Log files should either be of *.txt or *.log")
        invalid += 1
    if invalid:
        print("\n...Program Exiting")
        sys.exit(1)
        
    #INITIALIZE GLOBALS
    _BFS,_BI    = 0, 1
    NODE_OF     = [[],[]]
    HEIGHT      = range(LOW, HIGH + 1)
    
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
    table  = "Towers Of Hanoi Test: Memory Usage Analysis\n"
    seper  = "-" * len(table) + "\n"
    table += seper
    table += "\nTEST SETTINGS\n"
    table += "   Use Explored Set:\t" + str(EXPLORE) + "\n"
    table += "   Number Of Towers:\t" + str(LENGTH) + "\n"
    table += "\nTEST RESULTS (by height)\n"
    for i,h in enumerate(HEIGHT):
        table += "  For Height = " + str(h) + ":\n"
        table += "\tBreadth-First-Search sizes:\n"
        table += "\t  Graph:\t\t"        + str(NODE_OF[_BFS][i][0]) + "\n"
        if EXPLORE:
            table += "\t  Explored:\t\t" + str(NODE_OF[_BFS][i][1]) + "\n"
        table += "\t  Frontier Max:\t"   + str(NODE_OF[_BFS][i][2]) + "\n"
        table += "\tBidirectional sizes:\n"
        table += "\t  Graph:\t\t"        + str(NODE_OF[_BI][i][0]) + "\n"
        if EXPLORE:
            table += "\t  Explored:\t\t" + str(NODE_OF[_BI][i][1]) + "\n"
        table += "\t  Frontier Max:\t"   + str(NODE_OF[_BI][i][2]) + "\n"
    
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
    
    
