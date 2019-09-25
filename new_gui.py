#!/usr/bin/python

#### IMPORTS ##################################################################

import agentframework as af

import random
random.seed(100)
import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.set_cmap('YlGn')
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

#### UPDATING  ################################################################

# (moving, eating, mating, aging, dying) AND PLOTTING
carry_on = True

def update(frame_number):
    
    global breed
    global carry_on
    #global agents

    print('Frame: ', frame_number)
    print('Number of Sheep: ', len(agents))
    
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
    global breed
    global min_age_for_preg
    global preg_duration
    global agents

    breed = breed_slider.get()
    max_age = max_age_slider.get()
    min_age_for_preg = min_preg_age_slider.get()
    preg_duration = preg_duration_slider.get()
    
    num_agents = n_slider.get()
    agents = []
    for i in range(num_agents):
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

fig = plt.figure(figsize=(10, 10)) # to be used for plotting the animation into
import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, height=400, width=600)
canvas.pack()

left_frame = tk.Frame(root, bd=5)
left_frame.place(relx=0.15, rely=0.05, relwidth=0.25, relheight=0.9, anchor='n')

main_title = tk.Label(left_frame, text="~ Sheep Sim ~")
main_title.place(relx=0.05,rely=0.0,relwidth=0.9,relheight=0.08)
main_title.config(font=("Poor Richard", 15))

n_slider = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL,label='Number of Agents')
n_slider.set(50) # SET DEFAULT NUM AGENTS
n_slider.place(relx=0.05,rely=0.08,relwidth=0.9, relheight=0.18)

max_age_slider = tk.Scale(left_frame, from_=0, to=50, orient=tk.HORIZONTAL,label='Life Expectancy')
max_age_slider.set(30) # SET DEFAULT breed on or off
max_age_slider.place(relx=0.05,rely=0.25,relwidth=0.9, relheight=0.18)

breed_slider = tk.Scale(left_frame, from_=0, to=1, orient=tk.HORIZONTAL,label='Babies?',showvalue=0)
breed_slider.set(1) # SET DEFAULT breed on or off
breed_slider.place(relx=0.2,rely=0.42,relwidth=0.55,relheight=0.15)

min_preg_age_slider = tk.Scale(left_frame, from_=0, to=50, orient=tk.HORIZONTAL,label='Fertility Age')
min_preg_age_slider.set(20) # SET DEFAULT breed on or off
min_preg_age_slider.place(relx=0.05,rely=0.57,relwidth=0.9,relheight=0.18)

preg_duration_slider = tk.Scale(left_frame, from_=0, to=50, orient=tk.HORIZONTAL,label='Pregnancy Duration')
preg_duration_slider.set(10) # SET DEFAULT breed on or off
preg_duration_slider.place(relx=0.05,rely=0.73,relwidth=0.9,relheight=0.17)


button = tk.Button(left_frame, text="Run", font=40, command=run)
button.place(relx=0.15, rely=0.92, relheight=0.08, relwidth=0.6)


right_frame = tk.Frame(root, bd=10)
right_frame.place(relx=0.64, rely=0.05, relwidth=0.68, relheight=0.9, anchor='n')


anim_placeholder = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=right_frame)
anim_placeholder._tkcanvas.pack()

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