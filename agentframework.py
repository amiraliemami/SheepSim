"""
Module requirements:
- 'numpy'
- 'random'
"""

#### NECESSARY MODULES AND FUNCTIONS
import random
import numpy as np

def perturb(x): 
	"""Given a number, returns a perturbed version of it with equal chance of increase or decrease by 1, mod300.	
	
	Arguments:
		x (integer or float): a number
	Returns:
		Either (x+1)mod300 or (x-1)mod300, with equal probability.
	"""
    return (x + random.choice([-1,1])) % 300

#### AGENT CLASS
class Agent():
		"""Provides the framework for sheep agents and their associated actions.
		
		Arguments:
			environment (matrix): list of lists of numbers corresponding to grass height at each pixel of environment
			agents (list): list of Agent objects in the simulation
			init_coords (2-tuple of ints): Determines (x,y) at which this agent is spawned. If None, random x and y are chosen between 0 and 300. (default None)
			gender (str): 'm' or 'f', the sheep's gender (default: None, causes _gender below to be set randomely).

		Attributes:
			_x (int): The sheep's x coordinate, between 0 and 300
			_y (int): The sheep's y coordinate, between 0 and 300
			_gender (str): 'm' or 'f', the sheep's gender (default: random if gender argument is None)
			_store (int): Amount of grass eaten and stored by the sheep. Initiates at 0.
			_pregnancy (int): Stage of pregnancy the sheep is at. Initiates at 0.
			_age (int): Number of runs the sheep has lived for. Initiates at 0.

		Methods:
			Set methods: 
				set_x, set_y, set_store, set_pregnancy
			Get methods: 
				get_x, get_y, get_store, get_pregnancy, get_gender, get_age
			Action methods: 
				move, eat, share_neighbours, mating
			Other methods:
				is_dead, increment_age, distance_to
        """
	
    def __init__(self, environment:list,agents:list,init_coords=None,gender=None):
        """Initiates the agent upon creation.

		Arguments:
			environment (list): list of lists of numbers corresponding to grass height at each pixel of environment
			agents (list): list of Agent objects in the simulation
			init_coords (2-tuple of ints): Determines (x,y) at which this agent is spawned. If None, random x and y are chosen between 0 and 300. (default None)
			gender (str): 'm' or 'f', the sheep's gender (default: None, causes _gender below to be set randomely).

		Attributes:
			_x (int): The sheep's x coordinate, between 0 and 300
			_y (int): The sheep's y coordinate, between 0 and 300
			_gender (str): 'm' or 'f', the sheep's gender (default: random if gender argument is None)
			_store (int): Amount of grass eaten and stored by the sheep. Initiates at 0.
			_pregnancy (int): Stage of pregnancy the sheep is at. Initiates at 0.
			_age (int): Number of runs the sheep has lived for. Initiates at 0.
			environment (list): store given environment as internal attribute
			agents (list): store given agents as internal attribute
		"""

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
		"""Sets the private _x attribute to given integer."""
        self._x = x

    def set_y(self,y:int):
		"""Sets the private _y attribute to given integer."""
        self._y = y

    def set_store(self,val:int):
		"""Sets the private _store attribute to given integer."""
        self._store = val

    def set_pregnancy(self,val:int):
		"""Sets the private _pregnancy attribute to given integer."""
        self._pregnancy = val
        
    def get_x(self):
		"""Returns the private _x attribute"""
        return self._x

    def get_y(self):
		"""Returns the private _y attribute"""
        return self._y

    def get_store(self):
		"""Returns the private _store attribute"""
        return self._store

    def get_pregnancy(self):
		"""Returns the private _pregnancy attribute"""
        return self._pregnancy

    def get_gender(self): # read-only
		"""Returns the private _gender attribute. Note: This attribute does not have a set method - it is read-only."""
        return self._gender

    def get_age(self):
		"""Returns the private _age attribute"""
        return self._age

    # actions
    def move(self):
		"""Perturbs the agent's x and y coordinates independantly using the perturb() function. Takes no arguments."""
        self._x, self._y = perturb(self._x), perturb(self._y)

    def eat(self, sick_enabled=False):
		"""Calling this will cause the sheep to "eat grass" from the coordinate it is standing on in the environment. 
		
		If the environment has value equal to or more than 10 at the coordinate at which the sheep is currently standing, the sheep will increase its
		store by 10, and the environment's value here will decrease by 10. If the value here is less than 10, the sheep will add this value to its store
		and reduce the environment to 0 at this spot. If environment is at 0 at this coordinate, the sheep will not eat.
		
		Arguments:
			sick_enabled (bool): if True, sheep sick up 50 onto their current coordinate in the environment if their store reaches 100 (default False)
		"""

        grass_available = self.environment[self._y][self._x]
		# eat 10 if grass abundant
        if grass_available >= 10:
            self.environment[self._y][self._x] -= 10
            self._store += 10
		# do nothing if no grass
        elif grass_available == 0:
			pass
		# eat what's left if less than 10
		else:
            self.environment[self._y][self._x] = 0
            self._store += grass_available
        
		if sick_enabled:
        # sick up 50 of store if store goes above 100
			if self._store > 100:
				self.environment[self._y][self._x] += 50
				self._store = 50
    
    def distance_to(self, other):
		"""Given another agent, get the Euclidean distance between self and the given agent.
		
		Arguments:
			other (Agent class): Other sheep to get distance to.
		Returns:
			Euclidean distance (float) to the other sheep.
		"""
        return np.sqrt(((self._x - other.get_x())**2) + ((self._y - other.get_y())**2))

    def share_with_neighbours(self,neighbourhood_size=20):
		"""Share store with nearby sheep by splitting resources with them.
		
		Check if any other sheep are within a given radius of self, and if so, share stores by setting the value of the stores for self and
		the other sheep to the average of the stores between the two.
		
		Arguments:
			neighbourhood_size (int or float): Radius below which sharing is triggered (default 20)
		"""
        for agent in self.agents:
			# do not perform action with oneself (not necessary as avg of x and x is x, but is good practice in case we generalise)
            if agent is not self:
                if self.distance_to(agent) <= neighbourhood_size:
                    avg = (self._store + agent.get_store())/2
                    self._store = avg
                    agent.set_store(avg)
           #else: # CHECK IF SAME as self
           #    print('The same!',agent,self)


    ######### EXTRAS - Mating, Aging and Dying #################################################################################################

    def mating(self,preg_duration=10,min_age=20):
		"""Enables mating for the sheep, meaning that female sheep get pregnant if they come close enough to male sheep and give birth to new sheep after a given pegnancy duration.
		

		Arguments:
			preg_duration (integer): 
		
		
		"""
        pregnancy = self._pregnancy
        # GIVE BIRTH to another sheep to the right
        if pregnancy == preg_duration:
            self.agents.append(Agent(self.environment,self.agents,[self._x+1,self._y]))
            self._pregnancy = 0 # reset after giving birth
        # ADVANCE PREGNANCY if pregnant
        elif pregnancy > 0:
            self._pregnancy += 1
        # else stay non-pregnant
        else:
            pass
        
        # if of age and enough food consumed (50), try to mate with other sheep:
        if (self._age > min_age) and (self._store > 50):
            for agent in self.agents:
                if agent is not self:
                    # only mate if closer than 10
                    if self.distance_to(agent) <= 10: 
                        # only mate if other sheep is also of min_age and food
                        if (agent.get_age() > min_age) and (agent.get_store() > 50):
                            
                            if self._gender == 'f' and agent.get_gender() == 'm':
                                if self._pregnancy == 0: # only get pregnant if not already
                                    self._pregnancy = 1
                            elif self._gender == 'm' and agent.get_gender() == 'f':
                                if agent.get_pregnancy() == 0:
                                    agent.set_pregnancy(1)
                            else:
                                pass

    def is_dead(self,max_age=100):
        return (self._age > max_age)

    def increment_age(self):
            self._age += 1



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