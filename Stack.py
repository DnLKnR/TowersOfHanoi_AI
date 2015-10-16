## This file will contain the implementation for the stack used in the towers of hanoi
import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
    def set_next(self, next):
        self.next = next
    
    def get_value(self):
        return self.value
    
    def get_next(self):
        return self.next
        
class Stack(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        
    def push(self, value):
        #Create new node for value
        new = Node(value)
        #Connect the node to head
        if self.head != None:
            new.set_next(self.head)
        #Reset head to the new node
        self.head = new
        #Increment the length of the stack
        self.length += 1
    
    def pop(self):
        #If stack is null, return invalid
        if self.length == 0:
            return -1
        elif self.length == 1:
            self.tail = None
        #get the value off the first node
        value = self.head.get_value()
        #increment head forwards
        self.head = self.head.get_next()
        #decrement length
        self.length -= 1
        #return the value
        return value
    
    def queue(self,value):
        new = Node(value)
        if self.length == 0:
            self.head = new
            self.tail = new
        else:
            self.tail.set_next(new)
            #Set tail to the newly added item
            self.tail = self.tail.get_next()
        #Increment the length of the stack
        self.length += 1
    
    def get_size(self):
        #return length of the stack
        return self.length
        
    def peek(self):
        return self.head.get_value()
    
    def compare(self, stack):
        start = [self.head, stack.head]
        #Not equivalent if sizes are not equal
        if self.get_size() != stack.get_size():
            return False
        
        #loop through both stacks simultaneously, while checking values
        while None not in start:
            if start[0].get_value() != start[1].get_value():
                return False
            #else shift forward in each list
            start[0] = start[0].get_next()
            start[1] = start[1].get_next()
        
        return True
    
    def is_empty(self):
        return (self.length == 0)
    
    def to_array(self):
        start = self.head
        stack = []
        if self.get_size() == 0:
            return stack
        while start != None:
            stack.append(start.value)
            start = start.get_next()
        
        return stack
    
    def copy(self):
        start       = self.head
        copy_stack  = Stack()
        while start != None:
            value = start.get_value()
            copy_stack.queue(value)
            start = start.get_next()
        return copy_stack
        
    def print_stack(self):
        stack = self.to_array()
        for value in stack[:-1]:
            print(str(value) + ", ",end="")
        if len(stack) > 0:
            print(str(stack[-1]))
        else:
            print("")



        
