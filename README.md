# kura-notebook
kuratap notebook 

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
