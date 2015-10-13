from Stack import Stack

class StackTest:
    def __init__(self, name="default", start=0, end=10, increment=1):
        self.values = []
        for value in range(start, end, increment):
            self.values.append(value)
        self.stack = Stack()
        self.name = name
        self.fails = 0
    
    def fail(self):
        self.fails += 1
    
    def generate(self):
        for value in self.values:
            self.stack.push(value)
            self.stack.to_array()
        
        
    def execute(self):
        self.generate()
        for i in range(len(self.values)-1,-1,-1):
            #Test pop value
            if not self.assert_true(self.values[i],self.stack.pop()):
                print("\tPop() did not return expected value")
            #Push value back onto stack and check if the value is now on top
            self.stack.push(self.values[i])
            if not self.assert_true(self.values[i],self.stack.peek()):
                print("\tPeek() did not return expected value after Push()")
            #Pop the value back off the stack and make sure it is the value we just pushed
            if not self.assert_true(self.values[i],self.stack.pop()):
                print("\tPop() function execute did not return expected value after Push()")
            #Verify that the length is proper
            if not self.assert_true(self.stack.get_size(), i):
                print("\tLengths do not match between stack and values array")
            #Verify that stack compare works provided equal stack
            self.assert_compare()
        
        if self.fails == 0:
            print("Stack test results for " + self.name + ": All tests passed")
        else:
            print("Stack test results for " + self.name + ": tests failed.")
            
                
    def assert_true(self, item_1, item_2):
        if item_1 != item_2:
            print(self.name + ": Assertion False")
            self.print_test(item_1,item_2)
            self.fail()
            return False
        else:
            #print(self.name + ": Assertion True")
            #self.print_test(item_1,item_2)
            return True
    
    def assert_list(self, list_1, list_2):
        for i in range(len(list_1)):
            if list_1[i] != list_2[i]:
                print(self.name + ": Assertion False")
                self.print_test(list_1,list_2)
                self.fail()
                
    def assert_compare(self):
        #Verify that stack compare works provided null stack
        if self.stack.compare(Stack()) and self.stack.get_size():
            print("Compare function does not work for null stack")
            self.print_test(False,True)
            self.fail()
        
        #produce random stack of equal size and verify false
        false_stack = Stack()
        for value in self.stack.to_array():
            false_stack.push(value)
        if self.stack.compare(false_stack) and false_stack.get_size() > 1:
            print("Compare function fails for equal length, non-equivalent stacks")
            self.print_test(False,True)
            self.fail()
        
        #produce copy of the stack and verify that compare function works
        true_stack = Stack()
        for value in reversed(self.stack.to_array()):
            true_stack.push(value)
        if not self.stack.compare(true_stack):
            print("Compare function fails for equivalent stacks")
            self.print_test(True,False)
            self.fail()
    
    def print_test(self,expected,result):
        print("\tExpected output: " + str(expected))
        print("\t         Result: " + str(result))
    

def run_tests(tests):
    for test in tests:
        test.execute()

tests = [StackTest("Test 1",0,10,1),
         StackTest("Test 2",0,20,2),
         StackTest("Test 3",30,150,10),
         StackTest("Test 4",10,-1,-1)]

run_tests(tests)
