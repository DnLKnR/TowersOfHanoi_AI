from TowersOfHanoi import Towers_Of_Hanoi, breadth_first_search, bidirectional_search, trace
import timeit, argparse, sys

## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program checks the run time for Towers of Hanoi in terms of seconds")
parser.add_argument("--min",    metavar="INT", dest="min",    nargs=1, default=[3], type=int,  help="Minimum Tower Height for Analysis (default is 3)")
parser.add_argument("--max",    metavar="INT", dest="max",    nargs=1, default=[7], type=int, help="Maximum Tower Height for Analysis (default is 6)")
parser.add_argument("--runs",   metavar="INT", dest="runs",   nargs=1, default=[5],type=int,  help="Number of executions per Height (default is 10)")
parser.add_argument("--towers", metavar="INT", dest="towers", nargs=1, default=[3], type=int,  help="Number of Towers (default is 3)")
parser.add_argument("--log",    metavar="FILE", dest="file",  nargs=1, default=[""],type=str,  help="Specify a log file (default will print to terminal)")
parser.add_argument("--no-explore",dest="explore",action='store_false',default=True,  help="Disable using explored set")
parser.add_argument("-sp",          dest="sp",    action='store_true', default=False,help="Execute Solution Path analysis")
parser.add_argument("-rt",         dest="rt",     action='store_true', default=False, help="Execute Run-Time analysis")
parser.add_argument("-mu",         dest="mu",     action='store_true', default=False, help="Execute Memory Usage analysis")

class Mem_Usage:
    def __init__(self, towers, heights, explore):
        self.towers  = towers
        self.heights = heights
        self.explore = explore
        
    def get_analysis(self):
        '''This function generates the analysis for the memory usage in terms
        of nodes.  This function returns in the form of a string.'''
        MemInfo_of = [[],[]]
        BFS,BI    = 0, 1
        ## EXECUTE BREADTH FIRST SEARCH AND BIDIRECTIONAL MEMORY-USAGE ANALYSIS ##
        for h in self.heights:
            ## SETUP AND STORE INSTANCE FOR MEMORY USAGE FOR HEIGHT h ##
            answer_bfs = breadth_first_search(Towers_Of_Hanoi(length=self.towers,height=h,explore=self.explore),
                                              return_mem_usage=True)
            ## GET AND STORE MEMORY USAGE METRICS ##
            BFS_mem = answer_bfs[-1]
            MemInfo_of[BFS].append(BFS_mem)
            
            answer_bi = bidirectional_search(Towers_Of_Hanoi(length=self.towers,height=h,explore=self.explore),
                                             Towers_Of_Hanoi(length=self.towers,height=h,swap=True,explore=self.explore),
                                             return_mem_usage=True)
            BI_mem  = answer_bi[-1]
            MemInfo_of[BI].append(BI_mem)
            
        
        ## FORMAT ANALYSIS FOR MEMORY USAGE ##
        analysis = "Memory Usage Test Results\n\n"
        for i,h in enumerate(self.heights):
            analysis += "\tFor Height = " + str(h) + ":\n"
            analysis += "\t\tBreadth-First-Search sizes:\n"
            analysis += "\t\t  Graph:\t\t"        + str(MemInfo_of[BFS][i][0]) + "\n"
            if self.explore:
                analysis += "\t\t  Explored:\t\t" + str(MemInfo_of[BFS][i][1]) + "\n"
            analysis += "\t\t  Frontier Max:\t"   + str(MemInfo_of[BFS][i][2]) + "\n"
            analysis += "\t\tBidirectional sizes:\n"
            analysis += "\t\t  Graph:\t\t"        + str(MemInfo_of[BI][i][0]) + "\n"
            if self.explore:
                analysis += "\t\t  Explored:\t\t" + str(MemInfo_of[BI][i][1]) + "\n"
            analysis += "\t\t  Frontier Max:\t"   + str(MemInfo_of[BI][i][2]) + "\n\n"
        
        ## RETURN THE MEMORY USAGE ANALYSIS AS A STRING ##
        return analysis

class Path:
    def __init__(self,length,heights):
        self.length  = length
        self.heights = heights
        
    def get_analysis(self):
        analysis = "Solution Path Length Analysis\n\n"
        for h in self.heights:
            Problem     = Towers_Of_Hanoi(length=self.length,height=h)
            BFS_States  = trace(breadth_first_search(Problem))
            #Bidirectional Breadth-First-Search
            Problem     = Towers_Of_Hanoi(length=self.length,height=h)
            Goal        = Towers_Of_Hanoi(length=self.length,height=h,swap=True)
            Bi_States   = trace(bidirectional_search(Problem, Goal))
            
            analysis += "\tFor Height = " + str(h) + ":\n"
            analysis += "\t\tBreadth-First-Search:\t" + str(len(BFS_States)) + "\n"
            analysis += "\t\tBidirectional:\t\t\t" +        str(len(Bi_States))  + "\n\n"
        
        
        return analysis

class Run_Time:
    def __init__(self, length, heights, explore, count):
        self.length  = length
        self.heights = heights
        self.explore = explore
        self.count   = count
        self.h       = heights[0]
        
        self.__construct__()
        
    def __construct__(self):
        ## INITIALIZE ARRAYS WHERE STRINGS WILL BE KEPT FOR TIMEIT OBJECTS ##
        self.setup       = []
        self.program     = []
        ## FORM SHARED ARGUMENTS FOR BI AND BFS FUNCTIONS (NOTE WE HAVE TO USE GLOBALS) ##
        arguments   = "length=LENGTH,height=HEIGHT,explore=EXPLORE"
        ## FORM THE FUNCTION CALL STRING FOR TIMEIT ##
        program_bfs = "breadth_first_search(Towers_Of_Hanoi(" + arguments + "))"
        program_bi  = "bidirectional_search(Towers_Of_Hanoi(" + arguments + "),"
        program_bi +=                      "Towers_Of_Hanoi(" + arguments + ",swap=True))"
        self.program.append(program_bfs)
        self.program.append(program_bi)
        
        ## FORM THE IMPORT STRINGS FOR TIMEIT ##
        setup_str  = "from __main__ import Towers_Of_Hanoi,"
        setup_bfs   = setup_str + " breadth_first_search, LENGTH, HEIGHT, EXPLORE"                            
        setup_bi    = setup_str + " bidirectional_search, LENGTH, HEIGHT, EXPLORE"  
        self.setup.append(setup_bfs)
        self.setup.append(setup_bi)
    
    def get_analysis(self):
        Time_of = [[],[]]
        BFS,BI  = 0,1
        
        ## EXECUTE BREADTH FIRST SEARCH RUN-TIME ANALYSIS ##
        for h in self.heights:
            ## FOR TIMEIT TO WORK, h MUST BE ACCESSIBLE GLOBALLY THROUGH OBJECT ##
            global HEIGHT
            HEIGHT = h
            ## SETUP AND RUN TIMEIT INSTANCE FOR RUNTIME FOR HEIGHT h over COUNT repetitions ##
            BFS_timer = timeit.Timer(self.program[BFS], setup=self.setup[BFS])
            BI_timer  = timeit.Timer(self.program[BI],  setup=self.setup[BI])
            ## GET AND COMPUTE AVERAGE RUN-TIME THEN STORE IT ##
            BFS_avg_t = round(BFS_timer.timeit(self.count)/self.count, 5)
            Time_of[BFS].append(BFS_avg_t)
            ## GET AND COMPUTE AVERAGE RUN-TIME THEN STORE IT ##
            BI_avg_t  = round(BI_timer.timeit(self.count)/self.count, 5)
            Time_of[BI].append(BI_avg_t)
            
        
        ## CREATE OUTPUT RUN-TIME ANALYSIS ##
        analysis = "Run-Time Test Results\n\n"
        for i,h in enumerate(self.heights):
            analysis += "\tFor Height = " + str(h) + ":\n"
            analysis += "\t\tBreadth-First-Search:\t" + str(Time_of[BFS][i]) + "s\n" 
            analysis += "\t\tBidirectional:\t\t\t" + str(Time_of[BI][i]) + "s\n\n"
        
        return analysis

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
    RUN_SP = inputs.sp
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
    HEIGHTS     = range(LOW, HIGH + 1)
    
    ## FORMAT OUTPUT FOR ANALYSIS HEADER ##
    table  = "Towers Of Hanoi Analysis\n"
    seper  = "-" * len(table) + "\n"
    table += seper
    table += "\nTEST SETTINGS\n"
    table += "\tUse Explored Set:\t\t" + str(EXPLORE) + "\n"
    table += "\tNumber Of Towers:\t\t" + str(LENGTH) + "\n"
    table += "\tNumber Of Executions:\t" + str(COUNT) + "\n"
    table += "\tTower Height Range:\t\t" + str(LOW) + " to " + str(HIGH) + "\n\n"
    
    #IF NO TEST SPECIFIED OR RUNTIME SPECIFIED, EXECUTE RUNTIME
    if RUN_RT or not (RUN_MU or RUN_RT or RUN_SP):
        table += seper
        ## GLOBAL FOR Run_Time USE ##
        global HEIGHT
        HEIGHT = HEIGHTS[0]
        run_time = Run_Time(LENGTH, HEIGHTS, EXPLORE, COUNT)
        ## ADD RUN TIME REPORT BY CALLING get_analysis FUNCTION ##
        table += run_time.get_analysis()
    
    #IF NO TEST SPECIFIED OR MEMORY USAGE SPECIFIED, EXECUTE MEMORY USAGE
    if RUN_MU or not (RUN_MU or RUN_RT or RUN_SP):
        table += seper
        mem_usage = Mem_Usage(LENGTH,HEIGHTS,EXPLORE)
        ## ADD MEMORY USAGE REPORT BY CALLING get_analysis FUNCTION ##
        table += mem_usage.get_analysis()
    
    #IF NO TEST SPECIFIED OR SOLUTION PATH SPECIFIED, EXECUTE SOLUTION PATH
    #Note: The purpose for the solution path is for varying tower heights
    if RUN_SP or not (RUN_MU or RUN_RT or RUN_SP):
        table += seper
        #Default test just returns the solution path lengths
        solution_path = Path(LENGTH,HEIGHTS)
        table += solution_path.get_analysis()
    
    #Print to terminal if a log file was not specified
    if LOGFILE == "":
        print(table)
    else:
        log = open(LOGFILE, 'w')
        log.write(table)
        log.close()
        print("Results output to " + LOGFILE)
            
