#!/usr/bin/python


#### Imports

import agentframework as af

import random

import numpy as np # for getting sum of values in the environment matrix easily

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt     #plt.set_cmap('YlGn') ## CAUSES tk CHECKBUTTON TO NOT WORK!!!!!
import matplotlib.animation as anim

import tkinter as tk

### global variable to control animation start/stop
carry_on = True

#### functions for running the model and GUI: moving, eating, mating, aging, dying

def update_labels(frame_for_display,num_agents_for_display):
    """To be used within the update() function to update the display of frame number and number of sheep.
    
    Arguments:
        frame_for_display (int): frame number
        num_agents_for_display (agents): number of sheep alive in the scene
    
    Requires global:
        run_button (tkinter button)
        n_label (tkinter label)
        frame_label (tkinter label)
    """
    n_text = "{} sheep grazing".format(num_agents_for_display)
    if num_agents_for_display == 0:
        n_text = "All dead!"
        run_button.config(text='Restart', bg='#268B49')
    n_label.configure(text=n_text)

    frame_text = "Frame {}".format(frame_for_display)
    frame_label.configure(text=frame_text)


def update(frame_number, max_age, optimised_movement, breed, min_age_for_preg, preg_duration, agents, environment):
    """To be used by FuncAnimation from matplotlib to update the simulation.
    
    Arguments passed through by the run() function which calls this update() function.
    
    Argument: 
        frame_number (int): provided by FuncAnimate()
        max_age (int)
        optimised_movement (bool)
        breed (bool)
        min_age_for_preg (int)
        preg_duration (int)
        agents (list of Agent classes)
        environment (list of list of numbers)

    Global:
        carry_on (bool)
    """

    if frame_number == 0:
        # frame 0 occurs twice, and first call does not draw, hence exclude
        return

    global carry_on
    
    # update the frame number and number of sheep displayed in the GUI
    update_labels(frame_number-1,len(agents))
    ##### print number of sheep to console
    print('Frame: ', frame_number-1)
    print('Number of Sheep: ', len(agents))

    # re-plot environment at the start of every update to show developments during last update
    fig.clear()
    plt.imshow(environment, cmap='YlGn', vmin=0, vmax=250)
    plt.xlim(0,300)
    plt.ylim(0,300)
    plt.axis('off')

    # simulation stopping conditions. Exit function using 'return'.
    if len(agents) == 0:
        print('All dead!')
        carry_on = False
        return
    elif np.array(environment).sum() == 0:
        print("All grass eaten!")
        carry_on = False
        return

    # shuffle agents before each iteration to try to avoid artifacts caused by order of execution
    #random.shuffle(agents)

    # make an empty list to populate with sheep that die this round, if any
    the_dead = []

    # run through each sheep and perform actions and plot it on the environment
    for agent in agents:

        # set colour based on gender
        c = ('black' if agent.get_gender() == 'm' else 'white')
        # set size relative to maximum age (oldest = biggest)
        s = ((agent.get_age()+1)/(max_age+1))*100

        if agent.is_dead(max_age):
            # check if this sheep is at max age, and let it die peacefully if so.
            the_dead.append(agent)
            plt.scatter(agent.get_x(),agent.get_y(),s=s,c=c,marker='1') # Plot him as a skeleton
        else:
            # if still alive, let him live and PERFORM ACTIONS

            # plot it (first round, plots initial position)
            plt.scatter(agent.get_x(),agent.get_y(),s=s,c=c,marker='*')

            # change sick_enabled to True to activate throwing up
            agent.eat(max_grass_per_turn=20, sick_enabled=False)
            # perform actions
            agent.move(optimised=optimised_movement)
            if breed:
                agent.mating(preg_duration,min_age_for_preg)
            #agent.share_with_neighbours(20) # un-comment to activate sharing with neighbours.

            # age it
            agent.increment_age()
            
    # remove all who died in this round in one go
    for dead_agent in the_dead:
        agents.remove(dead_agent)


def gen_function():
    """To be used by FuncAnimation from matplotlib to progress the simulation.
    Maximum number of frames chosen to be 2,000.

    Global:
        carry_on (bool): if false, gen function does not increase the frame number
    """
    a = 0
    global carry_on
    while carry_on: 
        # maximum number of frames for a given simulation set at 2,000
        if a < 2000:
            yield a # Returns and awaits next call.
            a += 1

def run():
    """Reads in parameters from silders and checkboxes and initiates the animation to be plotted. 
    Used by run_stop_toggle to initiate simulation on buttonpress.
    """

    # make the button reusable by resetting carry_on to True every run
    global carry_on
    carry_on = True

    # re-import the clean environment for every run of the simulation
    environment = af.import_environment()

    # read parameters from the GUI widgets
    optimised_movement = opt_var.get()
    breed = babies_var.get()
    max_age = max_age_slider.get()
    min_age_for_preg = min_preg_age_slider.get()
    preg_duration = preg_duration_slider.get()
    num_agents = n_slider.get()

    # print parameters to console
    print(
    '\n#### Run started with parameters:\n\
    {} agents\n\
    {} max age\n\
    {} movement\n\
    {} breeding\n\
    {} minimum age for pregnancy\n\
    {} duration of pregnancy\n'\
        .format(
        num_agents,
        max_age,
        ('Optimised' if optimised_movement else 'Random'),
        ('Enabled' if breed else 'Disabled'),
        min_age_for_preg,
        preg_duration
        )
    )

    # create initial list of agents
    # set seed to always create the same agents
    random.seed(0)
    agents = []
    for _ in range(num_agents):
        agents.append(af.Agent(environment,agents)) 
    
    # run animation, passing the parameters initiated here to the update() function through 'fargs'
    animation = anim.FuncAnimation(
        fig, 
        update, 
        # arguments for update():
        fargs=(max_age, optimised_movement, breed, min_age_for_preg, preg_duration, agents, environment),
        frames=gen_function, 
        repeat=False
        )
    # and place it into the GUI
    anim_placeholder.draw()


def start_kill_toggle():
    """Function to be used by the run_button to start, kill, and restart the simulation. Implements the following functionality:
    
    1. If button is pressed for the first time, the simulation is run() and the button text changes to "Kill" and its colour to normal.
    2. If the now "Kill" button is pressed, simulation is stopped and text changed to "Restart" and to green colour.
    3. If the now "Restart" button is pressed, the simulation is re-run with new parameters from the GUI, and text changed to "Kill" and colour to normal. 
    4. 2 and 3 are then repeated.

    Functionality for returning this button to "Restart" if all sheep die is implemented in update_labels().
    """
    
    current_text = run_button.config("text")[-1]
    if current_text == 'Start' or current_text == 'Restart':
        run()
        run_button.config(text='Kill', bg='red3')
    elif current_text == 'Kill':
        global carry_on
        carry_on = False
        run_button.config(text='Restart', bg='#268B49')


#### TKINTER GUI SETUP ##############################################################

# setup of root, canvas, and frames
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
main_title = tk.Label(left_frame, text="Sheep  (°ꈊ°)  Sim")
main_title.place(relx=0,rely=-0.02,relwidth=1,relheight=0.08)
main_title.config(font=("Poor Richard", 16))

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
opt_var = tk.IntVar(root)
optimised_chck = tk.Checkbutton(left_frame, variable = opt_var, text='Optimised Eating')
optimised_chck.place(relx=0.05,rely=0.4,relwidth=0.9,relheight=0.06)

# line
separator_line = tk.Frame(left_frame,bg='grey')
separator_line.place(relx=0.05,rely=0.47,relheight=0.001,relwidth=0.9)

# reproduction checkbox
babies_var = tk.IntVar(root)
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
    """Requires the GUI widgets to exist before it is called."""
    n_slider.set(50)
    max_age_slider.set(30)
    max_age_slider.set(30)
    opt_var.set(1)
    babies_var.set(1)
    min_preg_age_slider.set(20)
    preg_duration_slider.set(10)

set_defaults() # initiate to set the defaults upon first loading the GUI

# add reset to defaults button
defaults_button = tk.Button(left_frame, text="Defaults", command=set_defaults)
defaults_button.place(relx=0.07, rely=0.93, relwidth=0.37, relheight=0.07)

# add run button
run_button = tk.Button(left_frame, text="Start", font=100, fg='white', bg='#268B49', command=start_kill_toggle)
run_button.place(relx=0.50, rely=0.92, relwidth=0.42, relheight=0.09)


# fill plotting panel (right_frame) ##########

fig = plt.figure(figsize=(15, 15)) 
fig.set_facecolor('#F0F0F0')
fig.clear()
# plot environment to fill empty space/give a sense of the simulation pre-run
environment = af.import_environment()
plt.imshow(environment, cmap='YlGn', vmin=0, vmax=250)
plt.xlim(0,300)
plt.ylim(0,300)
plt.axis('off')

anim_placeholder = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=right_frame)
anim_placeholder._tkcanvas.place(relx=0,rely=0,relwidth=1,relheight=1)

# show number of agents beneath the animation window, these will be updated by the update_labels() function within the update() function
n_label = tk.Label(right_frame,text="",anchor=tk.E)
n_label.place(relx=0.4,rely=0.9,relwidth=0.5,relheight=0.05)
frame_label = tk.Label(right_frame, text="",anchor=tk.W)
frame_label.place(relx=0.12,rely=0.9,relwidth=0.5,relheight=0.05)

# start gui
root.mainloop()