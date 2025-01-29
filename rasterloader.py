import os
import numpy as np
import pandas as pd
from functions import *

#select where the data is (should be the NAS)
rootdir = '/Users/mli853/Documents/NWB/steinmetz2019/allData'
#select where you want your numpy files stored
outputdir = '/Users/mli853/Documents/NWB/steinmetz2019/testsave'
#select brain area 
brainarea = "BLA"
#select bin size (seconds)
binsize = 0.01
#only include session with over 100 neurons

#loop through every folders brain areas
sessions = []
saves = []
areas = []
for path, subdirs, files in os.walk(rootdir):
    for file in files:
        #check all of the brainlocation files to see if requested brain area is there
        if "channels.brainLocation.tsv" in file:
            #turn tsv file into pandas
            location = pd.read_csv(str(os.path.join(path, file)), sep='\t') 
            #select all brain areas in the session
            unique_values = location['allen_ontology'].unique()
            #if requested brain area is among the recorded locations 
            if brainarea in unique_values:
                #see how many neurons from that brain area where recorded 
                area = location['allen_ontology'].to_numpy()
                brainareaindices= np.where(area == str(brainarea))
                channel = np.load(str(str(os.path.join(path)))+"/clusters.peakChannel.npy")
                clusters = np.where(channel==brainareaindices[0])
                #if greater than or equal to 128, save those sessions
                if len(clusters[0]) >= 128:
                    areas.append(area)
                    saves.append(str(os.path.join(path)))
                    sessions.append(str(os.path.basename(path)))
print("relevant sessions identified")

#go through sessions with the good brain area and save necessary stuff for making np arrays
spiketimes = []
spikes = []
annotations = []
channels=[]
for save in saves:
    spiketimefile = str(save)+"/spikes.times.npy"
    spiketimes.append(np.load(spiketimefile))
    spikesfile = str(save)+"/spikes.clusters.npy"
    spikes.append(np.load(spikesfile))
    annotationfile = str(save)+"/clusters._phy_annotation.npy"
    annotations.append(np.load(annotationfile))
    nchannelfile = str(save)+"/clusters.peakChannel.npy"
    channels.append(np.load(nchannelfile))
print('data compiled')
#save np arrays of those neuron spike timings 


#save np arrays of those neuron spike timings 
for i in range(len(spikes)):
    #sort out the events
    events = eventize(areas[i],channels[i],brainarea,annotations[i],spikes[i],spiketimes[i])
    #discard smaller sessions
    if len(events) < 128:
        continue
    #turn into raster
    pmat = pmatize(events, binsize)
    #get numer of neurons
    numneu = len(events)
    #save numpy file
    np.save(str(outputdir)+"/"+str(brainarea)+"_"+str(numneu)+"neurons.npy", pmat)
    print("file created")
print("doneso!")
