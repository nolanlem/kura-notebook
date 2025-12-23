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

#%%

# Directory containing the .npy files
npy_dir = './stimuli_3/' # checking stimuli_2 now

# Get all .npy files in the directory
npy_files = glob.glob(os.path.join(npy_dir, '*.npy'))

# Count of renamed files
renamed_count = 0

# Process each file
for file_path in npy_files:
    file_name = os.path.basename(file_path)
    
    # Skip files that already have '_n_' in their name
    if '_n_' in file_name:
        continue
    
    # Create the new file name by adding '_n_'
    # Example: 'medium_92_2.npy' -> 'medium_n_92_2.npy'
    parts = file_name.split('_')
    if len(parts) >= 3:  # Make sure we have enough parts
        new_file_name = f"{parts[0]}_n_{parts[1]}_{parts[2]}"
        
        # Construct the full new file path
        new_file_path = os.path.join(npy_dir, new_file_name)
        
        # Rename the file
        os.rename(file_path, new_file_path)
        renamed_count += 1
        print(f"Renamed: {file_name} -> {new_file_name}")

print(f"Renamed {renamed_count} .npy files in the root './stimuli_2/' directory.")

# If no files were renamed, it might be because they already have the '_n_' pattern
if renamed_count == 0:
    print("No .npy files without '_n_' pattern were found in the root directory.")
    print("Files might already be in the desired format.")
#%%
# Function to rename files in a directory with a specific extension
def rename_files_with_extension(directory, extension, recursive=False):
    renamed_count = 0
    
    # Get all files with the specified extension
    if recursive:
        files = glob.glob(os.path.join(directory, '**', f'*.{extension}'), recursive=True)
    else:
        files = glob.glob(os.path.join(directory, f'*.{extension}'))
    
    for file_path in files:
        # Skip files in the root of ./stimuli_2/phases/ if extension is .npy and recursive is True
        if recursive and extension == 'npy' and os.path.dirname(file_path) == os.path.abspath('./stimuli_2/phases'):
            continue
            
        file_name = os.path.basename(file_path)
        
        # Skip files that already have '_n_' in their name
        if '_n_' in file_name:
            continue
        
        # Create the new file name by adding '_n_'
        parts = file_name.split('_')
        if len(parts) >= 3:  # Make sure we have enough parts
            new_file_name = f"{parts[0]}_n_{parts[1]}_{parts[2]}"
            
            # Construct the full new file path
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
            
            # Rename the file
            os.rename(file_path, new_file_path)
            renamed_count += 1
            print(f"Renamed: {file_path} -> {new_file_path}")
    
    return renamed_count

# Rename .wav files in ./stimuli_2/
wav_count = rename_files_with_extension('./stimuli_2', 'wav')
print(f"Renamed {wav_count} .wav files in './stimuli_2/'")

# Rename .txt files in all subdirectories of ./stimuli_2/
txt_count = rename_files_with_extension('./stimuli_2', 'txt', recursive=True)
print(f"Renamed {txt_count} .txt files in subdirectories of './stimuli_2/'")

# Rename .npy files in all subdirectories of ./stimuli_2/ (except those directly in ./stimuli_2/phases/)
npy_count = rename_files_with_extension('./stimuli_2', 'npy', recursive=True)
print(f"Renamed {npy_count} .npy files in subdirectories of './stimuli_2/' (excluding files directly in './stimuli_2/phases/')")

total_count = wav_count + txt_count + npy_count
print(f"Total files renamed: {total_count}")

if total_count == 0:
    print("No files were renamed. They might already be in the desired format.")
#%% sanity check: stimulus, beat windows, and onsets are all correct 
os.chdir('/Users/nolanlem/Desktop/kura-notebook/')
# plot the stimulus waveform and the onsets from the onsets datafile corresponding to that stimulus
dir1 = './stimuli_3/' # this one in the git dir 
dir2 = './stimuli_4/'
stim1 = 'medium_n_81_3' 
stim2 = 'medium_n_81_4'
#stim1_ = 'strong_81_3'
#stim1 = reformat_stim_name(stim1_) # NB: if using old naming conventions, but i changed them all 
stimwf1 = join(dir1, stim1 + '.wav')
stimwf2 = join(dir2, stim2 + '.wav')
# load the wfs
y1, sr1 = librosa.load(stimwf1)
y2, sr2 = librosa.load(stimwf2)
y1 = y1[:sr1*4] # take only 4 seconds for better visual inspections
y2 = y2[:sr2*4]

# which stim, stimuli_1, or stimuli_2 to check?
stim = stim1 # which one to inspect?

if stim == stim1: 
    y = y1
    stim = stim1
    dir = dir1 
else: 
    y = y2
    stim = stim2 
    dir = dir2

fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
ax[0].plot(y) # plot the wf of the stimulus
ax[0].set_title(f'stim waveform {stim}') # title of the plot
########################################################
# get the beat-windows and plot them 
bwfile = join(dir, 'phases', 'beat-windows', stim + '.txt')
bws = np.loadtxt(bwfile) # bws are in sample units already
bws = bws[bws < len(y)] # take only the portion that corresponds to the stimulus (we originally craeted longer versions and then cut them down but param datafiles have data the entire generation file)
ax[0].vlines(bws, -1, 1, color='r')
########################################################
# get the center bpm and check that it is approx the same as the average bpm of the beat-windows boundaries 
# NB: initial center bpm was calcuated from the entirety of the param data files, not the first 15 beats... 
# (this is how we calculated the center bpm)
center_bpm = join(dir, 'phases', 'center-bpm', stim + '.txt')
bpm = np.loadtxt(center_bpm) # in bpm 
bpm_calculated_from_bws = 60./np.diff(librosa.samples_to_time(bws)).mean()
print(f'stimulus bpm: {bpm} \t calculated bpm: {bpm_calculated_from_bws}')
########################################################
# get the onsets
stimdata = join(dir, 'phases', 'onsets', stim + '.npy')
onsets = np.load(stimdata, allow_pickle=True)

# sanity check, plot the onsets with wf 
num_osc_to_plot = 50
for osc_onsets in onsets[:num_osc_to_plot]:
    #osc_onsets_samples = librosa.time_to_samples(osc_onsets) # don't need this because onsets in this data file are already in samples
    osc_onsets = np.array(osc_onsets)
    osc_onsets = librosa.time_to_samples(osc_onsets)
    osc_onsets_samples = osc_onsets[osc_onsets < len(y2)] # portion that corresponds to first 15 beats
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
dir1 = '/Users/nolanlem/Documents/kura/kura-git/swarm-tapping-study/stim-no-timbre-5/stimuli_2'

dir2 = '/Users/nolanlem/Desktop/tap-data-ccrma/Experiment-2/stimuli/' # this is one locally


# example stimulus name 
stim1 = 'strong_n_72_2' # test v.2
#stim1 = 'medium_81_1'
#stim2 = reformat_stim_name(stim2) # different naming convention which makes things confusing 
# get the stimname to open the .wav file assoc w it
stimname1 = join(dir2, stim1 + '.wav')
# load stim wfs
y1, sr1 = librosa.load(stimname1)
y1 = y1[:sr1*4]
fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
#check waveforms are same
ax[0].plot(y1)
ax[0].set_title(f'stim waveform {stim1}')
# add axis and plot y2
#ax[1].plot(y2)
#ax[1].set_title(f'stim waveform {stim2}')

# check stim data
stimdata = '/Users/nolanlem/Desktop/tap-data-ccrma/Experiment-2/stim-data/' + stim1 + '.npy'
onsets = np.load(stimdata, allow_pickle=True)

# add axis to current plt
# sanity check 
for i,osc_onsets in enumerate(onsets[:20]):
    osc_onsets_samples = librosa.time_to_samples(osc_onsets)
    osc_onsets_samples = osc_onsets_samples[osc_onsets_samples < len(y1)] # need to just take portion that corresponds to first 15 beats
    ax[1].vlines(osc_onsets_samples, -1, 1, color='r', linewidth=0.2)

ax[1].set_title('selected onsets ')

#%%

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

# Code to rename .wav files in stimuli_2 directory by adding '_n_' to filenames
import os

# Directory containing the .wav files
wav_dir = './stimuli_2/'

# List all files in the directory
files = os.listdir(wav_dir)

# Count of renamed files
renamed_count = 0

# Loop through all files
for file in files:
    if file.endswith('.wav') and '_n_' not in file:
        # Construct the full file path
        old_file_path = os.path.join(wav_dir, file)
        
        # Create the new file name by adding '_n_'
        # Example: 'medium_92_2.wav' -> 'medium_n_92_2.wav'
        parts = file.split('_')
        if len(parts) >= 3:  # Make sure we have enough parts (e.g., 'medium_92_2.wav')
            new_file_name = f"{parts[0]}_n_{parts[1]}_{parts[2]}"
            
            # Construct the full new file path
            new_file_path = os.path.join(wav_dir, new_file_name)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            renamed_count += 1
            print(f"Renamed: {file} -> {new_file_name}")

print(f"Renamed {renamed_count} files.")

# If no files were renamed, it might be because they already have the '_n_' pattern
if renamed_count == 0:
    print("No files without '_n_' pattern were found in the stimuli_2 directory.")
    print("Files in stimuli_2 might already be in the desired format.")