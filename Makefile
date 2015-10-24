WHILE = number=1; while [[ $$number -le 16 ]]
INC = ((number = number + 1))
TEST = do python3.4 Test.py --min $$number --max $$number --runs 1
RT = -rt --log Analysis/RT_Test_$$number.log
MU = -mu --log Analysis/MU_Test_$$number.log
SP = -sp --log Analysis/SP_Test_$$number.log

rt:
	${WHILE}; \
		${TEST} ${RT}; \
		${INC}; \
	done

mu:
	${WHILE}; \
		${TEST} ${MU}; \
		${INC}; \
	done

sp:
	${WHILE}; \
		${TEST} ${SP}; \
		${INC}; \
	done
	

