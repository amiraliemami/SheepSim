#### NECESSARY MODULES AND FUNCTIONS
import random
import numpy as np

def perturb(x): 
    return (x + random.choice([-1,1])) % 300

#### AGENT CLASS
class Agent():
    def __init__(self, environment:list,agents:list,init_coords=None,gender=None):
        
        # private attributes
        if init_coords is None:
            self._x = random.randint(0,300)
            self._y = random.randint(0,300)
        else:
            self._x = init_coords[0]
            self._y = init_coords[1]

        if gender is None:
            self._gender = random.choice(['m','f'])
        else:
            self._gender = gender

        self._store = 0
        self._pregnancy = 0
        self._age = 0

        # public attributes
        self.environment = environment
        self.agents = agents
        
    # functions for accessing private attributes
    def set_x(self,x:int):
        self._x = x
    def set_y(self,y:int):
        self._y = y
    def set_store(self,val:int):
        self._store = val
    def set_pregnancy(self,val:int):
        self._pregnancy = val
        
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    def get_store(self):
        return self._store
    def get_pregnancy(self):
        return self._pregnancy

    def get_gender(self): # read-only
        return self._gender
    def get_age(self):
        return self._age
    
    # actions
    def move(self):
        self._x, self._y = perturb(self._x), perturb(self._y)

    def eat(self):
        grass_available = self.environment[self._y][self._x]
        if grass_available > 10:
            self.environment[self._y][self._x] -= 10
            self._store += 10
        # make it eat what's left
        else:
            self.environment[self._y][self._x] = 0
            self._store += grass_available
        
        # # sick up 50 of store if store goes above 100
        # if self._store > 100:
        #     self.environment[self._y][self._x] += 50
        #     self._store = 50
    
    def distance_to(self, other):
        return np.sqrt(((self._x - other.get_x())**2) + ((self._y - other.get_y())**2))

    def share_with_neighbours(self,neighbourhood_size):
        for agent in self.agents:
            if agent is not self:
                if self.distance_to(agent) <= neighbourhood_size:
                    avg = (self._store + agent.get_store())/2
                    self._store = avg
                    agent.set_store(avg)
           #else: # CHECK IF SAME as self
           #    print('The same!',agent,self)

    ## EXTRA - mating and aging

    def mating(self,preg_duration=10,min_age=20):
        for agent in self.agents:
            pregnancy = agent.get_pregnancy() 

            # GIVE BIRTH to another sheep to the right
            if pregnancy == preg_duration:
                self.agents.append(Agent(self.environment,self.agents,[agent.get_x()+1,agent.get_y()])) 
                agent.set_pregnancy(0) # reset after giving birth
            # ADVANCE PREGNANCY if pregnant
            elif pregnancy > 0:
                agent.set_pregnancy(pregnancy+1)
            # else stay non-pregnant
            else:
                pass

            # mating rules
            if agent is not self:

                if self.distance_to(agent) <= 5: # only mate if closer than 5
                    # only mate if of min_age reached for mating
                    if self._age > min_age and agent.get_age() > min_age: 
                        # only mate if have 50 in stomach
                        if self._store > 50 and agent.get_store() > 50: 
                            
                            if self._gender == 'f' and agent.get_gender() == 'm':
                                if self._pregnancy == 0: # only get pregnant if not already
                                    self._pregnancy = 1
                            elif self._gender == 'm' and agent.get_gender() == 'f':
                                if agent.get_pregnancy() == 0:
                                    agent.set_pregnancy(1)
                            else:
                                pass

    def increment_age_or_die(self,max_age=100):
        if self._age > max_age:
            self.agents.remove(self) 
            return True   
        else:
            self._age += 1
            return False



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