#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:00:42 2019

@author: Amir
"""

import agentframework as af
import random
import numpy as np
import matplotlib.pyplot as plt
random.seed(100)

# set default global variables
num_of_agents = 10
num_steps = 2000
neighbourhood = 20

# for commandline run as
# python model.py n_agents n_iters neighbourhood_size
import sys
print(sys.argv)
if len(sys.argv) > 1:
    args = sys.argv[1:]
    print('#### USING COMMANDLINE ARGUMENTS: ',args)
    num_of_agents = int(args[0])
    num_steps = int(args[1])
    neighbourhood = int(args[2])
else:
    print('#### USING DEFAULT ARGUMENTS: ',num_of_agents,num_steps,neighbourhood)


#### INITIALISE
environment = []
with open('data/in.txt') as f:
    for line in f:
        parsed_line = line.split(',')
        rowlist = []
        for value in parsed_line:
            rowlist.append(int(value))
        environment.append(rowlist)
        
agents = []
for _ in range(num_of_agents):
    agents.append(af.Agent(environment,agents)) 
    # the agents list will update, and since only a link is given to the agents,
    # everyone will get a full list

# TEST each agent has list of others
# print(agents[0].agents[6].x,agents[0].agents[6].y)
# print(agents[6].x,agents[6].y)
#agents[0].share_with_neighbours(neighbourhood)


# plot initial positions
np_agents = np.array([[agent.x,agent.y] for agent in agents])
plt.scatter(np_agents[:,0],np_agents[:,1],c='white',label='Initial')
plt.imshow(environment)
# plt.ylim(0, 100)
# plt.xlim(0, 100)
plt.title('Initial')
plt.show()

### MOVE AND EAT
for _ in range(num_steps):
    random.shuffle(agents) # shuffle agents before each iteration
    for i in range(len(agents)):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)

# plot final positions
np_agents_new = np.array([[agent.x,agent.y] for agent in agents])
plt.scatter(np_agents_new[:,0],np_agents_new[:,1],c='white',label='Final')
plt.imshow(environment)

plt.title('Final')
#plt.legend()
# plt.ylim(0, 100)
# plt.xlim(0, 100)
plt.show()