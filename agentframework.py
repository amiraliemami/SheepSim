import random


class Agent():
    # class_attribute = ... don't use this or global variables.

    def __init__(self,x=None,y=None):
        # DON'T NEED TO MAKE THESE VARIABLES
        # as python will do it for you upon use, but it's better practice
        self.x = x
        self.y = y

        # method_local_variable = ...
        # ^ can only be used above

        # get class name to access class attribute:
        # Agent.class_attribute

    def speak(self):
        print('Hello!')
    
    def randomise(self):
        self.x = random.randint(0,100)
        self.y = random.randint(0,100)