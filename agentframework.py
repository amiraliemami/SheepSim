import random

def perturb(x): 
    return (x + random.choice([-1,1])) % 100

class Agent():
    # protect self.x and y using 'property': https://docs.python.org/3/library/functions.html#property
    def __init__(self, environment:list):
        self.x = random.randint(0,100)
        self.y = random.randint(0,100)
        
        self.environment = environment
        self.store = 0
        
        
    def set_x(self,x:int):
        self.x = x
    def set_y(self,y:int):
        self.y = y
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

    def move(self):
        self.x, self.y = perturb(self.x), perturb(self.y)

    def eat(self):
        grass_available = self.environment[self.y][self.x]
        if grass_available > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        # make it eat what's left
        else:
            self.environment[self.y][self.x] = 0
            self.store += grass_available
        
        if self.store > 100:
            self.environment[self.y][self.x] += 50
            self.store = 50
            

















    # class_attribute = ... don't use this or global variables.

#    def __init__(self,x=None,y=None):

#        # DON'T NEED TO MAKE THESE VARIABLES
#        # as python will do it for you upon use, but it's better practice
#        self.x = x
#        self.y = y
#
#        # method_local_variable = ...
#        # ^ can only be used above
#
#        # get class name to access class attribute:
#        # Agent.class_attribute
#
#    def speak(self):
#        print('Hello!')
#    
#    def randomise(self):
#        self.x = random.randint(0,100)
#        self.y = random.randint(0,100)
#        
#    def has_bigger_x(self,other):
#        if self.x > other.x:
#            print('TRUE!')
#        else:
#            print('FALSE!')