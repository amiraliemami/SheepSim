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
plt.set_cmap('viridis')
import matplotlib.animation as anim

###### INITIALISE ###############################################################

# set default global variables
num_agents = 20
num_iters = 2000
neighbourhood = 20

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


#### FOR TESTING OF MATING

# positions = [[50,50],[52,52],[55,55]]
# genders = ['m','f','f']
# num_agents = len(positions)
# agents = []
# for i in range(num_agents):
#     agents.append(af.Agent(environment,agents,positions[i],genders[i]))  

agents = []
for i in range(num_agents):
    agents.append(af.Agent(environment,agents)) 

#### UPDATING  ###############################################################

# (moving, eating, mating, aging, dying) AND PLOTTING
carry_on = True
def update(frame_number):
    
    fig.clear()
    global carry_on
    
    random.shuffle(agents) # shuffle agents before each iteration
    num_agents = len(agents) # update num_agents
    print('Number of sheep: ',num_agents)

    for agent in agents:
        agent.move()
        agent.eat()
        #agent.share_with_neighbours(neighbourhood)
        agent.mating()

        # check if it dies at the end of this turn
        dead = agent.increment_age_or_die(10)
        
        plt.scatter(agent.get_x(),agent.get_y(),
                    s=(agent.get_store()*0.5),
                    c=('red' if dead else 'white'),
                    marker='*')

    plt.imshow(environment, vmin=0, vmax=250) # environment needs to be plotted every run to show developments
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


# Just showing menu elements
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

tkinter.mainloop() # Wait for interactions.