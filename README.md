# Sheep Sim (°ꈊ°)

Submission for Assessnent 1 of GEOG5995 at the University of Leeds

## Website

https://amiraliemami.github.io/leedsmodule/

## Workbook

Practicals 1 to 9 are presented in a Jupyter Notebook, included in the repository and also hosted [here](https://nbviewer.jupyter.org/github/amiraliemami/leedsmodule/blob/master/Jupyter%20Workbook.ipynb).

## Model and GUI

#### ------- object diagram -------

The final model and extras are presented by ```model.py```, using ```agentframework.py``` for definition of the agents and their attributes and methods.

To run the model and load the GUI, run the following:
```bash
python model.py
```

Extra features of model:

- Death - sheep die after reaching maximum life expectancy (adjustable in GUI, default 60)
- Optimised movement - move to position which has most grass, instead of random
- Seeding for spawning - random or set, allowing repeated experiments
- Reproduction - female sheep (white) can be impregnated by male sheep (black) if both sheep have sufficient store (default 50), are close enough (default within 20), and are of fertility age (adjustable in GUI, default 20)
- Pregnancy takes time - female sheep get pregnant, and after a number of turns (adjustable in GUI, default 10), give birth to a new sheep nearby.
- Defaults button - reset all values to default
- Start/Kill/Restart button - can stop and restart simulation (even with changed parameters) without having to rerun the script.

## Testing

To run the unit tests, simply run the following script:
```bash
python tests.py
```

Other tests that were run during the development process:

1. Made sure that slider values are passed into the run function in ```model.py``` as expected.
2. Fixed frame number edge-cases to make sure first frame was spawn, then move and eat and mate were in the correct order
3. Whether there was need for randomisation of the agents list (as this was causing drawing flickers) - answer is no 
4. Made sure 'optimised movement' did not get stuck by addin random movement if this happens 
5. Type and value checking was added to the main python scripts and mistakes will be caught by them
6. ```move()```, ```eat()```, and ```mate()``` were checked against their behaviours in the simulation

## Documentation

link.com


## License
[MIT](https://choosealicense.com/licenses/mit/)
