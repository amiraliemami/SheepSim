## Model:
# Make a y variable.
# Make a x variable.
# Change y and x based on random numbers.
# Make a second set of y and xs, and make these change randomly as well.
# Work out the distance between the two sets of y and xs.

y0, x0 = 50, 50 # y then x because of reading image files
print('Initial: ',x0,y0)

from random import choice
def perturb(x): 
    pert = choice([-1,1])
    return x + pert

x0, y0 = perturb(x0), perturb(y0) 
print('Perturbed: ',x0, y0)

x, y = x0, y0
for _ in range(5):
    x, y = perturb(x), perturb(y)
print('5 more steps... ', x, y)

import numpy as np
def distance(x0,y0,x1,y1):
    return np.sqrt((x1-x0)**2 + (y1-y0)**2)

distance(x0,y0,x,y)