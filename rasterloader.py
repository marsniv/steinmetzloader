import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import h5py
from functions import *

#select where the data is (should be the NAS)
rootdir = '/Users/mli853/Documents/NWB/steinmetz2019/allData'
#select where you want your numpy files stored
outputdir = '/Users/mli853/Documents/NWB/Github/testsave'
#select brain area 
brainarea = "VISp"
#select bin size
binsize = 0.01

#loop through every folders brain areas
sessions = []
saves = []
indices = []
for path, subdirs, files in os.walk(rootdir):
    for file in files:
        #check all of the brainlocation files to see if requested brain area is there
        if "channels.brainLocation.tsv" in file:
            location = pd.read_csv(str(os.path.join(path, file)), sep='\t')  
            unique_values = location['allen_ontology'].unique()
            if brainarea in unique_values:
                #if requested brain area is in that list, then select indices of those neurons
                tosave = np.array(location.index[location.allen_ontology == brainarea])
                indices.append(tosave)
                saves.append(str(os.path.join(path)))
                sessions.append(str(os.path.basename(path)))
print(str(len(saves))+" sessions identified")

#go through sessions with the good brain area and save necessary stuff for making np arrays
spiketimes = []
spikes = []
annotations = []
for save in saves:
    spiketimefile = str(save)+"/spikes.times.npy"
    spiketimes.append(np.load(spiketimefile))
    spikesfile = str(save)+"/spikes.clusters.npy"
    spikes.append(np.load(spikesfile))
    annotationfile = str(save)+"/clusters._phy_annotation.npy"
    annotations.append(np.load(annotationfile))

#save np arrays of those neuron spike timings 
for i in range(len(spikes)):
    #currently, i pmatize every neuron spiking instead of just the ones from the relevant 
    #brain area. fix in future! 
    events = eventize(spikes[i], spiketimes[i], annotations[i], indices[i])
    pmat = pmatize(spiketimes[i], binsize, events)
    #LAST STEP remove low quality neuron ids 
    #pmat = annotatize(pmat, annotations[i], indices[i])
    np.save(str(outputdir)+"/"+str(sessions[i])+"_"+str(brainarea)+".npy", pmat)
    print("session " +str(i+1)+"/"+str(len(spikes))+" extracted")
print("doneso!")