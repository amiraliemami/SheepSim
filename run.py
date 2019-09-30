#!/usr/bin/python

#### IMPORTS ##################################################################

import agentframework as af

import random
random.seed(100)

import numpy as np # for getting sum of values in the environment matrix easily

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt     #plt.set_cmap('YlGn') ## CAUSES tk CHECKBUTTON TO NOT WORK!!!!!
import matplotlib.animation as anim

###### INITIALISE #############################################################

#### function for importing the environment from file
def import_environment():
    environment = []
    with open('data/in.txt') as f:
        for line in f:
            parsed_line = line.split(',')
            rowlist = []
            for value in parsed_line:
                rowlist.append(int(value))
            environment.append(rowlist)
    #print('Max of environment: ',max(max(environment))) 
    # we find that max is 245. Choose 250 as max grass level for imshow().
    return environment

# set default global variables #################

#neighbourhood = 20

# set variables for display in the GUI
num_agents_for_display = "--"
frame_for_display = "--"

# variable to control animation start/stop
carry_on = True

#### functions for running the model and GUI  ######## moving, eating, mating, aging, dying ##########################

def update(frame_number):
    """To be used by FuncAnimation from matplotlib to update the simulation."""
    
    global optimised_movement
    global breed

    global carry_on

    global frame_for_display
    global num_agents_for_display

    # update variables to be picked up later and displayed in the GUI
    frame_for_display = frame_number
    num_agents_for_display = len(agents)

    # # print number of sheep to console every 5 frames:
    # if frame_number%5 == 0:
    #     print('Frame: ', frame_number)
    #     print('Number of Sheep: ', num_agents_for_display)
    
    # environment needs to be re-plotted at the start of every update to show developments during last update
    fig.clear()
    plt.imshow(environment, cmap='YlGn', vmin=0, vmax=250)
    plt.xlim(0,300)
    plt.ylim(0,300)
    plt.axis('off')

    # simulation stopping conditions
    if len(agents) == 0:
        print('All dead!')
        carry_on = False
    elif np.array(environment).sum() == 0:
        carry_on = False
        print("All grass eaten!")

    # shuffle agents before each iteration
    random.shuffle(agents)

    the_dead = []

    # run through each sheep and perform actions and plot it on the environment
    for agent in agents:

        ######### perform actions

        agent.move(optimised=optimised_movement)
        agent.eat(max_grass_per_turn=20, sick_enabled=False)
        if breed:
            agent.mating(preg_duration,min_age_for_preg)
        #agent.share_with_neighbours(neighbourhood)

        ######### plot this sheep

        # set colour based on gender
        c = ('black' if agent.get_gender() == 'm' else 'white')
        # set size relative to maximum age (oldest = biggest)
        s = (agent.get_age()/max_age)*100

        # check if this sheep dies at the end of this turn
        if agent.is_dead(max_age):
            the_dead.append(agent)
            plt.scatter(agent.get_x(),agent.get_y(),s=s,c=c,marker='1')
        else:
            agent.increment_age()
            plt.scatter(agent.get_x(),agent.get_y(),s=s,c=c,marker='*')
    
    # remove all who died in this round in one go
    for dead_agent in the_dead:
        agents.remove(dead_agent)


def gen_function():
    """To be used by FuncAnimation from matplotlib to progress the simulation."""
    a = 0
    global carry_on
    while carry_on: 
        # maximum number of frames for a given simulation set at 2,000
        if a < 2000:
            yield a # Returns control and awaits next call.
            a += 1

def run():
    """Reads in parameters from silders and checkboxes and initiates the animation to be plotted."""

    # initialise
    global num_agents
    global max_age
    global optimised_movement
    global breed
    global min_age_for_preg
    global preg_duration
    global agents

    # makes the button reusable
    global carry_on
    carry_on = True
    # re-import the clean environment for every run of the simulation
    global environment 
    environment = import_environment()

    # read in simulation parameters from the GUI widgets
    optimised_movement = opt_var.get()
    breed = babies_var.get()
    max_age = max_age_slider.get()
    min_age_for_preg = min_preg_age_slider.get()
    preg_duration = preg_duration_slider.get()
    num_agents = n_slider.get()

    # create initial list of agents
    agents = []
    for _ in range(num_agents):
        agents.append(af.Agent(environment,agents)) 
    
    print('Run started with {} agents'.format(num_agents))

    # run animation
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    # and place it into the GUI
    anim_placeholder.draw()


def stop():
    global carry_on
    carry_on = False
def cont():
    global carry_on
    carry_on = True
    
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    anim_placeholder.draw()


#### TKINTER GUI ##############################################################

import tkinter as tk

# setup
root = tk.Tk()
root.title('Sheep Sim - Amir')

canvas = tk.Canvas(root, height=470, width=660)
canvas.pack()
left_frame = tk.Frame(root, bd=5)
left_frame.place(relx=0.15, rely=0.05, relwidth=0.25, relheight=0.9, anchor='n')
right_frame = tk.Frame(root,bd=5)
right_frame.place(relx=0.64, rely=0.02, relwidth=0.68, relheight=0.96, anchor='n')

# fill options panel (lef_frame) ##########

# title
main_title = tk.Label(left_frame, text="Sheep  °ꈊ°  Sim")
main_title.place(relx=0,rely=-0.02,relwidth=1,relheight=0.08)
main_title.config(font=("Poor Richard", 17))

# line
separator_line0 = tk.Frame(left_frame,bg='grey')
separator_line0.place(relx=0.05,rely=0.08,relheight=0.001,relwidth=0.9)

# number of agents slide
n_slider = tk.Scale(left_frame, from_=1, to=120, orient=tk.HORIZONTAL,label='Number of Agents')
n_slider.place(relx=0.05,rely=0.095,relwidth=0.9, relheight=0.18)
# max age slider
max_age_slider = tk.Scale(left_frame, from_=1, to=100, orient=tk.HORIZONTAL,label='Life Expectancy')
max_age_slider.place(relx=0.05,rely=0.24,relwidth=0.9, relheight=0.18)
# optimised eating checkbox
opt_var = tk.IntVar()
optimised_chck = tk.Checkbutton(left_frame, variable = opt_var, text='Optimised Eating')
optimised_chck.place(relx=0.05,rely=0.4,relwidth=0.9,relheight=0.06)

# line
separator_line = tk.Frame(left_frame,bg='grey')
separator_line.place(relx=0.05,rely=0.47,relheight=0.001,relwidth=0.9)

# reproduction checkbox
babies_var = tk.IntVar()
optimised_chck = tk.Checkbutton(left_frame, variable = babies_var, text='Reproduction')
optimised_chck.place(relx=-0.01,rely=0.475,relwidth=0.9,relheight=0.1)
# min age for pregnancy slider
min_preg_age_slider = tk.Scale(left_frame, from_=0, to=50, orient=tk.HORIZONTAL,label='Fertility Age')
min_preg_age_slider.place(relx=0.05,rely=0.57,relwidth=0.9,relheight=0.18)
# pregnancy duration slider
preg_duration_slider = tk.Scale(left_frame, from_=1, to=50, orient=tk.HORIZONTAL,label='Pregnancy Duration')
preg_duration_slider.place(relx=0.05,rely=0.73,relwidth=0.9,relheight=0.17)

# set defaults
def set_defaults():
    n_slider.set(50)
    max_age_slider.set(30)
    max_age_slider.set(30)
    opt_var.set(1)
    babies_var.set(1)
    min_preg_age_slider.set(20)
    preg_duration_slider.set(10)
# call to set defaults upon loading the GUI
set_defaults()

# reset to defaults button
button = tk.Button(left_frame, text="Defaults", command=set_defaults)
button.place(relx=0.1, rely=0.935, relwidth=0.37, relheight=0.07)

# run button
button = tk.Button(left_frame, text="►", font=100, command=run)
button.place(relx=0.54, rely=0.92, relwidth=0.36, relheight=0.09)


# fill plotting panel (right_frame) ##########

fig = plt.figure(figsize=(15, 15)) 
fig.set_facecolor('#F0F0F0')
fig.clear()
# plot environment to fill empty space/give a sense of the simulation pre-run
environment = import_environment()
plt.imshow(environment, cmap='YlGn', vmin=0, vmax=250)
plt.xlim(0,300)
plt.ylim(0,300)
plt.axis('off')

anim_placeholder = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=right_frame)
anim_placeholder._tkcanvas.place(relx=0,rely=0,relwidth=1,relheight=1)

# show number of agents beneath the animation window
n_label = tk.Label(right_frame,text="",anchor=tk.E)
n_label.place(relx=0.4,rely=0.9,relwidth=0.5,relheight=0.05)
# frame_label = tk.Label(right_frame, text="",anchor=tk.E)
# frame_label.place(relx=0.4,rely=0.05,relwidth=0.5,relheight=0.05)

def update_labels():
    n_text = "{} sheep grazing".format(num_agents_for_display)
    if num_agents_for_display == 0:
        n_text = "All dead!"
    n_label.configure(text=n_text)

    # frame_text = "Frame {}".format(frame_for_display)
    # frame_label.configure(text=frame_text)

    root.after(100, update_labels)

# run updates
update_labels()

# start gui
root.mainloop()