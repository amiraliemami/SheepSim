#!/usr/bin/python

#### IMPORTS #####################################################################

import agentframework as af

import random
random.seed(100)
import numpy as np

import tkinter

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.set_cmap('YlGn')
import matplotlib.animation as anim

###### INITIALISE ###############################################################

# set default global variables #################

num_agents = 50
num_iters = 2000

max_age = 50
min_age_for_preg = 10
preg_duration = 10

neighbourhood = 20

###############################################

#### IMPORT ENVIRONMENT
environment = []
with open('data/in.txt') as f:
    for line in f:
        parsed_line = line.split(',')
        rowlist = []
        for value in parsed_line:
            rowlist.append(int(value))
        environment.append(rowlist)
#print('Max of environment: ',max(max(environment)))
# max is 245. Choose 250 as max grass level


#### initiate agents based on num_agents required ############
agents = []
for i in range(num_agents):
    agents.append(af.Agent(environment,agents)) 


# #### FOR TESTING OF MATING
# positions = [[50,50],[52,52]]
# genders = ['m','f']
# num_agents = len(positions)
# agents = []
# for i in range(num_agents):
#     agents.append(af.Agent(environment,agents,positions[i],genders[i]))  


#### UPDATING  ###############################################################

# (moving, eating, mating, aging, dying) AND PLOTTING
carry_on = True
def update(frame_number):
    
    print('Frame: ', frame_number)
    print('Number of Sheep: ', len(agents))

    global carry_on

    # environment needs to be plotted at the start of every run to show developments from last run
    fig.clear()
    plt.imshow(environment, vmin=0, vmax=250)
    plt.xlim(0,300)
    plt.ylim(0,300)
    plt.axis('off')

    # simulation stopping conditions
    if len(agents) == 0:
        print('All dead :(')
        carry_on = False
    elif np.array(environment).sum() == 0:
        carry_on = False
        print("All grass eaten!")

    # shuffle agents before each iteration
    random.shuffle(agents) 

    the_dead = []
    for agent in agents:
        agent.eat()
        agent.mating(preg_duration,min_age_for_preg)
        agent.move()
        #agent.share_with_neighbours(neighbourhood)

        c = ('black' if agent.get_gender() == 'm' else 'white') # coloured based on gender
        s = (agent.get_age()/max_age)*300 # size based on age

        # check if it dies at the end of this turn
        if agent.is_dead(max_age):
            the_dead.append(agent)
            plt.scatter(agent.get_x(),agent.get_y(),s=s,c=c,marker='1')
        else:
            agent.increment_age()
            plt.scatter(agent.get_x(),agent.get_y(),s=s,c=c,marker='*')
    
    # remove all who died in this round at once
    for dead_agent in the_dead:
        agents.remove(dead_agent)

#### Setup animation and GUI ################################################

def gen_function():
    a = 0
    global carry_on
    while (a < num_iters) and carry_on:
        yield a	  # Returns control and waits next call.
        a += 1

fig = plt.figure(figsize=(10, 10))
animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
plt.show()