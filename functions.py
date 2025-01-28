import numpy as np

#select correct events
def eventize(areas,channels,brainarea, annotations, spikes, spiketimes):
    #select the indices of the 1122 channels with the correct brain area 
    brainareaindices= np.where(areas == str(brainarea))
    #select the clusters that were identified in those channels
    clusters = np.where(channels==brainareaindices[0])
    #select the indices of those neuron ids 
    neurons = clusters[0]
    listofevents = []
    for i in range(0, int(np.max(neurons))):
        if i not in neurons:
            continue
        if annotations[i] < 2:
            continue
        #select all spike times where that neuron id fired
        condition = (spikes[:]==i)
        #select the range of times when neuron is active
        listofevents.append(spiketimes[condition])
    events = np.array(listofevents, dtype=object)
    return events

def pmatize(events, bin_size):
    #select length of recording sessions
    maxtime = np.max([np.max(arr) for arr in events])
    time_window = [0, int(np.max(maxtime))]  # Time window in seconds
    pmat = []
    for i in range(len(events)):
        spike_train, _ = np.histogram(events[i], bins=np.arange(time_window[0], time_window[1] + bin_size, bin_size))
        spike_train = np.where(spike_train > 0, 1, spike_train)
        pmat.append(spike_train)
    return pmat 
