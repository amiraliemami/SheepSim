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


###### INITIALISE ###############################################################

# set default global variables #################

num_iters = 2000 # max iterations the sim will run for
max_age = 50
min_age_for_preg = 10
preg_duration = 10

neighbourhood = 20

#### initiate agents based on num_agents required ############
agents = []
for i in range(num_agents):
    agents.append(af.Agent(environment,agents)) 

fig = plt.figure(figsize=(5, 5))

##### tk GUI ############################################################

root = tk.Tk()
root.title("Model")

canvas = tk.Canvas(root,height=700,width=700).pack()
frame = tk.Frame(root,bg='#ffffff').place(relx=0.05,rely=0.05,relheight=0.90,relwidth=0.90)

label = tk.Label(canvas, text = "Run?")
label.pack()


#chck_var = tk.IntVar()
#chck = tk.Checkbutton(frame, text = "Breeding",variable=chck_var)
#chck.pack()
#
#breed = (chck_var.get() == 1)
#
#tk.Label(frame, text = "Number of Agents").pack()
#n_agents_entry = tk.Entry(frame).pack()
#
## set number of agents based on user input
#if n_agents_entry is not None:
#    print(n_agents_entry)
#    num_agents = int(n_agents_entry)
#else:
#    num_agents = 30 # DEFAULT
#    
#tk.Label(frame, text = "Run?").pack() # this is placed in 0 0 
#btn1 = tk.Button(frame, text = "Run",command = run).pack()
#
#plot_area = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
#plot_area._tkcanvas.pack()

root.mainloop()



## Showing menu elements
#menu_bar = tk.Menu(root)
#root.config(menu=menu_bar)
#model_menu = tk.Menu(menu_bar)
#menu_bar.add_cascade(label="Model", menu=model_menu)
#model_menu.add_command(label="Run model", command=run)

# Run GUI
#tk.mainloop()