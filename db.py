# open medium_n_105_2.npy 
#%%
import numpy as np 
import matplotlib.pyplot as plt 
import os
#%%
data = np.load('medium_n_105_2.npy', allow_pickle=True)
# data.shape = (40,)  (array of lists)
# and each osc in the 40 is a list of the zero crossings in sec

#%%

# open medium_n_105_2.npy 
#
os.chdir('/Users/nolanlem/Desktop/kura-notebook/stimuli_2/')

data = np.load('phases/onsets/medium_n_105_2.npy', allow_pickle=True)


#%%

os.chdir('/Users/nolanlem/Desktop/kura-notebook/stimuli_3/')

data = np.load('phases/onsets/medium_n_105_3.npy', allow_pickle=True)

sr = 22050.

#%%
new_onsets_dir = 'new_onsets'
os.makedirs(new_onsets_dir, exist_ok=True)

# go through all the .npy files in ./phases/onsets/*.npy and divide all of the values by sr and save the new 2D array as a .npy file in a dir called 'new_onsets' in the current directory

sr = 22050. 

os.chdir('/Users/nolanlem/Desktop/kura-notebook/stimuli_4/')

for file in os.listdir('./phases/onsets_old/'):
    print(f'working on {file}')
    if file.endswith('.npy'):
        print(f'working on {file}')
        data = np.load(f'./phases/onsets_old/{file}', allow_pickle=True)
        zc_array = []
        for zc in data:
            zc = np.asarray(zc, dtype=int)
            zc = zc/sr
            zc_array.append(list(zc))
        obj = np.array(zc_array, dtype=object)
        np.save(f'./phases/onsets/{file}', obj, allow_pickle=True)
#%%




#%%

# for all of the .npy files in ./phases/onsets/*.npy, for each row in the data, find the index of where the elem == 1 and append that idx to a list for each row and then save the 2D list as a .npy file in a dir called 'new_onsets'

new_onsets_dir = 'new_onsets'
os.makedirs(new_onsets_dir, exist_ok=True)

#%%
#%%
sr = 44100.
# loop through each of the rows in data and find where the elem == 1 and append that idx to a list for each row 
idxs_2d = []
for row in data:
    idxs = []
    for i, elem in enumerate(row):
        if elem == 1:
            idxs.append(i/sr)
    idxs_2d.append(idxs)
#print(indices)



#%%