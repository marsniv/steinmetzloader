import os
import numpy as np
import pandas as pd
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
    #the cluster ids and their spike times
    spiketimefile = str(save)+"/spikes.times.npy"
    spiketimes.append(np.load(spiketimefile))
    spikesfile = str(save)+"/spikes.clusters.npy"
    spikes.append(np.load(spikesfile))
    #the annotation for good quality neurons (see Steinmetz' github)
    annotationfile = str(save)+"/clusters._phy_annotation.npy"
    annotations.append(np.load(annotationfile))

#save np arrays of those neuron spike timings 
for i in range(len(spikes)):
    #sort events and trim ones we are interested in 
    events = eventize(spikes[i], spiketimes[i], annotations[i], indices[i])
    #turn into a numpy array with timebins as columns and neurons as rows
    pmat = pmatize(spiketimes[i], binsize, events)
    #collect number of neurons per session
    numneu = len(events)
    np.save(str(outputdir)+"/"+str(brainarea)+"_"+str(numneu)+"neurons_"+str(sessions[i])+".npy", pmat)
    print("session " +str(i+1)+"/"+str(len(spikes))+" extracted")
print("doneso!")
