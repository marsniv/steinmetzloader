# steinmetzloader

Hello! 
I have written this code so people in my lab can load in data from Steinmetz et al., 2019 (https://doi.org/10.1038/s41586-019-1787-x). 
It outputs numpy files with rows as neurons and columns as time bins with 0s and 1s for spikes and silence. It will create a new numpy file for every recording session.

## preparing the data
If you are in the MaTRIX Laboratory, the data is already loaded on the CEDAR (thanks Keith!)
If you are not in the MaTRIX Laboratory, load the data from here (https://figshare.com/articles/dataset/Dataset_from_Steinmetz_et_al_2019/9598406) and make sure you have extracted all the TAR files. 

## functions.py
This includes some relevant functions

## rasterloader.py
The way this code is set up is through command line (sorry not sorry). 
Set `rootdir` to wherever the allData folder from Steinmetz was saved. This code will comb through that folder and extract relevant sessions.
Set `outputdir` to where you want the numpy files of the spikes to be loaded. 
Set `brainarea` to your desired brain area. 
You can change binsize if you want, or leave it at 10ms.

## running
After all these changes are done, go to terminal and make sure you are in the right location. Then simply run:
`python rasterloader.py`

Done! 

If you are interested in further adjusting the code to suit your needs, consult this:
https://github.com/nsteinme/steinmetz-et-al-2019/wiki/data-files


