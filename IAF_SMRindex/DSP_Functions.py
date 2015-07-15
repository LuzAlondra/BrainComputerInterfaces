### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### January 18th, 2012

# ************************************
# *       BIOSIGNAL PROCESSING       *
# *   'Digital Signal Processing'    *
# ************************************


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
from __future__ import division
import copy
import numpy as np
import random as rd
import scipy as sp


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL VARIABLES
# ---- 64 electrodes matrix according to BioSemi Layout ----
layout = np.array([[ 0,  0,  0,  1, 33, 34,  0,  0,  0],
                   [ 2,  0,  3,  0, 37,  0, 36,  0, 35],
                   [ 7,  6,  5,  4, 38, 39, 40, 41, 42],
                   [ 8,  9, 10, 11, 47, 46, 45, 44, 43],
                   [15, 14, 13, 12, 48, 49, 50, 51, 52],
                   [16, 17, 18, 19, 32, 56, 55, 54, 53],
                   [23, 22, 21, 20, 31, 57, 58, 59, 60],
                   [25,  0, 26,  0, 30,  0, 63,  0, 62],
                   [ 0,  0,  0, 27, 29, 64,  0,  0,  0]], dtype = int)



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATIONS


# -------- F1. Conversion from 24bits to Float Format ------
def bits_float(BYTES):
    d0 = np.frombuffer(BYTES[0::3], dtype='u1').astype(float)
    d1 = np.frombuffer(BYTES[1::3], dtype='u1').astype(float)
    d2 = np.frombuffer(BYTES[2::3], dtype='i1').astype(float)
    d0 += 256 * d1
    d0 += 65536 * d2
    return d0


# ---------------- F2. IIR FILTER DESIGN -------------------
def spectral_filter(Fs, fL, fH, order, sort):
    
    # 1- Wn calculation
    if sort == 'lowpass':
        wn = (fH*2)/Fs
    elif sort == 'highpass':
        # --- ultra low frequency rejection
        if fL < 2:
            wn = (fL*2)/Fs
            a  = (np.sqrt(3) - 2*np.sin(np.pi * wn))/(np.sin(np.pi * wn) + np.sqrt(3)*np.cos(np.pi * wn))
            B = np.array([1, -1])
            A = np.array([1, -a])
            return (B, A)
        # --- rejection of 2Hz or larger frequencies
        else:
            wn = (fL*2)/Fs            
    elif sort == 'bandpass':        
        wn = [(fL*2)/Fs, (fH*2)/Fs]
    elif sort == 'bandstop':
        wn = [(fL*2)/Fs, (fH*2)/Fs]
    # 2- B/A calculation
    (B, A) = sp.signal.iirfilter(order, wn, btype = sort, analog = 0, ftype = 'butter', output = 'BA')
    return (B, A)


# ------------- F3. Bad Electrode Rejection ---------------- 
def replace_refIDX(Ref_CHs, selected_chs, num_ch):
    'Remove the bad electrodes and ignore them in the referencing process,\
     (via original scalp location denomination)'
     
    if type(Ref_CHs) == list: Ref_CHs = np.array(Ref_CHs, dtype = int)
    selected_chs = np.array(selected_chs)
    in_array = np.setmember1d(Ref_CHs, selected_chs)
    in_array = np.where(in_array == False)
    if in_array[0].tolist() == []: 
        all_chs  = np.arange(num_ch, dtype = int)
        in_array = np.setmember1d(all_chs, selected_chs)
        in_array = np.where(in_array == False)
        Ref_CHs  = all_chs[in_array[0]]
    else:
        Ref_CHs = Ref_CHs[in_array[0]]
    return Ref_CHs


# ----------- F4. Bad Electrode Replacement --------------- 
def replace_electrodes(electrode_loc, selected_chs, new_layout, ch_pos):
    
    # 1- electrode location according to Biosemi denomination
    electrode_loc += 1
    (i, j) = np.where(new_layout == (electrode_loc))
    replace_chs = np.zeros(0, dtype = int)        
    if i-1 > 0: replace_chs = np.append(replace_chs, layout[i-1,j])
    if j-1 > 0: replace_chs = np.append(replace_chs, layout[i,j-1])
    if i+1 < 9: replace_chs = np.append(replace_chs, layout[i+1,j])
    if j+1 < 9: replace_chs = np.append(replace_chs, layout[i,j+1])
    if i  != 0 and j !=  0: replace_chs = np.append(replace_chs, layout[i-1,j-1])
    if i+1 < 9 and j !=  0: replace_chs = np.append(replace_chs, layout[i+1,j-1])
    if i+1 < 9 and j+1 < 9: replace_chs = np.append(replace_chs, layout[i+1,j+1])
    if i  != 0 and j+1 < 9: replace_chs = np.append(replace_chs, layout[i-1,j+1])  
    tempo_idx = np.nonzero(replace_chs)
    replace_chs  = replace_chs[tempo_idx[0]]
    # 2- re-assignment for python processing
    replace_chs -= 1
    # 3- checking if the selected channels does not encompass bad electrodes
    selected_chs = np.array(selected_chs)
    in_array = np.setmember1d(replace_chs, selected_chs)
    in_array = np.where(in_array == False)
    replace_chs  = replace_chs[in_array[0]]
    # 4- returning only till four components
    if len(replace_chs) >= 4: replace_chs = replace_chs[:4]
    # 5- updating the new label of the channels
    tempo = np.setmember1d(np.array(ch_pos), replace_chs)
    replace_chs = np.where(tempo == True)
    replace_chs = replace_chs[0]
    return replace_chs


# ---------------- F5. Signal Conditioning -----------------
def SiGCoN(ch,eeg_data,new_layout,reference,bandwidth,bandrejection,DCband,downsample_rate,mode,bad_chs):
    'reference     = [Ref_Type, ch_neg]\
     bandwidth     = [BW,   (Bhp,Ahp),(Blp,Alp)]\
     bandrejection = [Rej50,(B,A)]\
     DCband        = [DCremove, (B,A)]'
    
    num_channels= np.size(eeg_data, axis = 0)
    # ------------------------------------------------------
    if mode == 'spectral':
        # ***** Offline Processing *****
        if eeg_data.ndim == 3:
            num_trials  = np.size(eeg_data, axis = 1)
            for tr in range(num_trials):
                # (a) Spectral Filtering
                # --- DC removal 
                if DCband[0] == 'on':
                    eeg_data[ch,tr,:] = eeg_data[ch,tr,:] - np.mean(eeg_data[ch,tr,:])
                # --- Bandpass filter performance
                if bandwidth[0] == 'on': 
                    # highpass filtering
                    eeg_data[ch,tr,:] = sp.signal.filtfilt(bandwidth[1][0], bandwidth[1][1], eeg_data[ch,tr,:])
                    # lowpass filtering
                    eeg_data[ch,tr,:] = sp.signal.filtfilt(bandwidth[2][0], bandwidth[2][1], eeg_data[ch,tr,:])
                # --- Bandstop filter performance
                if bandrejection[0] == 'on': 
                    eeg_data[ch,tr,:] = sp.signal.filtfilt(bandrejection[1][0],bandrejection[1][1], eeg_data[ch,tr,:])
            return eeg_data[ch,:,:]
        # ***** Online Processing *****
        else:
            # (a) Spectral Filtering
            # --- DC removal 
            if DCband[0] == 'on':
                eeg_data[ch,:] = eeg_data[ch,:] - np.mean(eeg_data[ch,:])
            # --- Bandpass filter performance
            if bandwidth[0] == 'on': 
                # highpass filtering
                eeg_data[ch,:] = sp.signal.filtfilt(bandwidth[1][0],bandwidth[1][1], eeg_data[ch,:])
                # lowpass filtering
                eeg_data[ch,:] = sp.signal.filtfilt(bandwidth[2][0],bandwidth[2][1], eeg_data[ch,:])
            # --- Bandstop filter performance
            if bandrejection[0] == 'on': 
                eeg_data[ch,:] = sp.signal.filtfilt(bandrejection[1][0],bandrejection[1][1], eeg_data[ch,:])
            return eeg_data[ch,:]
    # ------------------------------------------------------        
    if mode == 'spatial':
        # (b) DownSampling (previous requirements)
        # ***** Offline Processing *****
        if eeg_data.ndim == 3:
            num_trials  = np.size(eeg_data, axis = 1)
            num_samples = np.size(eeg_data, axis = 2)//downsample_rate
            dsp_ch = np.zeros((1,num_trials,num_samples))
        # **** Online Processing *****
        else:
            num_samples = np.size(eeg_data, axis = 1)//downsample_rate
            dsp_ch = np.zeros((1,num_samples))
        # (c) Spatial Filtering (previous requirements)       
        # --- monopolar referencing
        if reference[0] == 'Monopolar':           
            ref_idx = replace_refIDX(reference[1], bad_chs, num_channels)
        # --- bipolar referencing
        elif reference[0] == 'Bipolar':
            ref_idx = replace_refIDX(reference[1], bad_chs, num_channels)
        # --- common average referencing
        elif reference[0] == 'CAR':
            ref_idx = replace_refIDX(range(num_channels), bad_chs, num_channels)
        # --- laplacian referencing
        else:           
            (i, j) = np.where(new_layout == (ch+1))
            ref_ch = np.zeros(0, dtype = int)   
            # small laplacian referencing
            if reference[0] == 'SmallLaplacian':  
                if i != 0:  ref_ch = np.append(ref_ch, new_layout[i-1,j])
                if j != 0:  ref_ch = np.append(ref_ch, new_layout[i,j-1])
                if j+1 < 9: ref_ch = np.append(ref_ch, new_layout[i,j+1])
                if i+1 < 9: ref_ch = np.append(ref_ch, new_layout[i+1,j])
            # large laplacian referencing
            elif reference[0] == 'LargeLaplacian':                 
                if i-1 > 0: ref_ch = np.append(ref_ch, new_layout[i-2,j])
                if j-1 > 0: ref_ch = np.append(ref_ch, new_layout[i,j-2])
                if j+2 < 9: ref_ch = np.append(ref_ch, new_layout[i,j+2])
                if i+2 < 9: ref_ch = np.append(ref_ch, new_layout[i+2,j])   
            # remove the zero values & re-assign the channel values (for python processing)
            ref_idx = np.nonzero(ref_ch)
            if ref_idx[0].tolist() != []: 
                ref_ch = ref_ch[ref_idx[0]]
                ref_ch -= 1            
            else:
                ref_ch = np.zeros(0, dtype = int)   
            ref_idx = replace_refIDX(ref_ch, bad_chs, num_channels)
        # (d) Execution of steps b and c
        # ***** Offline Processing *****
        if eeg_data.ndim == 3:            
            for tr in range(num_trials): 
                eeg_tempo = eeg_data[ch,tr,:] - np.mean(eeg_data[ref_idx,tr,:], axis = 0)
                dsp_ch[0,tr,:] = eeg_tempo[0::downsample_rate]  
        # ***** Online Processing *****    
        else:
            eeg_tempo = eeg_data[ch,:] - np.mean(eeg_data[ref_idx,:], axis = 0)
            dsp_ch[0,:] = eeg_tempo[0::downsample_rate]    
        return dsp_ch


# ------------- F6. ERD/ERS Maps ~ PreProcessing -----------
def ERDS_PreProcessing(eeg_data, eeg_samples, eeg_trials, bandpass_filtering, channels):
    'ERD/ERS Maps Preprocessing'
    
    # (a) Local Variables Declaration    
    # --  number of bands
    numbands = 0
    for item in bandpass_filtering:
        if item[0] == 'on': numbands += 1
    # --  returning matrix
    Power_ERDS = []
    # (b) Time Course of ERD/ERS  
    for idx in range(len(eeg_data)):  
        # -- number of samples 
        Samples = eeg_samples[idx]
        Power_ERDS.append(np.zeros((len(channels),numbands,len(Samples))))
        # -- number of trials
        Trials = eeg_trials[idx]
        # -- processing for one specific band
        index_band = -1
        for Band in bandpass_filtering:
            if Band[0]  == 'on': 
                # -- number of current selected bands
                index_band += 1
                for index_ch in range(len(channels)):               
                    # -- current bandpass filtering of all trial for the selected channel
                    filtered_trials = np.zeros((len(Trials),len(Samples)))                                                        
                    for index_tr in Trials: 
                        # signal extraction
                        signal = eeg_data[idx][channels[index_ch], index_tr, Samples]
                        # highpass filtering
                        signal = sp.signal.filtfilt(Band[1][0], Band[1][1], signal)
                        # lowpass filtering
                        filtered_trials[index_tr,:] = sp.signal.filtfilt(Band[2][0], Band[2][1], signal) 
                    # -- average calculation over all band-pass filtered trials
                    mean_trial = np.mean(filtered_trials, axis = 0) 
                    mean_trial = np.reshape(mean_trial, (1,len(mean_trial)))
                    mean_trial = np.repeat(mean_trial, len(Trials), axis = 0)
                    # -- substraction of the mean of the data for each sample to avoid that
                    #    the evoked potentials may mask induced activities
                    filtered_trials = filtered_trials - mean_trial
                    # -- squaring of the amplitude samples to obtain power samples
                    filtered_trials = filtered_trials**2
                    # -- averaging of power samples for all trials
                    filtered_trials = np.median(filtered_trials, axis = 0)   
                    # -- data storage
                    Power_ERDS[idx][index_ch, index_band, :] = filtered_trials.copy()        
    return Power_ERDS


# ------ F7. Reference Calculation for ERD/ERS POWER ------
def ERDSPower_REF(eeg_ref, bandpass_filtering):
    'Reference Calculation for ERD/ERS Power'
    
    # ***** Offline Processing *****
    if type(eeg_ref) == list:
        # (a) Dimension of the eeg_ref matrix
        Reference, dimX, dimY, = [], [], []
        for idx in range(len(eeg_ref)):
            dimX.append(np.size(eeg_ref[idx], axis = 0))
            dimY.append(np.size(eeg_ref[idx], axis = 1))
        # (b) Feature Extraction
        row = np.zeros(0)    
        for idx in range(len(eeg_ref)):                
            for tr in range(dimY[idx]):                        
                for ch in range(dimX[idx]):
                    for band in bandpass_filtering:                            
                        if band[0] == 'on':
                            # -- highpass filtering
                            tempo = sp.signal.filtfilt(band[1][0], band[1][1], eeg_ref[idx][ch, tr, :])
                            # -- lowpass filtering + band power 
                            tempo = sp.signal.filtfilt(band[2][0], band[2][1], tempo)
                            row = np.append(row, np.mean(tempo**2))          
                # -- matrix creation according to the number of features
                if tr == 0: 
                    Reference.append(np.zeros((1, len(row))))
                    Reference[idx][0, :] = row.copy()
                else:
                    row = np.reshape(row, (1, len(row)))
                    Reference[idx] = np.append(Reference[idx], row.copy(), axis = 0)                    
                # -- row reset                  
                row = np.zeros(0)  
        return Reference
    # ***** Online Processing *****
    else:
        # (a) Dimension of the eeg_ref matrix
        dimX = np.size(eeg_ref, axis = 0)
        # (b) Feature Extraction
        row = np.zeros(0)                             
        for ch in range(dimX):
            for band in bandpass_filtering:                            
                if band[0] == 'on':
                    # -- highpass filtering
                    tempo = sp.signal.filtfilt(band[1][0], band[1][1], eeg_ref[ch, :])
                    # -- lowpass filtering + band power 
                    tempo = sp.signal.filtfilt(band[2][0], band[2][1], tempo)
                    row = np.append(row, np.mean(tempo**2))          
        return row


# ------------------- F8. Window Library --------------------
def WinLibrary(choice, segment):
    'Digital Window Selection'

    if   choice == 'Bartlett':
        WindoW = sp.signal.bartlett(segment)
    elif choice == 'Blackman':
        WindoW = sp.signal.blackman(segment)
    elif choice == 'Boxcar':
        WindoW = sp.signal.boxcar(segment)
    elif choice == 'FlatTop':
        WindoW = sp.signal.flattop(segment)
    elif choice == 'Gaussian':
        WindoW = sp.signal.gaussian(segment)
    elif choice == 'Hamming':
        WindoW = sp.signal.hamming(segment)
    elif choice == 'Triangular':
        WindoW = sp.signal.triang(segment)
    elif choice == 'Hanning':
        WindoW = sp.signal.hanning(segment)
    return WindoW
