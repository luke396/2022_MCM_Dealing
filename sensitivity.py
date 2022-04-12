import numpy as np
from SALib.analyze import sobol
from SALib.sample import saltelli
import pandas as pd
from main_MACD_and_pairs import model
from matplotlib import pyplot as plt
# Define the model inputs
problem = {
    'num_vars': 1,
    'names': 'money',
    'bounds': [[100, 10000]]
}


param_values = saltelli.sample(problem, 1024)
Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    Y[i] = model(X)

Si = sobol.analyze(problem, Y)
print('done')

from SALib.plotting.bar import plot as barplot
import matplotlib.pyplot as plot

plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.plot(param_values, Y)
plt.figure(dpi=600)
ax.set(xlabel='Money', ylabel='Wallet',
       title='Sensitivity')
ax.grid()
fig.savefig("test.png", bbox_inches='tight')
plt.show()