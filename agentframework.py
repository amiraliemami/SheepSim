"""
Module requirements:
- 'numpy'
- 'random'

Includes:
- Agent class
- function for importing the environment: import_environment(path)
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
	Raises:
		TypeError: if non-number is passed as argument.
	"""
	if type(x) not in [float, int]:
		raise TypeError("Can only perturb a number.")

	return ((x + random.choice([-1,1])) % 300)

def import_environment(path='data/in.txt'):
    """Imports the 300x300 pixel environment from the given file path.
    
    Arguments:
        path (str): path to environment file (default 'data/in.txt')
    Returns
        environment (matrix of numbers): list of list of numbers imported from the file
    Raises:
        IOError: if file not found at the given path
    """
    environment = []
    with open(path) as f:
        for line in f:
            parsed_line = line.split(',')
            rowlist = []
            for value in parsed_line:
                rowlist.append(int(value))
            environment.append(rowlist)
    #print('Max of environment: ',max(max(environment))) 
    # we find that max is 245. Choose 250 as max grass level for imshow() in the main python script
    return environment


#### AGENT CLASS
class Agent():
	"""Provides the framework for sheep agents and their associated actions.

	Arguments:
		environment (matrix): list of lists of numbers corresponding to grass height at each pixel of environment
		agents (list): list of Agent objects in the simulation
		init_coords (2-tuple of integers): Determines (x,y) at which this agent is spawned. If None, random x and y are chosen between 0 and 300. (default None)
		sex (str): 'm' or 'f', the sheep's sex (default: None, causes _sex below to be set randomely).

	Attributes:
		_x (integer): The sheep's x coordinate, between 0 and 300
		_y (integer): The sheep's y coordinate, between 0 and 300
		_sex (str): 'm' or 'f', the sheep's sex (default: random if sex argument is None)
		_store (integer): Amount of grass eaten and stored by the sheep. Initiates at 0.
		_pregnancy (integer): Stage of pregnancy the sheep is at. Initiates at 0.
		_age (integer): Number of runs the sheep has lived for. Initiates at 0.

	Methods:
		set_ methods: 
			set_x, set_y, set_store, set_pregnancy
		get_ methods: 
			get_x, get_y, get_store, get_pregnancy, get_sex, get_age
		"Action" methods: 
			move, eat, share_neighbours, mate
		Other methods:
			is_dead, increment_age, distance_to
	"""
	
	def __init__(self, environment:list,agents:list,init_coords=None,sex=None):
		"""Initiates the agent upon creation.

		Arguments:
			environment (list): list of lists of numbers corresponding to grass height at each pixel of environment
			agents (list): list of Agent objects in the simulation
			init_coords (2-tuple of integers): Determines (x,y) at which this agent is spawned. If None, random x and y are chosen between 0 and 300 (default None).
			sex (str): 'm' or 'f', the sheep's sex (default: None, causes _sex below to be set randomely).

		Attributes:
			_x (integer): The sheep's x coordinate, between 0 and 300
			_y (integer): The sheep's y coordinate, between 0 and 300
			_sex (str): 'm' or 'f', the sheep's sex (default: random if sex argument is None)
			_store (integer): Amount of grass eaten and stored by the sheep. Initiates at 0.
			_pregnancy (integer): Stage of pregnancy the sheep is at. Initiates at 0.
			_age (integer): Number of runs the sheep has lived for. Initiates at 0.
			environment (list): store given environment as internal attribute
			agents (list): store given agents as internal attribute
		"""

		# private attributes
		if init_coords is None:
			self._x = random.randint(0,299)
			self._y = random.randint(0,299)
		else:
			self._x = init_coords[0]
			self._y = init_coords[1]

		if sex is None:
			self._sex = random.choice(['m','f'])
		else:
			self._sex = sex

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

	def get_sex(self): # read-only
		"""Returns the private _sex attribute. Note: This attribute does not have a set method - it is read-only."""
		return self._sex

	def get_age(self):
		"""Returns the private _age attribute"""
		return self._age

	# actions
	def move(self,optimised=True):
		"""Moves the sheep it is called on one step.
		
		Can be random (random walk, optimised=False), or towards the direction of most grass unless current position has
		more than surrounding areas, in which case the sheep does not move (greedy search, optimised=True).

		Arguments:
			optimised (bool): 
			If False, sheep moves randomely to a neighbouring pixel. If True, sheep moves towards
			direction of most grass, or does not move if current pixel has most grass (default True)
		"""

		if optimised:
			# initialise
			x_current, y_current = self._x % 300, self._y % 300
			x_best, y_best = x_current, y_current
			max_grass_val = self.environment[y_current][x_current]
			# run loop on the 3x3 block around the sheep's current position
			for i in [-1,0,1]:
				for j in [-1,0,1]:
					x = (x_current + i) % 300
					y = (y_current + j) % 300
					grass_val_here = self.environment[y][x]
					# only update if more grass found here than so far
					if grass_val_here > max_grass_val:
						max_grass_val = grass_val_here
						x_best, y_best = x, y

			if max_grass_val == 0:
				# if best grass is 0, means that current position and all directions are at 0
				# in this case, take a random step
				self._x, self._y = perturb(self._x), perturb(self._y)
			else:
				self._x, self._y = x_best, y_best	
		else:
			# If not optimised, perturb the agent's x and y coordinates randomly and independantly using the perturb() function
			self._x, self._y = perturb(self._x), perturb(self._y)

	def eat(self, max_grass_per_turn=20, sick_enabled=False):
		"""Calling this will cause the sheep to "eat grass" from the coordinate it is standing on in the environment. 

		If the environment has value equal to or more than max_grass_per_turn at the coordinate at which the sheep is currently standing, the sheep will increase its
		store by max_grass_per_turn, and the environment's value here will decrease by max_grass_per_turn. If the value here is less than max_grass_per_turn, the sheep 
		will add this value to its store and reduce the environment to 0 at this spot. If environment is at 0 at this coordinate, the sheep will not eat.

		Arguments:
			max_grass_per_turn (int or float): the maximum amount each sheep can eat per turn, if current coordinate has this available. Otherwise, the sheep consumes
				what's left of the grass beneath it (default 20)
			sick_enabled (bool): if True, sheep sick up 50 onto their current coordinate in the environment if their store reaches 100 (default False)
		"""

		if type(max_grass_per_turn) not in [float, int]:
			raise TypeError("max_grass_per_turn must be a number.")

		grass_available = self.environment[self._y][self._x]
		# eat max_grass_per_turn if grass abundant
		if grass_available >= max_grass_per_turn:
			self.environment[self._y][self._x] -= max_grass_per_turn
			self._store += max_grass_per_turn
		# do nothing if no grass
		elif grass_available == 0:
			pass
		# eat what's left if less than max_grass_per_turn
		else:
			self.environment[self._y][self._x] = 0
			self._store += grass_available

		if sick_enabled:
		# sick up 50 of store if store goes above 100
			if self._store > 100:
				self.environment[self._y][self._x] += 50
				self._store = 50
    
	def distance_to(self, other):
		"""Given another agent, return the Euclidean distance between self and the given agent.

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
			neighbourhood_size (integer or float): Radius below which sharing is triggered (default 20)
		"""

		if type(neighbourhood_size) not in [float, int]:
			raise TypeError("neighbourhood_size must be a number.")	

		for agent in self.agents:
			# do not perform action with oneself (not necessary as avg of x and x is x, but is good practice in case we generalise, 
			# e.g. if a fight is involved and resources are lost per interaction)
			if agent is not self:
				if self.distance_to(agent) <= neighbourhood_size:
					avg = (self._store + agent.get_store())/2
					self._store = avg
					agent.set_store(avg)
		
		#print(neighbourhood_size) # to check

	######### EXTRAS - Mating, Aging and Dying #################################################################################################

	def mate(self, preg_duration=10, min_age=20, min_dist=10, min_store=50):
		"""Enables mating for the sheep, meaning that female sheep get pregnant if they come close enough to male sheep and thus give birth to new sheep after a given pegnancy duration.

		If both self and other sheep are of age, have enough food store, are close enough, and are also of opposite sexes, the female one will get pregnant. 
		Pregnancies progress with each iteration of the simulation and once the correct duration is reached, a new sheep (new instance of the Agent class) 
		is initiated 5 positions to the right of the mother. 

		NOTES:
		- At each run of this mating function on an agent (i.e. agent.mating()), that agent looks around it for possible mates. Thus must be run on each agent per update of the simulation.
		- A pregnant sheep cannot get re-pregnant until it gives birth.

		Arguments:
			preg_duration (integer): number of turns that a pregnancy lasts from conception to giving birth (default 10)
			min_age (integer): both sheep (male and female) must be of this age or more to be able to mate (default 20)
			min_dist (integer or float): must be closer than this distance to be able to mate (default 10)
			min_store (integer or float): both sheep must have this much store or more to be able to mate (default 50)
		Raises:
			ValueError: if pregnancy value becomes negative or goes above preg_duration
		"""

		# type checking
		if type(preg_duration) != int:
			raise TypeError("preg_duration must be an integer.")
		if type(min_age) != int:
			raise TypeError("min_age must be an integer.")
		if type(min_dist) not in [float, int]:
			raise TypeError("min_dist must be a number.")
		if type(min_store) not in [float, int]:
			raise TypeError("min_store must be a number.")

		# add 1 to preg_duration since the iteration in which the baby is conceived counts as +1 in the agentframework
		# this ensures that if (min_age_for_preg + preg_duration > max_age) then no babies are born
		preg_duration += 1

		# if self has pregnancy 0, look for a mate (always true if male, and a necessary condition if female)
		pregnancy = self._pregnancy
		if pregnancy == 0:
			# proceed if self is of age and has consumed enough food
			if (self._age > min_age) and (self._store > min_store) and (self._pregnancy == 0):
			# loop through all sheep in simulation
				for agent in self.agents:
					# do not self-mate, please (not needed as opposite sexes required, but good practice in case we generalise to parthenogenesis)
					if agent is not self:
						# only mate if distance between self and other sheep is less than the given minimum distance
						if self.distance_to(agent) <= min_dist:
							# only mate if other sheep is also of min_age and store
							if (agent.get_age() > min_age) and (agent.get_store() > min_store):

								# only mate if opposite sexes
								if self._sex == 'f' and agent.get_sex() == 'm':
									self._pregnancy = 1

								elif self._sex == 'm' and agent.get_sex() == 'f':
									# only get other sheep pregnant if it's not already
									if agent.get_pregnancy() == 0:
										agent.set_pregnancy(1)
        
		elif pregnancy == preg_duration:
			# Give birth to another sheep 5 positions to the right (mod 300 to cover edge cases) if pregnancy duration reached
			self.agents.append(Agent(self.environment, self.agents, [(self._x + 5) % 300, self._y]))
			# reset pregnancy after giving birth, ready for the next
			self._pregnancy = 0
		
		elif pregnancy > 0 and pregnancy < preg_duration:
			# Advance pregnancy if already pregnant
			self._pregnancy += 1

		# pregnancy value checking
		elif pregnancy > preg_duration:
			raise ValueError("Pregnancy duration exceeded... Something's wrong!")
		elif pregnancy < 0:
			raise ValueError("Negative value for pregnancy duration... Something's wrong!'")

	def is_dead(self,max_age=100):
		"""Checks if age has reached the maximum age (integer, default 100) and returns a bool answer."""
		if type(max_age) != int:
			raise TypeError("max_age must be an integer.")
		return (self._age >= max_age)

	def increment_age(self):
		"""Increments the agent's age on which it was called."""
		self._age += 1