To run the tests, execute the Test.py file through the Python3.4 interpreter. These 
files should be fully functional.

To execute the basic test, run the following:
	
	python3.4 Test.py

To execute the basic tests to an output file called output.txt, run the
following:
	
	python3.4 Test.py --log output.txt
	
Note: output.txt can be swapped out for any file ending in either *.txt or
*.log.

This will run the run-time analysis, memory-usage, and solution path length
with the following basic settings: 
	Tower Heights from 3 to 7
	Number of Towers is 3
	Explored Set usage is enabled
	Number of Executions for Run-Time Analysis is 5
	

To execute with more personalized settings, you can use the following 
command line arguments:

	usage: Test.py [-h] [--min INT] [--max INT] [--runs INT] [--towers INT]
	               [--log FILE] [--no-explore] [-A] [-rt] [-mu]
	
	This program checks the run time for Towers of Hanoi in terms of seconds
	
	optional arguments:
	  -h, --help    show this help message and exit
	  --min INT     Minimum Tower Height for Analysis (default is 3)
	  --max INT     Maximum Tower Height for Analysis (default is 6)
	  --runs INT    Number of executions per Height for run-time analysis
	  				(default is 10)
	  --towers INT  Number of Towers (default is 3)
	  --log FILE    Specify a log file (default will print to terminal)
	  --no-explore  Disable using explored set
	  -sp           Execute Solution Path analysis
	  -rt           Execute Run-Time analysis
	  -mu           Execute Memory Usage analysis
	  
	  
Note: If -sp, -rt, -mu are used in any combination, only those tests specified
will run instead of all of them.

If --log FILE, where FILE is a file name of *.txt or *.log, is used,
the output will be redirected to that file.  The FILE will be overwritten
with the new information.

The metrics that can be adjust for this program are the tower heights, the number
of towers, disabling Explored Set usage, and the number of executions for the 
run-time analysis (which will take the average).

The necessary files for this project are:
	__init__.py
	TowersOfHanoi.py
	Test.py
	
The general approach to my problem was to reuse as much code as possible
between the breadth first search and the bidirectional breadth first search.
This means maximizing variability while decreasing hard-coded values.  By
using this approach, I was also capable of having other varying metrics
like number of towers.  The Bidirectional Search differs from the 
Breadth-First-Search by storing two Problems with initial and goal
states, but one Problem has the two states swapped, so it is working from
the opposite end backwards.  Also, Compare is used to compare two states
for a solution instead of using goal test.
