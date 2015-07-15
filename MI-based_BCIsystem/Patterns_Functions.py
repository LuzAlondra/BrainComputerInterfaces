### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### January 18th, 2012

# ************************************
# *       BIOSIGNAL PROCESSING       *
# * 'Feature Extractors & Selectors' *
# ************************************


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
from __future__ import division
import copy
import numpy as np
import scipy as sp
import svmutil as libsvm
from IIR_Filters import filtfilt



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATIONS

# ------------ F1. BAND POWER CALCULATION ------------------
def BandPower(extractor,signal,band,filtering,reference,samples_segment,noverlap_segment,signal_len):
    'Band Power according Absolute, Relative & Reference values'
    
    signal_power = np.zeros(0)
    # (1) Signal Filtering
    # --- highpass filter
    filtered_tempo = filtfilt(band[1][0], band[1][1], signal)
    # --- lowpass filter
    filtered_tempo = filtfilt(band[2][0], band[2][1], filtered_tempo)
    # (2) Signal Power
    power = filtered_tempo**2
    # (3) Reference Signal Calculation for Relative Values
    if extractor == 'relative':
        ref_tempo = filtfilt(filtering[10][1][0], filtering[10][1][1], signal)
        ref_tempo = filtfilt(filtering[10][2][0], filtering[10][2][1], ref_tempo)
        ref_power = ref_tempo**2
    # (4) ERD/ERS Power 
    if extractor == 'ERD/ERS': power = power - reference
    # (5) Signal Segmentation & Powering
    # --- time window initialization 
    start, end = 0, samples_segment 
    while end <= signal_len:                                                           
        #  A- absolute power or ERDS
        power_point = np.average(power[start:end])
        #  B- relative power
        if extractor == 'relative':
            ref_point = np.average(ref_power[start:end])
            power_point = power_point/ref_point            
        #  C- segment power into signal power
        #row = np.append(row, np.log10(power_point))
        signal_power = np.append(signal_power, power_point)
        #  D- time window update
        start += noverlap_segment
        end   += noverlap_segment
    return signal_power
    

# ------------------- F2. DBI METHOD -----------------------
def DBI_Method(eeg_classes):
    'DBI Method'
    
    DBIlocs = np.zeros(0)
    # (1) Standard Deviation and Mean per class
    # --- StdDev_Mean = [[std_matrix1, mean_matrix1],...,[std_matrixN, mean_matrixN]] 
    StdDev_Mean = []
    for item in eeg_classes:
        tempo = []
        tempo.append(np.std(item, axis = 0))
        tempo.append(np.mean(item, axis = 0))
        StdDev_Mean.append(tempo)
    # (2) Ri terms (Ri x features)
    NumFea = np.size(eeg_classes[0], axis=1)
    current, Ri = 0, np.zeros((1, NumFea))
    for std_i, mean_i in StdDev_Mean:
        operators, Rij = copy.copy(StdDev_Mean), np.zeros((1, NumFea))
        # --- removing the current cluster
        operators.pop(current)
        current += 1
        # --- Rij terms (Rij x features)
        #     (comparing the current cluster with the rest of clusters)
        for std_j, mean_j in operators:
            rij = (std_i + std_j)/np.abs(mean_i - mean_j) 
            rij = np.reshape(rij, (1, NumFea))
            Rij = np.append(Rij, rij, axis = 0)
        # --- maximum values across the Rij terms
        ri = np.max(Rij[1:,:], axis = 0)
        ri = np.reshape(ri, (1, NumFea))
        Ri = np.append(Ri, ri, axis = 0)      
    # (3) DBI organization
    # --- the first term must be ignored owing to the zero row created by default
    DBIarray = np.mean(Ri[1:,:], axis = 0)
    DBItempo = np.mean(Ri[1:,:], axis = 0)
    maximo   = np.max(DBIarray)
    DBIarray.sort()
    # --- sorting the values in ascending order according to their location 
    for item in DBItempo:
        index = np.where(DBItempo == np.nanmin(DBItempo))
    # --- saving data
        DBIlocs = np.append(DBIlocs, index[0][0])
    # --- removing the tested item by NaN
        DBItempo[index[0][0]] = None
    return DBIlocs, DBIarray
