# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 09:47:11 2020

@author: AlexM

Plot IR data
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

"""
Plots several sets of spectra on the same graph if file array contains more than one file.
Main reads each of the files in the file array and appends each data set to an overall array, for frequencies and absorbances.
Then plots this data.
"""
def main():
    filearray = ['measurements\MABr_2000.dpt','measurements\MAPbBr3_2000.dpt', 'measurements\PbMOF_2000.dpt','measurements\\NCMOF_2000.dpt']
    allfreqdata = []
    allabsorbancesdata = []
    for file in filearray:
        frequencies,absorbances = readData(file)
        allfreqdata.append(frequencies)
        allabsorbancesdata.append(absorbances)
    plotData(allfreqdata,allabsorbancesdata,filearray)

"""
readData:
Input is filename for a file of dpt filetype (Two columns separated by 'space' character). Creates two lists , one for each column of the file.  
Assumes frequencies are on the left column and absorbances on the right.
Returns the frequencies and absorbances for that file in two lists.
"""
def readData(Filename):
    file = open(Filename, "r")
    lines = file.readlines()
    frequencies = []
    absorbances = []
    for data in lines:
        frequencies.append(data.split('\t')[0])
        absorbances.append(data.split('\t')[1])
    absorbances = [i.replace('\n','') for i in absorbances]            
    file.close()
    "floats are important!"
    #set to float or else its an array strings, which messes up plotting.
    frequencies = [float(i) for i in frequencies]
    absorbances = [float(i) for i in absorbances]

    return frequencies,absorbances

"""
Plots each data set by taking in the main list of lists (all frequencies and all absorbances). 
Then applies annotations and cleans axis ticks etc. 
Input filearray to determine the plot legend lables.
"""    
def plotData(allfrequencies, allabsorbances,filearray):
    plt.figure(figsize=(20,15))
    ax = plt.subplot(1,1,1)
    x = []
    y = []
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  
    dataSetNames = [filename.replace('measurements\\','').replace('_2000.dpt','') for filename in filearray]
    for dataSet in range (len(allfrequencies)):
        y = np.array(allabsorbances[dataSet])
        x = np.array(allfrequencies[dataSet])
        plt.plot(x,y, '-',label = dataSetNames[dataSet])
        plt.hlines(0,min(x),max(x),linestyle='--')
    plt.grid()
    
    min_y = -0.08
    max_y = 0.26
    
    plt.vlines(929,min_y,max_y,linestyle='--',color='r')
    plt.vlines(1080,min_y,max_y,linestyle='--',color='r')
    
    plt.vlines(1650,min_y,max_y,linestyle='--',color='r')
    plt.vlines(1950,min_y,max_y,linestyle='--',color='r')
    
    ax.annotate('1,3-Butadiene (~916)', xy=(916, 0.26), xytext=(950, 0.265),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    ax.annotate('Or 2-Propenal (~916)', xy=(916, 0.26), xytext=(950, 0.255)
            )
    ax.annotate('2-Butanone (~936)', xy=(936, 0.01), xytext=(900, -0.03),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    ax.annotate('Or Propane', xy=(936, 0.01), xytext=(900, -0.04)
            )
    ax.annotate('1,3-Butadiene or 1,4-Dioxane (~1014)', xy=(1014, 0.01), xytext=(1100, -0.03),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    ax.annotate('Benzene (848-852)', xy=(850, 0.068), xytext=(730, 0.11),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    ax.annotate('? (718-722)', xy=(718, 0.152), xytext=(600, 0.18),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    ax.annotate('(1692-1693)', xy=(1693, 0.1), xytext=(1693, 0.12),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    ax.annotate('(999-1001)', xy=(1000, 0.12), xytext=(995, 0.14),
            arrowprops=dict(arrowstyle="->",facecolor='black'),
            )
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Absorbance %')
    plt.title('ATR IR for MAPbBr3@MOF and References', fontsize=20)
    plt.legend(loc='upper right',fontsize=18)#location of the key
    plt.show()
  
main()

