#%%
import numpy as np 
import pandas as pd 
import soundfile as sf 
import librosa 
import matplotlib.pyplot as plt 
import os
import glob
import ast



def join(*args):
    return os.path.join(*args)

def load_taps_into_list(df):
    return df.apply(lambda x: ast.literal_eval(x) if pd.notna(x) else np.nan)


#%%
# read in the participant tap data 
files = os.listdir('./tap-data/')
df = pd.read_csv(join('./tap-data/', files[0]))

#%%
# here are all the columns in the df
for col in df.columns:
    print(col)

#%% to get taps as array 

#%% get a single tap entry from the df
#block1 taps are in ['block1_taps.rt']
block1taps = df['block1_taps.rt'].dropna() # drop all NaNs from df 
# there is this weird thing where the taps are stored as strings in the csv file, so you have to do this literal_eval thing to get them back as lists
block1taps = block1taps.apply(lambda x: ast.literal_eval(x) if pd.notna(x) else np.nan)
block1taps_entry = block1taps.iloc[0] # now you can get the tap entries by index if you want 





#%%
# get list of all the stimuli 

allstims = [os.path.basename(fi) for fi in list(set(df['sndfile'].dropna()))]
allstims = sorted(allstims, key=lambda x: int(x.split('_')[2]))

# all no-timbre (nt) stims
nt_stims = [stim for stim in allstims if '_t_' not in stim]
nt_stims = sorted(nt_stims, key=lambda x: int(x.split('_')[2]))


strong_stims = [stim for stim in allstims if stim.startswith('s')]
medium_stims = [stim for stim in allstims if stim.startswith('m')]
weak_stims = [stim for stim in allstims if stim.startswith('w')] 
none_stims = [stim for stim in allstims if stim.startswith('n')] 

#%%
stim = 'strong_n_72_1.wav'

df[df.version == 119.0]



