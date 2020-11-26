# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import signal
from scipy import stats
from scipy.stats import gaussian_kde
from scipy.stats import norm
from scipy.stats import cauchy
from matplotlib.ticker import FormatStrFormatter
from sklearn import preprocessing

"""

"""
def main():
    mol_file = 'MAPbBr3\MAPbBr3-VIBRATIONS-1.mol'
    frequencies = []
    intensities = []
    frequencies,intensities = readData(mol_file)
    min_freq = 0
    max_freq = 5000
    frequencies,intensities = select_freq_range(frequencies,intensities,min_freq,max_freq)
    plotData(frequencies,intensities,"gaussian")
"""
readData:
"""
def readData(Filename):
    frequencies = []
    intensities = []
    vibration = 0
    freq_boolean = False 
    "intensity"
    int_boolean = False
    with open(Filename) as f:
        data = f.readlines()
        """File read as a list of lines. 
        Once it reads the FREQ header, set a boolean to true and start appending lines. 
        Once it hits the next header, set the boolean to false to stop collecting lines. 
        Perform same action for the INT header."""
        for line in data:
            if "vibration" in line:
                vibration = vibration+1
            if "FREQ" in line: 
                freq_boolean = True 
            if freq_boolean == True: 
                frequencies.append(line.strip(' \n'))
            if "FR-COORD" in line: 
                freq_boolean = False
            if "INT" in line: 
                int_boolean = True
            if int_boolean == True: 
                intensities.append(line.strip(' \n'))
    f.close()
    "Remove the headers from lists"
    frequencies.remove('[FREQ]')
    frequencies.remove('[FR-COORD]')
    intensities.remove('[INT]')
    "floats are important!"
    #set to float or else its an array strings, which messes up plotting.
    frequencies = [float(i) for i in frequencies]
    intensities = [float(i) for i in intensities]

    return frequencies,intensities

    """
    Compute the gaussian KDE from the given sample.

    Args:
        data (array or list): sample of values
        width (float): width of the normal functions
        gridsize (int): number of grid points on which the kde is computed
        normalized (bool): if True the KDE is normalized (default)
        bounds (tuple): min and max value of the kde

    Returns:
        The grid and the KDE
    """
def my_kde(frequencies,width,intensities,lineshape, gridsize=100, normalized=True, bounds=None):
    # boundaries
    if bounds:
        xmin, xmax = bounds
    else:
        xmin = min(frequencies) - 3 * width
        xmax = max(frequencies) + 3 * width

    # grid points
    x = np.linspace(xmin, xmax, gridsize)

    # compute kde
    kde = np.zeros(gridsize)
    if lineshape == "gaussian":
        for val in enumerate(frequencies):
            kde += norm.pdf(x, loc=val[1], scale=width)*intensities[val[0]]
    elif lineshape == "lorenzian":
        for val in enumerate(frequencies):
            kde += cauchy.pdf(x, loc=val[1], scale=width)*intensities[val[0]]        
    # normalized the KDE
    if normalized:
        kde /= sp.integrate.simps(kde, x)
    return x, kde

def lorentzian(x, x0, a, gam):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def select_freq_range(frequencies,intensities,min_freq,max_freq):
    for i in frequencies[:]:
        if i > max_freq:
            index = frequencies.index(i)
            frequencies.remove(i)
            intensities.pop(index)
        if i < min_freq:
            index = frequencies.index(i)
            frequencies.remove(i)
            intensities.pop(index)
    print('freq: '+ str(frequencies))
    print('int: '+ str(intensities))
    return frequencies,intensities
"""
"""    
def plotData(frequencies,intensities,lineshape):  
    width = 20
    
    x,kde = my_kde(frequencies,width,intensities,"lorenzian")
    
    # normalize the data attributes
    normalized_kde = preprocessing.normalize(np.array(kde).reshape(1,-1))
    normalized_int = preprocessing.normalize(np.array(intensities).reshape(1,-1))

    #plot
    plt.vlines(frequencies,0,normalized_int)
    plt.plot(x,normalized_kde[0])

main()

