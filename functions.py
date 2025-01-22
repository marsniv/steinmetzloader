import numpy as np

#functions
#loop through every neuron id
def eventize(spikes, spiketimes, annotation, indices):
    listofevents = []
    for i in range(1, int(np.max(spikes))):
        if annotation[i] >= 2 and i in indices:
            pass
        else:
            continue 
        #select all spike times where that neuron id fired
        condition = (spikes[:]==i)
        #select the range of times when neuron is active
        listofevents.append(spiketimes[condition])
    events = np.array(listofevents, dtype=object)
    return events

def pmatize(spiketimes, bin_size, events):
    time_window = [0, int(np.max(spiketimes))]  # Time window in seconds
    time_vector = np.arange(time_window[0], time_window[1], bin_size)
    pmat = []
    for i in range(len(events)):
        spike_train, _ = np.histogram(events[i], bins=np.arange(time_window[0], time_window[1] + bin_size, bin_size))
        spike_train = np.where(spike_train > 0, 1, spike_train)
        pmat.append(spike_train)
    return pmat    

    good = np.array(good, dtype=object)
    array = [array[j] for j in range(len(array)) if good[j]]
    return array
