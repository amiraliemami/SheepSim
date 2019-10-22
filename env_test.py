import matplotlib.pyplot as plt
import agentframework as af

environment = af.import_environment()
plt.imshow(environment, cmap='YlGn', vmin=0, vmax=250)
plt.show()