#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:00:42 2019

@author: Amir
"""

#### IMPORTS
import agentframework as af
import random
random.seed(100)
import numpy as np

import tkinter

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
plt.set_cmap('viridis')

import matplotlib.animation as anim


# set default global variables
num_agents = 10
num_iters = 2000
neighbourhood = 20

##### COMMANDLINE:
# python model.py n_agents n_iters neighbourhood_size
import sys
print(sys.argv)
if len(sys.argv) > 1:
    args = sys.argv[1:]
    print('#### USING COMMANDLINE ARGUMENTS: ',args)
    num_agents = int(args[0])
    num_iters = int(args[1])
    neighbourhood = int(args[2])
else:
    print('#### USING DEFAULT ARGUMENTS: ',num_agents,num_iters,neighbourhood)


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
for _ in range(num_agents):
    agents.append(af.Agent(environment,agents)) 


#### UPDATING (moving and eating) AND PLOTTING
carry_on = True

def update(frame_number):
    
    fig.clear()
    global carry_on
    
    random.shuffle(agents) # shuffle agents before each iteration
    for i in range(num_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        
    if np.array(environment).sum() == 0:
        carry_on = False
        print("All grass eaten!")

    plt.imshow(environment, vmin=0, vmax=max(max(environment))) # environment needs to be plotted every time to show developments
    for i in range(num_agents):
        np_agents = np.array([[agent.x,agent.y] for agent in agents])
        plt.scatter(np_agents[:,0],np_agents[:,1],c='white')
        plt.xlim(0,300)
        plt.ylim(0,300)

def gen_function(b = [0]):
    a = 0
    global carry_on
    while (a < num_iters) and carry_on:
        yield a	  # Returns control and waits next call.
        a += 1
   
def run():
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.show()

fig = plt.figure(figsize=(10, 10))

root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# Just showing menu elements
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

tkinter.mainloop() # Wait for interactions.