# Kura notebooks


# Stimulus Parameter Data

Stimulus parameter data (for stimuli v.1 as an example) is in ('./stimuli_1/phases/) and consists of the initial parameter configurations (initial phase, initial frequencies) that generated the stimulus from the Kuramoto coupled oscillator model. 

ex.
 - initial phases of each oscillator [unit: radians] ('./phases/init_phases/*.txt)
 - initial frequency of each oscillator [radians] ('./phases/init_freqs/*.txt') 

Also in ./stimuli_1/phases/ are the parameters from the beat-binning analysis that generated the beat-windows we used to segment to stimuli in order to perform phase coherence analysis. 


 - beat windows [samples] (windows of time in which the taps and oscillator onsets are considered to be in a beat) 
- center bpm [bpm] (average tempo of stimulus as calculated from the beat windows)
- onset data [seconds] ('./phases/onsets/*.csv') (onsets "triggers" (every time the instantaneous Phase of an oscillator in the ensemble would cross zero))
- NB: onset data was originally in './phases/' as .npy files but they were huge and so I moved them into another director that I'm not tracking on the git repo but let me know if you want the   giant files that have the instantaneous phases of each oscillator in the ensemble during generation. 

# Jupyter Notebooks 
Look at at about_data_set.py and about_tap_data.py to see how the above applies. I have some notes documenting for example how to plot the oscillator onsets with the beat windows with the stimulus waveform. 

# also NB: 
I changed the file naming conventions throughout all of the parameter files to be consistent so it should be easier in this repo.  