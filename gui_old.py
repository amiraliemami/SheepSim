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

max_age = 30
min_age_for_preg = 5
preg_duration = 1

neighbourhood = 20

###############################################

##### COMMANDLINE: n_agents n_iters neighbourhood_size
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

#### READ POSITIONS FROM FILE
from_file = False
if from_file:
    import requests
    from bs4 import BeautifulSoup

    r = requests.get('https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html',verify=False)
    page = r.text
    soup = BeautifulSoup(page,'html.parser')
    xs = soup.find_all(attrs={"class": "x"})
    ys = soup.find_all(attrs={"class": "y"})
    num_agents = len(xs) # overwrite num_agents  ########## IMPORTANT

    agents = []
    for i in range(num_agents):
        ### FOR IMPORTING POSITIONS FROM URL
        init_coords = [int(xs[i].text)*3,int(ys[i].text)*3]
        agents.append(af.Agent(environment,agents,init_coords))


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
   
def run():
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

fig = plt.figure(figsize=(10, 10))

root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# Showing menu elements
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

# Run GUI
tkinter.mainloop()