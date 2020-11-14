# simulation-scripts
Collection of scripts used for analysing simulation data

Two python scripts for plotting data returned by cp2k k points simulation, and one .bs to csv file script. 

plot_bands_vera_updated.py shall take the .bs file and the .out file as a commandline input. Then return the band structure plot for this data. It requires the user to have a newly used .bs file (.bs files tend to append data if your cp2k script is ran twice). If this is not done, you will get errors surrounding "not same number of xaxis values and y axis values".

plot_bands_am.py relies on the data inputted to be in csv format, which is achieved with cp2k_bs2csv.py. cp2k_bs2csv.py takes .bs file as input in the commandline, and converts it to csv. Then using this csv as an input for plot_bands_am.py will create a bandstructure plot. But this requires new data manually entered into the plot_bands_am.py script depending on the simulated structure. 
