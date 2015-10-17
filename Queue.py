
class Queue:
    def __init__(self):
        self.values = []
        self.length = 0
        
    def push(self, value):
        self.values.insert(0,value)
        self.length += 1
    
    def pop(self):
        if self.length == 0:
            return -1
        value = self.values.pop()
        self.length -= 1
        return value
    
    def queue(self,value):
        self.values.insert(0,value)
        self.length += 1
    
    def get_size(self):
        #return length of the stack
        return self.length
        
    def peek(self):
        if self.length == 0:
            return -1
        return self.values[-1]
    
    def compare(self, stack):
        #Not equivalent if sizes are not equal
        if self.get_size() != stack.get_size():
            return False
        
        for i in range(self.get_size()):
            if self.values[i] != stack.values[i]:
                return False
        return True
    
    def is_empty(self):
        return (self.length == 0)
    
    def to_array(self):
        return self.values
    
    def copy(self):
        copy_queue  = Queue()
        for value in self.values:
            copy_queue.queue(value)
        return copy_queue
        
    def print_stack(self):
        stack = self.to_array()
        for value in stack[:-1]:
            print(str(value) + ", ",end="")
        if len(stack) > 0:
            print(str(stack[-1]))
        else:
            print("")