#!/usr/bin/python

#### IMPORTS ##################################################################

import agentframework as af

import random
random.seed(100)

import numpy as np # for getting sum of values in the environment matrix easily

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#plt.set_cmap('YlGn') ## CAUSES tk CHECKBUTTON TO NOT WORK!!!!!
import matplotlib.animation as anim

###### INITIALISE #############################################################

# set default global variables #################

num_agents = 50
num_iters = 2000

max_age = 30
min_age_for_preg = 20
preg_duration = 10
#neighbourhood = 20

#### IMPORT ENVIRONMENT

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
    # max is 245. Choose 250 as max grass level
    return environment
environment = import_environment()
#### UPDATING  ################################################################

# (moving, eating, mating, aging, dying) AND PLOTTING
carry_on = True

def update(frame_number):
    
    global optimised_movement
    global breed
    global carry_on
    #global agents

    # print('Frame: ', frame_number)
    # print('Number of Sheep: ', len(agents))
    
    # environment needs to be plotted at the start of every run to show developments from last run
    fig.clear()
    plt.imshow(environment, cmap='YlGn',vmin=0, vmax=250)
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
        agent.move(optimised=optimised_movement)
        agent.eat()
        if breed:
            agent.mating(preg_duration,min_age_for_preg)
        #agent.share_with_neighbours(neighbourhood)

        c = ('black' if agent.get_gender() == 'm' else 'white') # coloured based on gender
        s = (agent.get_age()/max_age)*100 # size based on age

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
        yield a # Returns control and waits next call.
        a += 1

def run():
    
    # initialise
    global num_agents
    global max_age
    global optimised_movement
    global breed
    global min_age_for_preg
    global preg_duration
    global agents

    global carry_on
    carry_on = True

    global environment
    environment = import_environment()


    optimised_movement = opt_var.get()
    breed = babies_var.get()
    print(optimised_movement,'breed: ',breed)
    max_age = max_age_slider.get()
    min_age_for_preg = min_preg_age_slider.get()
    preg_duration = preg_duration_slider.get()
    
    num_agents = n_slider.get()
    agents = []
    for _ in range(num_agents):
        agents.append(af.Agent(environment,agents)) 
        
    # run animation
    animation = anim.FuncAnimation(fig, update, frames=gen_function, repeat=False)
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
n_slider.set(50) # SET DEFAULT NUM AGENTS
n_slider.place(relx=0.05,rely=0.095,relwidth=0.9, relheight=0.18)
# max age slider
max_age_slider = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL,label='Life Expectancy')
max_age_slider.set(30) # SET DEFAULT 
max_age_slider.place(relx=0.05,rely=0.24,relwidth=0.9, relheight=0.18)
# optimised eating checkbox
opt_var = tk.IntVar()
opt_var.set(1)
optimised_chck = tk.Checkbutton(left_frame, variable = opt_var, text='Optimised Eating')
optimised_chck.place(relx=0.05,rely=0.4,relwidth=0.9,relheight=0.06)

# line
separator_line = tk.Frame(left_frame,bg='grey')
separator_line.place(relx=0.05,rely=0.47,relheight=0.001,relwidth=0.9)

# reproduction checkbox
babies_var = tk.IntVar()
babies_var.set(1)
optimised_chck = tk.Checkbutton(left_frame, variable = babies_var, text='Reproduction')
optimised_chck.place(relx=-0.01,rely=0.475,relwidth=0.9,relheight=0.1)
# min age for pregnancy slider
min_preg_age_slider = tk.Scale(left_frame, from_=0, to=50, orient=tk.HORIZONTAL,label='Fertility Age')
min_preg_age_slider.set(20) # SET DEFAULT 
min_preg_age_slider.place(relx=0.05,rely=0.57,relwidth=0.9,relheight=0.18)
# pregnancy duration slider
preg_duration_slider = tk.Scale(left_frame, from_=0, to=50, orient=tk.HORIZONTAL,label='Pregnancy Duration')
preg_duration_slider.set(10) # SET DEFAULT 
preg_duration_slider.place(relx=0.05,rely=0.73,relwidth=0.9,relheight=0.17)
# run button
button = tk.Button(left_frame, text="Run", font=40, command=run)
button.place(relx=0.15, rely=0.92, relheight=0.08, relwidth=0.6)


# fill plotting panel (right_frame) ##########

fig = plt.figure(figsize=(15, 15)) 
fig.set_facecolor('#F0F0F0')
fig.clear()
plt.imshow(environment, cmap='YlGn', vmin=0, vmax=250)
plt.xlim(0,300)
plt.ylim(0,300)
plt.axis('off')

anim_placeholder = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=right_frame)
anim_placeholder._tkcanvas.pack()

# start gui
root.mainloop()


###############################################################################

#btn1 = tk.Button(root, text = "Run", relief="raised", command = toggle)
#def toggle():
#    if btn1.config('relief')[-1] == 'sunken':
#        run()
#        btn1.config(relief="sunken",text='Stop')
#    else:
#        stop()
#        btn1.config(relief="raised",text='Run')