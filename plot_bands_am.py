# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 16:14:20 2020

@author:AlexM

How to use:

Scroll down to function calls to define input file name (must be csv of format |kx|ky|kz|band1|band2|Bandn...)
But without headers (same as the one returned in cp2k_bs2csv.py)
Edit global variable

NUMBER_OF_KPOINTS = 50
"""
import matplotlib.pyplot as plt
import numpy as np
import csv

#Number of K-Points
N_O_K = 100

N_COLUMNS = 0
FERMI_ENERGY_SI = 5.4
FERMI_ENERGY_GRAPHENE=-0.16130908418
FERMI_ENERGY_CsPbBr3=2.530415886175609419
FERMI_ENERGY_MAPbBr3=2.19867982

PATHS_SI = [[0,100,200,250,275,300,325,375,400,525],['L','G','X','W','U','L', 'W', 'X', 'U','G']]
PATHS_GR = [[0,66,100,166],['G','K','M','G']]
PATHS_CsPbBr3 = [[0,50,100,150],['X','G','T','R']]
PATHS_MAPbBr3 = [[0,50,100,150,200],['G','S','X','Y','G']]

k_pointx = []
k_pointy = []
k_pointz = []
energies = []

#read CSV and return arrays of k points and energies
"floats are important!"
def readCSV(Filename):
    k_pointx = []
    k_pointy = []
    k_pointz = []
    energies = []
    with open(Filename) as csvfile:
        reader = csv.reader(csvfile, delimiter = ' ')
        #create list for each column
        N_COLUMNS = len(next(reader))
        number_of_bands = N_COLUMNS-3
        print('number of bands: '+str(number_of_bands))
        print('column count: '+str(N_COLUMNS))
        for row in reader:
            k_pointx.append(float(row[0]))
            k_pointy.append(float(row[1]))
            k_pointz.append(float(row[2]))
            energy = []
            for x in range(3,N_COLUMNS):
                energy_at_k_point = float(row[x])
                energy.append(energy_at_k_point)
            energies.append(energy)
    #Number of rows
    return k_pointx,k_pointy,k_pointz,energies,number_of_bands

def Extract(energies,band):
    print('band: '+str(band))
    array = [i[band] for i in energies]
    return array

def create_fermi_line(x_axis_length,fermi_energy_ev ):
    x=np.arange(0,x_axis_length,0.01)
    a=np.empty(len(x)) 
    a.fill(fermi_energy_ev) 
    return x,a

def alignXCoords(startx,endx):
    x = np.linspace(startx,endx)
    return x

def createXAxis(paths,N_O_K):  
    x=[]
    x_con=[]
    index = 1
    for path in paths:
        if index<(len(paths)):
            x_n = np.linspace(paths[index-1],paths[index],N_O_K)
            x.append(x_n)
            index +=1   
    x_con = [a for b in x for a in b]
    return x_con

def plotBands(energies,number_of_bands, fermi_energy, figure_filename, paths,N_O_K):
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(paths[0], paths[1])
    fig = plt.gcf()
    fig.set_size_inches(12.5, 7.5)
    ax.set_ylim(-20, 15)

    for energy_band_number in range(number_of_bands):
        band_energies = Extract(energies,energy_band_number)
        re_aligned_energies = [energy-fermi_energy for energy in band_energies]
        x_con = createXAxis(paths[0], N_O_K)
        plt.plot(x_con,re_aligned_energies,linewidth=4, color='b')
    x_fermi,y_fermi = create_fermi_line(max(x_con),0)
    plt.ylabel('eV')
    plt.rc('axes', labelsize=20)
    plt.rc('xtick', labelsize=20)
    plt.rc('ytick', labelsize=20)
    plt.plot(x_fermi,y_fermi,'r--')
    plt.legend(loc='best')
    plt.show()
    fig.savefig(figure_filename, dpi=100)
    
#create arrays of energies and k points
#k_pointx,k_pointy,k_pointz,energies_si,number_of_bands_si = readCSV('silicon_bulk\Si_bulk.bs.set-1.csv')
#    
#fermi_energy_value= FERMI_ENERGY_SI
#figure_filename = 'silicon_bulk\plots/BS_MOF2_G_X_U.png'
#paths = PATHS_SI
##Number of K-Points
#N_O_K = 100
#plotBands(energies_si,number_of_bands_si, fermi_energy_value, figure_filename, paths,N_O_K)
##    
#    
#Graphene
k_pointx,k_pointy,k_pointz,energies_graphene,number_of_bands_graphene = readCSV('graphene\graphene.bs.set-1.csv')
    
fermi_energy_value= FERMI_ENERGY_GRAPHENE
figure_filename = 'graphene\plots\graphene_bands.png'
paths = PATHS_GR
#Number of K-Points
N_O_K = 100
plotBands(energies_graphene,number_of_bands_graphene, fermi_energy_value, figure_filename, paths,N_O_K)

#CsPbBr3
#k_pointx,k_pointy,k_pointz,energies_graphene,number_of_bands_perovskite = readCSV('CsPbBr3\CsPbBr3.bs.set-1.csv')
#
#fermi_energy_value= FERMI_ENERGY_CsPbBr3
#figure_filename = 'CsPbBr3\plots\CsPbBr3_literature_3.png'
#paths = PATHS_CsPbBr3
##Number of K-Points
#N_O_K = 50
#plotBands(energies_graphene,number_of_bands_perovskite, fermi_energy_value, figure_filename, paths,N_O_K)


#MAPbBr3
#k_pointx,k_pointy,k_pointz,energies_graphene,number_of_bands_perovskite = readCSV('MAPbBr3\Orthorhombic_MAPbBr3_1\MAPbBr3.bs.set-1.csv')
#
#fermi_energy_value= FERMI_ENERGY_MAPbBr3
#figure_filename = 'MAPbBr3\plots\MAPbBr3_literature_5.png'
#paths = PATHS_MAPbBr3
##Number of K-Points
#N_O_K = 50
#plotBands(energies_graphene,number_of_bands_perovskite, fermi_energy_value, figure_filename, paths,N_O_K)



