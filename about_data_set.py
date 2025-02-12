#%%
import numpy as np 
import pandas as pd 
import soundfile as sf 
import librosa 
import matplotlib.pyplot as plt 
import os
import glob
#import seaborn as sns 
#sns.set_theme(style='whitegrid')

# some utility functions

def join(*args):
    return os.path.join(*args)

def reformat_stim_name(stimname):
    sp = stimname.split('_')
    return '_'.join([sp[0], 'n', sp[1], sp[2]])

def load_csv_as_list(csvfi):
    df = pd.read_csv(csvfi)
    return df.values.tolist()

def return_idxs(arr):
    return [list(np.where(row == 1)[0]) for row in arr]
#%%

#%% check other dir data
# stim parameter data ('./phases/) consists of the initial conditions that generated the stimulus from the 
# kuramoto coupled oscillator model. 
# -- initial phases of each oscillator [unit: radians] ('./phases/init_phases/*.txt)
# -- initial frequency of each oscillator [radians] ('./phases/init_freqs/*.txt') 
#
# the stim parameter data also contains output data from the beat windowing algorithm we used (see paper)
# This was done only for 'phase coherence analysis', where we look at the phase relationships between taps and onsets over the length of the stimulus 
# -- beat windows [samples] (windows of time in which the taps and oscillator onsets are considered to be in a beat) 
# -- center bpm [bpm] (average tempo of stimulus as calculated from the beat windows)
# --- onset data [seconds] ('./phases/onsets/*.csv') (onsets of each oscillator in the ensemble)
# -- NB: onset data was originally in './phases/' as .npy files but they were huge 
#         they contained trigger onsets as '1' per iteration of the generative model (gen model runs sample by sample) but other
#         sample times were saved as 0s. 
#%%########################################################

# plot the stimulus waveform and the onsets from the onsets datafile corresponding to that stimulus
dir1 = './stimuli_1/' # this one in the git dir 
stim1 = 'strong_n_72_1'
#stim1 = reformat_stim_name(stim1_) # NB: if using old naming conventions, but i changed them all 
stimwf1 = join(dir1, stim1 + '.wav')
y1, sr1 = librosa.load(stimwf1)
y1 = y1[:sr1*4] # take only 4 seconds for better visual inspections

fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
ax[0].plot(y1) # plot the wf of the stimulus
ax[0].set_title(f'stim waveform {stim1}') # title of the plot
########################################################
# get the beat-windows and plot them 
bwfile = join(dir1, 'phases', 'beat-windows', stim1 + '.txt')
bws = np.loadtxt(bwfile) # bws are in sample units already
bws = bws[bws < len(y1)] # take only the portion that corresponds to the stimulus (we originally craeted longer versions and then cut them down but param datafiles have data the entire generation file)
ax[0].vlines(bws, -1, 1, color='r')
########################################################
# get the center bpm and check that it is approx the same as the average bpm of the beat-windows boundaries 
# NB: initial center bpm was calcuated from the entirety of the param data files, not the first 15 beats... 
# (this is how we calculated the center bpm)
center_bpm = join(dir1, 'phases', 'center-bpm', stim1 + '.txt')
bpm = np.loadtxt(center_bpm) # in bpm 
bpm_calculated_from_bws = 60./np.diff(librosa.samples_to_time(bws)).mean()
print(f'stimulus bpm: {bpm} \t calculated bpm: {bpm_calculated_from_bws}')
########################################################
# get the onsets
stimdata = join(dir1, 'phases', 'onsets', stim1 + '.npy')
onsets = np.load(stimdata, allow_pickle=True)

# sanity check, plot the onsets with wf 
num_osc_to_plot = 20
for osc_onsets in onsets[:num_osc_to_plot]:
    #osc_onsets_samples = librosa.time_to_samples(osc_onsets) # don't need this because onsets in this data file are already in samples
    osc_onsets = np.array(osc_onsets)
    osc_onsets = librosa.time_to_samples(osc_onsets)
    osc_onsets_samples = osc_onsets[osc_onsets < len(y1)] # portion that corresponds to first 15 beats
    ax[1].vlines(osc_onsets_samples, -1, 1, color='r', linewidth=0.2)
ax[1].set_title(f'selected onsets of {num_osc_to_plot} oscillators')

## NB: you should see the onsets of each of the 40 oscillators line up with the 
# envelope of the stimulus waveform 

########################################################
########################################################
########################################################
########################################################
########################################################
########################################################


#%%





#%%
dir1 = '/Users/nolanlem/Documents/kura/kura-git/swarm-tapping-study/stim-no-timbre-5/stimuli_1'

dir2 = '/Users/nolanlem/Desktop/tap-data-ccrma/Experiment-2/stimuli/' # this is one locally
# example stimulus name 
stim1 = 'strong_72_1'
#stim1 = 'medium_81_1'
stim2 = reformat_stim_name(stim1) # different naming convention which makes things confusing 
# get the stimname to open the .wav file assoc w it
stimname1 = join(dir1, stim1 + '.wav')
stimname2 = join(dir2, stim2 + '.wav')
# load stim wfs
y1, sr1 = librosa.load(stimname1)
y2, sr2 = librosa.load(stimname2)
y1 = y1[:sr1*4]

fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
#check waveforms are same
ax[0].plot(y1)
ax[0].set_title(f'stim waveform {stim1}')
# add axis and plot y2
#ax[1].plot(y2)
#ax[1].set_title(f'stim waveform {stim2}')

# check stim data
stimdata = '/Users/nolanlem/Desktop/tap-data-ccrma/Experiment-2/stim-data/' + stim2 + '.npy'
onsets = np.load(stimdata, allow_pickle=True)

# add axis to current plt
# sanity check 
for i,osc_onsets in enumerate(onsets[:20]):
    osc_onsets_samples = librosa.time_to_samples(osc_onsets)
    osc_onsets_samples = osc_onsets_samples[osc_onsets_samples < len(y1)] # need to just take portion that corresponds to first 15 beats
    ax[1].vlines(osc_onsets_samples, -1, 1, color='r', linewidth=0.2)

ax[1].set_title('selected onsets ')



# main root dir that holds all the data params files
datadir = join(dir1, 'phases')

onsets = np.load(join(datadir, stim1 + '.npy')) # (40, 7717250), ok these are 


# return the indices for each oscillator in the ensemble of a 2D array where it is 1, otherwise it is 0. 
# this was collected during generation (but wasn't best apporach and generated a large file)
def return_idxs(arr):
    return [list(np.where(row == 1)[0]) for row in arr]

onsets = return_idxs(onsets) # these are already in samples numbers

# recheck the onsets in this datadir

fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
#check waveforms are same
ax[0].plot(y1)
# add axis and plot y2
ax[1].plot(y2)
# check stim data

# add axis to current plt
# sanity check 
for osc_onsets in onsets[:2]:
    #osc_onsets_samples = librosa.time_to_samples(osc_onsets) # don't need this because onsets in this data file are already in samples
    osc_onsets = np.array(osc_onsets)
    osc_onsets_samples = osc_onsets[osc_onsets < len(y1)] # portion that corresponds to first 15 beats
    ax[2].vlines(osc_onsets_samples, -1, 1, color='r', linewidth=0.2)

#%% 
# this code just recreates the onset data in the 'phases' dir as csv files rather than the original giant .npy files 
onsetsdir = join(dir1, 'phases', '*.npy')
onsetsdir = glob.glob(onsetsdir)
new_onsetsdir = join(dir1, 'phases', 'onsets')
            
for i,fi in enumerate(onsetsdir):
    print(f'working on {fi} {i}/{len(onsetsdir)}')
    finame = os.path.basename(fi).split('.')[0] # get basename and remove .npy
    nfiname = reformat_stim_name(finame)
    onsets = np.load(join(datadir, stim1 + '.npy')) # (40, 7717250), ok these are 
    onsets = return_idxs(onsets) # these are already in samples numbers
    df = pd.DataFrame(onsets)
    df.to_csv(join(new_onsetsdir, nfiname + '.csv'), index=False)

#%% 
# sanity check: check that csv files contain onset information, cast to list or lists
df = pd.read_csv('./stimuli_1/phases/onsets/strong_n_72_1.csv')
dflist = df.values.tolist()




#%% so the '/Users/nolanlem/Documents/kura/kura-git/swarm-tapping-study/stim-no-timbre-5/stimuli_1/phases/' (dir1) is good , datadir refers to this

# check beat windows 
bwfile = join(datadir, 'beat-windows', stim1 + '.txt')
bws = np.loadtxt(bwfile) # bws are in sample units already
plt.plot(y1)
plt.gca().vlines(bws, -1, 1, color='r')

#%%
# check center-bpm (center-bpm should be the bpm calculated from the beat windows)
avg_bpm = join(datadir, 'center-bpm', stim1 + '.txt')
bpm = np.loadtxt(avg_bpm) 

bws_in_seconds = librosa.samples_to_time(bws)
beat_window_bpm = 60.0/np.mean(np.diff(bws_in_seconds))
print(f'bpm as calc by beat windows: {beat_window_bpm} \t datafile bpm: {bpm}')

#%% 

#%% #NB: don't need to run
###  change all data file names in phases dir to new naming convention

dirs = ['ang', 'beat-windows', 'center-bpm', 'init_freqs', 'init_phases', 'pc']
# Directory containing the .wav files
dir1 = './stimuli_1/phases/'

dirs = [join(dir1, d_) for d_ in dirs]

# List all files in the directory
files = os.listdir(dir1)

# Loop through all files
for dir_ in dirs:
    files = os.listdir(dir_)
    for file in files:
        if file.endswith('.txt'):
            # Construct the full file path
            old_file_path = os.path.join(dir_, file)
            
            # Create the new file name
            nfiname = reformat_stim_name(file) 
            #print(nfiname)
            
            # Construct the full new file path
            new_file_path = os.path.join(dir_, nfiname)
            print(new_file_path)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)

print("Files renamed successfully.")

#%%
# NB: don't need to run, renamed files 
dir_ = './stimuli_1/trigs'
files = os.listdir(dir_)
for file in files:
    if file.endswith('.npy'):
        # Construct the full file path
        old_file_path = os.path.join(dir_, file)
        
        # Create the new file name
        nfiname = reformat_stim_name(file) 
        #print(nfiname)
        
        # Construct the full new file path
        new_file_path = os.path.join(dir_, nfiname)
        print(new_file_path)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)