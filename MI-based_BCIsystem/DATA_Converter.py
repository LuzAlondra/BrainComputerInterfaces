### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### January 18th, 2012

# *********************************************
# *           GUI-DATA INTERPRETER            *
# * 'Conversion from string to useful values' *
# *********************************************


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
from __future__ import division
import numpy as np


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATIONS

#..............FUNCTION |1|: DAQ_output check-up............
def daq_error(daq_output):
    'DAQ_output last revision'
    
    # A. OFFLINE MENU
    if daq_output[0] == 'offline':
        # (1) Incomplete information in offline daq_menu verification
        tempo =[]
        for item in daq_output[1:]: tempo.append(item == '')
        if any(tempo):
            m1 = '--> The Data Acquisition menu is incomplete.'
            e1 = True
            return m1, e1, daq_output
        # (2) Information translation
        else:
            # -- range -> used electrodes
            daq_output[2:4] = range_selection(daq_output[2:4])
            if daq_output[10] == '0':
                daq_output[10]= []
            else:
                daq_output[10] = range_selection(daq_output[10])
            # -- combined range -> samples, training trials, testing trials
            for idx in range(4,7):
                if daq_output[idx].find(';') != -1:
                    daq_output[idx] = range_selection(daq_output[idx].split(';'))
                else:
                    tempo = range_selection(daq_output[idx])
                    daq_output[idx] = []
                    for i in range(len(daq_output[1])): daq_output[idx].append(tempo)
            # -- integers -> sample rate and overlapping
            daq_output[7] = int(daq_output[7])    
            daq_output[9] = int(daq_output[9]) 
            # -- floats -> time window           
            if daq_output[8].find(';') != -1:
                tempo = daq_output[8].split(';')
                daq_output[8] = []
                for item in tempo: daq_output[8].append(float(item))
            else:
                tempo = daq_output[8]
                daq_output[8] = []
                for idx in range(len(daq_output[1])): daq_output[8].append(float(tempo))
            m1, e1 = '', False
            return m1, e1, daq_output
            
    # B. ONLINE MENU
    else:
        # (1) Incomplete information in online daq_menu verification
        tempo = []            
        for item in daq_output[1:]: tempo.append(item == '')
        if any(tempo):
            m1 = '--> The Data Acquisition menu is incomplete.'
            e1 = True
            return m1, e1, daq_output
        # (2) Information translation
        else:
            ## -- integers -> TCP bytes, sample rate
            daq_output[2] = int(daq_output[2])
            daq_output[5] = int(daq_output[5])
            ## -- integers -> samples for controlling & referencing
            daq_output[8] = int(daq_output[8])
            daq_output[9] = int(daq_output[9])
            ## -- range -> cap & external electrodes
            daq_output[3] = range_selection(daq_output[3])
            daq_output[4] = range_selection(daq_output[4])
            ## -- float -> segmentation in seconds & overlap rate
            daq_output[6] = float(daq_output[6])   
            daq_output[7] = float(daq_output[7])             
            m1, e1 = '', False
            return m1, e1, daq_output                  


#............FUNCTION |2|: sigcon_output check-up...........
def sigcon_error(sigcon_output):
    'SigCon_output revision'
    
    # (1) Incomplete information
    tempo = []
    check = [sigcon_output[0],sigcon_output[1][0],sigcon_output[1][1],sigcon_output[2],sigcon_output[3],sigcon_output[4],sigcon_output[5][0],sigcon_output[5][1]]
    for item in check: tempo.append(item == '')
    if any(tempo):
        m2 = '--> The Signal Conditioning menu is incomplete.'
        e2 = True
        return m2, e2, sigcon_output
    # (2) Information translation
    else:
        ##-- integers -> downsampling frequency 
        sigcon_output[0] = int(sigcon_output[0])
        ##-- lists -> positive and negative channels
        sigcon_output[2] = range_selection(sigcon_output[2])
        if sigcon_output[1][0] == 'Monopolar':
            tempo = range_selection(sigcon_output[1][1])
            sigcon_output[1][1] = []
            sigcon_output[1][1].append(tempo.pop(0))
            if tempo != []: sigcon_output[1][1].append(tempo.pop(0))                                
        elif sigcon_output[1][0] == 'Bipolar':
            sigcon_output[1][1] = range_selection(sigcon_output[1][1])
        ##-- floats -> bandwidth
        if sigcon_output[5][0] == 'on':
            sigcon_output[5][1] = limiting_values(sigcon_output[5][1])
        m2, e2 = '', False
        return m2, e2, sigcon_output
    

#...........FUNCTION |3|: feaext_output check-up............
def feaext_error(feaext_output):
    'FeaExt_output revision'
          
    # (1) Incomplete information in ERD/ERS BP 
    if all([feaext_output[0] == 'ERD/ERS', feaext_output[1] == '']):
        m3 = '--> There is no reference to ERD/ERS.'
        e3 = True
        return m3, e3, feaext_output
    # (2) Incomplete information in Band Power Selection
    tempoA, tempoB = [], []
    check = [feaext_output[2][0], feaext_output[2][1],feaext_output[3][0],feaext_output[3][1],feaext_output[4][0], feaext_output[4][1],\
             feaext_output[5][0], feaext_output[5][1],feaext_output[6][0],feaext_output[6][1],feaext_output[7][0], feaext_output[7][1],\
             feaext_output[8][0], feaext_output[8][1],feaext_output[9][0],feaext_output[9][1],feaext_output[10][0],feaext_output[10][1],\
             feaext_output[11][0],feaext_output[11][1]]
    for item in check: tempoA.append(item == '')
    for item in check: tempoB.append(item == 'off')
    if any(tempoA):
        m3 = '--> The feature extraction menu is incomplete.'
        e3 = True
        return m3, e3, feaext_output            
    elif all(tempoB):
        m3 = '--> None bandpower has been selected.'
        e3 = True
        return m3, e3, feaext_output
    # (3) Information translation
    else:
        # -- reference for ERD/ERS power
        if feaext_output[1] != 'off':
            feaext_output[1] = range_selection(feaext_output[1])
        else:
            feaext_output[1] = 0
        # -- selected bands
        for idx in range(2,12):
            if feaext_output[idx][0] == 'on': feaext_output[idx][1] = limiting_values(feaext_output[idx][1])                 
        m3, e3, = '', False
        return m3, e3, feaext_output


#...........FUNCTION |4|: feasel_output check-up............
def feasel_error(feasel_output):
    'FeaSel_output revision'
          
    # (1) Incomplete information in N-Features 
    if any([all([feasel_output[2][0] == 'on', feasel_output[2][1] == '']),\
            all([feasel_output[3][0] == 'on', feasel_output[3][1] == ''])]):
        m4 = '--> There is no range of features.'
        e4 = True
        return m4, e4, feasel_output
    # (2) Information translation
    else:
        # -- DBI
        if feasel_output[0] == 'on':
            feasel_output[0] = True
        else:
            feasel_output[0] = False
        # -- RFE
        if feasel_output[1][0] == 'on':
            feasel_output[1][0] = True
        else:
            feasel_output[1][0] = False
        # -- N-Features for DBI
        if feasel_output[2][0] == 'on':
            feasel_output[2][0] = True
            feasel_output[2][1] = range_selection(feasel_output[2][1])
        else:
            feasel_output[2][0] = False  
        # -- N-Features for RFE (combined ranges)
        if feasel_output[3][0] == 'on':
            feasel_output[3][0] = True                
            if feasel_output[3][1].find(';') != -1:
                feasel_output[3][1] = range_selection(feasel_output[3][1].split(';'))
            else:
                tempo = range_selection(feasel_output[3][1])
                feasel_output[3][1] = []
                # copy & paste for 2 classifiers
                for i in range(2): feasel_output[3][1].append(tempo)                
        else:
            feasel_output[3][0] = False
        m4, e4, = '', False          
        return m4, e4, feasel_output                            


#............FUNCTION |5|: class_output check-up............
def class_error(class_output, daq_output):
    'Class_output revision'
          
    # (1) Incomplete information in class_menu verification
    tempo =[]
    for item in class_output[:2]: tempo.append(item == '')
    if daq_output[0] == 'online': tempo.append(class_output[2] == '')
    if any(tempo):
        m5, e5 = '--> The classifier menu is incomplete.', True
        return m5, e5, class_output
    else:
    # (2) Complete classifier menu
        class_output[1] = range_selection(class_output[1])
        for idx in range(len(class_output[1])): class_output[1][idx] += 1
        if daq_output[0] == 'online':             
            class_output[2] = range_selection(class_output[2])
            class_output[2] = np.array(class_output[2]) + 1           
        if class_output[3] == 'on':
            class_output[3] = True
        else:
            class_output[3] = False
        m5, e5, = '', False
        return m5, e5, class_output


#............FUNCTION |6|: plots_output check-up............
def plots_error(plots_output, daq_output):
    'Plots_output revision'

    # (1) Online Plotting (no available configuration)
    if daq_output[0] == 'online':
        if plots_output[6] == 'on':
            plots_output[6] = True
        else:
            plots_output[6] = False
        m, e = '', False  
        return m, e, plots_output
    
    # (2) Offline Plotting
    elif all([any([plots_output[0]=='on',plots_output[1]=='on',plots_output[2]=='on',plots_output[3]=='on',plots_output[4]=='on',plots_output[5]=='on']), daq_output[0] == 'offline']):
        # Spectrogram or PDS: ON
        if any([plots_output[0] == 'on', plots_output[1] == 'on']):
            tempo =[]
            for item in plots_output[7][5:7]: tempo.append(item == '')
            if any(tempo):
                ## -- missing information
                m1 = '--> The window type and/or overlapping\n      entries have not been completed.'
                e1 = True
            else:
                ## -- integers -> overlapping
                plots_output[7][6] = int(plots_output[7][6])                    
                m1, e1 = '', False
        else:
            m1, e1 = '', False
        # Spectrogram + PSD + ERDS Plots: ON
        tempoA = []
        for idx in [0,1,4,5]: tempoA.append(plots_output[idx] == 'on') 
        if any(tempoA):                
            if  plots_output[7][4] == '':
                ## -- missing information
                m2 = '--> The time window entry has not been completed.'
                e2 = True
            else:                     
                ## -- float --> timewin                                           
                plots_output[7][4] = float(plots_output[7][4])                                                       
                m2, e2 = '', False
        else:
            m2, e2 = '', False
        # Spectrogram + PSD + ERDS Plots: ON
        tempoA = []
        for idx in [0,1,4,5]: tempoA.append(plots_output[idx] == 'on') 
        if any(tempoA):                
            if  plots_output[7][3] == '':
                ## -- missing information
                m3 = '--> The samples entries have not been completed.'
                e3 = True
            else:                     
                ## -- combined lists --> samples                                            
                if plots_output[7][3].find(';') != -1:
                    plots_output[7][3] = range_selection(plots_output[7][3].split(';'))
                else:
                    tempo = range_selection(plots_output[7][3])
                    plots_output[7][3] = []
                    for i in range(len(daq_output[1])): plots_output[7][3].append(tempo)                                                       
                m3, e3 = '', False
        else:
            m3, e3 = '', False
        # Spectrogram + PSD + Box + Histo + ERDS Plots: ON
        tempoA = []
        for idx in [0,1,4,5]: tempoA.append(plots_output[idx] == 'on') 
        if any(tempoA):
            tempoB =[]
            for idx in [0,2]: tempoB.append(plots_output[7][idx] == '')
            if  any(tempoB):
                ## -- missing information
                m4 = '--> The brain states/trials entries have not been completed.'
                e4 = True
            else: 
                ## -- list --> brain states
                plots_output[7][0] = range_selection(plots_output[7][0])
                m5, e5 = '', False
                ## -- combined lists --> trials                  
                if plots_output[7][2].find(';') != -1:
                    plots_output[7][2] = range_selection(plots_output[7][2].split(';'))
                else:
                    tempo = range_selection(plots_output[7][2])
                    plots_output[7][2] = []
                    for i in range(len(daq_output[1])): plots_output[7][2].append(tempo)                                                       
                m4, e4 = '', False
        else:
            m4, e4 = '', False              
        # PDS or Histogram: ON
        tempo = []
        for idx in [1,3]: tempo.append(plots_output[idx] == 'on') 
        if any(tempo):            
            if plots_output[7][7] == '':
                ## -- missing information
                m5 = '--> The overlapping brain state entry has not been completed.'
                e5 = True
            else:                             
                m5, e5 = '', False
        else:
            m5, e5 = '', False
        # Spectrogram, PDS, or ERD/ERS maps: ON
        tempo = []
        for idx in [0,1,4,5]: tempo.append(plots_output[idx] == 'on') 
        if any(tempo):            
            if plots_output[7][1] == '':
                ## -- missing information
                m6 = '--> The channel entry has not been completed.'
                e6 = True
            else:
                ## -- list -> channels
                plots_output[7][1] = range_selection(plots_output[7][1])     
                m6, e6 = '', False
        else:
            m6, e6 = '', False            
        # ERD/ERS maps: ON
        tempo = []
        for idx in [4,5]: tempo.append(plots_output[idx] == 'on') 
        if any(tempo):            
            if plots_output[7][9] == '':
                ## -- missing information
                m7 = '--> The matrix index entry has not been completed.'
                e7 = True
            else:
                ## -- list -> channels
                plots_output[7][9] = range_selection(plots_output[7][9])     
                m7, e7 = '', False
        else:
            m7, e7 = '', False            
        # PDS
        if plots_output[1] == 'on':            
            if plots_output[7][8] == '':
                ## -- missing information
                m8 = '--> The overlapping channel entry has not been completed.'
                e8 = True
            else:
                if plots_output[7][8] == 'y':
                    plots_output[7][8] = True
                else:
                    plots_output[7][8] = False                        
                m8, e8 = '', False
        else:
            m8, e8 = '', False   
        # Message Union for Offline Menu                  
        m = ''
        for item in [m1, m2, m3, m4, m5, m6, m7, m8]: 
            if item != '': m = m + item + '\n'
        e = e1 or e2 or e3 or e4 or e5 or e6 or e7 or e8
        return m, e, plots_output
       
    # (3) Mismatch between daq and sigcon menus
    else: 
        m = '--> The DAQ and plot menus have different type of BCI system.'
        e = True
        return m, e, plots_output             


#..............FUNCTION |7|: range selection................
def range_selection(data):
    'Ranges interpretation'

    i = 0
    if type(data) == str: data = [data]
    for item in data:
        output = []
        if item.find(',') != -1:
            ## a. strings with commas
            ranges = item.split(',')
            for subitem in ranges:
                if subitem.find(':') == -1:
                    output.append(int(subitem)-1)
                else:
                    subranges = subitem.split(':')
                    if len(subranges) == 2:
                        output.extend(range(int(subranges[0])-1,int(subranges[1])))
                    else:
                        output.extend(range(int(subranges[0])-1,int(subranges[2]),int(subranges[1])))
        elif item.find(':') != -1:
            ## b. strings only with colon
            ranges = item.split(':')
            if len(ranges) == 2:
                output.extend(range(int(ranges[0])-1,int(ranges[1])))
            else:
                output.extend(range(int(ranges[0])-1,int(ranges[2]),int(ranges[1])))
        else:
            ## c. strings only with numbers
            output.append(int(item)-1)
        data[i] = output
        i += 1
    if len(data) == 1: data = data[0]
    return data


#............. FUNCTION |8|: limiting values ...............
def limiting_values(data):
    'Limiting values interpretation'

    data = data.replace(' ', '')
    LIST = data.split(':')
    if type(data) == type(LIST): LIST = data.split(',')
    d0 = float(LIST[0])
    if len(LIST) == 1:
        d1 = 0.0
    else:
        d1 = float(LIST[1])
    return [d0, d1]


#...... FUNCTION |9|: Replacement of the miBCI gui .........
def BCI_load(daq, sigcon, feaext, feasel, classs, plots):
    'Loading BCI-system configuration instead of using the BCI_gui()\
     (only applicable for free-running miBCI versions)'

    # (1) Conversion of Variables
    m1, e1, daq_output = daq_error(daq)
    m2, e2, sigcon_output = sigcon_error(sigcon)       
    m3, e3, feaext_output = feaext_error(feaext)
    m4, e4, feasel_output = feasel_error(feasel)
    m5, e5, class_output  = class_error(classs, daq_output)
    tempo = []
    for item in plots[:7]: tempo.append(item == 'off')
    if all(tempo):
        plots_output = plots
        m6, e6 = '', False
    else:
        m6, e6, plots_output  = plots_error(plots, daq_output)    
    error = any([e1, e2, e3, e4, e5, e6])
    # (2) Stopping the program owing to missing information
    if error:
        m7 = '\n\t\tTHE PROGRAM CANNOT START\n'
        m = ['\n', m1, m2, m3, m4, m5, m6, m7]
        m = '\n'.join(m)
        print m
    # (3) Saving the final results as a list (BCI_OUTPUT)
    else:
        print '\n\t\tTHE PROGRAM IS INITIALIZING THE ANALYSIS\n'
        output = [daq_output,sigcon_output,feaext_output,feasel_output,class_output,plots_output]
    return output

