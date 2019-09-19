#!/usr/bin/python

#### IMPORTS #####################################################################

import agentframework as af

import random
random.seed(100)
import numpy as np

import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.set_cmap('YlGn')
import matplotlib.animation as anim

#### UPDATING  ###############################################################

# (moving, eating, mating, aging, dying) AND PLOTTING
carry_on = True
def update(frame_number):
    
    print('Frame: ', frame_number)
    print('Number of Sheep: ', len(agents))

    global carry_on
    global environment
    global breed

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
        if breed:
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
    
    # remove all who died in this round at once, as this resolves problems that are caused if removed at instance of death
    for dead_agent in the_dead:
        agents.remove(dead_agent)

#### Setup animation and GUI ##################################################

def gen_function():
    a = 0
    global carry_on
    while (a < num_iters) and carry_on:
        yield a	  # Returns control and waits next call.
        a += 1

def run():
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    plot_area.draw()

def stop():
    global carry_on
    carry_on = False

def toggle():
    if btn1.config('relief')[-1] == 'sunken':
        run()
        btn1.config(relief="sunken",text='Stop')
    else:
        stop()
        btn1.config(relief="raised",text='Run')


###### INITIALISE ###############################################################

# set default global variables #################

num_iters = 2000 # max iterations the sim will run for
max_age = 50
min_age_for_preg = 10
preg_duration = 10
neighbourhood = 20

fig = plt.figure(figsize=(5, 5))

##### tk GUI ############################################################

root = tk.Tk()
root.title("Model")


tk.Label(root, text = "Number of Agents").grid(row=0,column=0)
n_agents_entry = tk.Entry(root).grid(row=0,column=1)

chck_var = tk.IntVar()
chck = tk.Checkbutton(root, text = "Breeding",variable=chck_var).grid(row=1,column=0)
breed = (chck_var.get() == 1)

# set number of agents based on user input
if n_agents_entry is not None:
    print(n_agents_entry)
    num_agents = int(n_agents_entry)
else:
    num_agents = 30 # DEFAULT

#### initiate agents based on num_agents required ############
agents = []
for i in range(num_agents):
    agents.append(af.Agent(environment,agents)) 


tk.Label(root, text = "Run?").grid(row=2,column=0)
btn1 = tk.Button(root, text = "Run", relief="raised", command = toggle)
btn1.grid(row=2,column=1)

plot_area = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
plot_area._tkcanvas.grid(columnspan=3)

root.mainloop()









