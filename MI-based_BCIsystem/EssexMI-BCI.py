# -*- coding: utf-8 -*-
## UNIVERSITY OF ESSEX
## School of Computer Science and Electronic Engineering
## PROJECT:
## A Virtual Environment Platform for Simulated BCI-Enabled
## Independent Living
## SUPERVISOR:
## Dr. Francisco Sepulveda
## PhD STUDENT:
## Luz Maria Alonso Valerdi
## DATE:
## March 6th, 2012

## .........................................................
## ........... BRAIN COMPUTER INTERFACE DESIGN .............
## .......... AND SYSTEM CONTROL IMPLEMENTATION ............
## .........................................................


# ==========================================================
# |1| PROGRAM DESCRIPTION
# ==========================================================
# 1.1 BCI graphical user interface to configure the system
# 1.2 OFFLINE signal processing according to:
#     a). Data Acquitision
#     b). Signal Conditioning
#     c). Feature Extraction
#     d). Feature Selection
#     e). Classification
#     f). 2D-Plots (Spectrogram, BoxPlot, Histogram, ERD/ERS maps)
# 1.3 ONLINE signal processing according to:
#     a). Data Acquitision
#     b). Signal Conditioning
#     c). Feature Extraction
#     d). Feature Selection
#     e). Classification
#     f). 2D-Plot (xy) 


# ==========================================================
# |2| MODULES IMPORTING
# ==========================================================
# 2.1 PythonXY modules
from __future__ import division
import pygtk
pygtk.require('2.0')
import copy
import cPickle
import datetime
import gobject
import gtk
import pango
import threading
import time
import copy as cp
import numpy as np
import random as rd
import scipy as sp
from scipy import io, fftpack, signal
from socket import *
import sys
# --- 2D/3D Plot Libraries
import matplotlib
import matplotlib.pyplot as plt
# --- machine learning py
import mlpy 

# 2.2 Available Plug-InS for PythonXY
from IIR_Filters import filtfilt
import svmutil as libsvm

# 2.3 LMAV classes for GUI Construction & Interpretation
from Constructors_gui import Image,Label,Frame,Button_Label,Radio_Button
from DAQ_gui import DAQ_menu
from SigCon_gui import SigCon_menu
from FeaExtSelClass_gui  import FeaExtSelClass_menu
from PlottinG_gui import PlotS_menu
from DATA_Converter import daq_error,sigcon_error,feaext_error,feasel_error,\
                              class_error,plots_error

# 2.4 LMAV fuctions for Digital Signal Processing
from DSP_Functions import spectral_filter,bits_float,replace_refIDX,replace_electrodes,\
                          SiGCoN, ERDS_PreProcessing, ERDSPower_REF, WinLibrary

# 2.5 LMAV functions for Feature Treatment
from Patterns_Functions import DBI_Method,BandPower

# 2.6 LMAV class for Classification Treatments
from CLASSPLOT import Class_Plot

# 2.7 LMAV functions for Experiment2 purposes
from EXP2_Functions import Session1_Tracks, Session23_Tracks, Session23_CueTarget,\
                           Achieved_Targets, Initialization_CueDriven


# ==========================================================
# |3| GLOBAL CONSTANT DECLARATION
# ==========================================================
# ---- Default Directory 
root = 'C:\\Documents and Settings\\lmalon\\Desktop\\'
# ---- BCI gui Output & Online System Stages
bci_output = []
current_stage = ' 1.1 MI-Training'
# ---- gui Constants
ground = '#000000'
tab_bg = '#DCDCDC'
white = '#FFFFFF'
lblue = '#A0AEC1'
blue = '#466289'
orange = '#FA6121'
small_font = 'Georgia 10'
font = 'Trebuchet 14'
large_font = 'Trebuchet 16'
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
#layout_labels =  ['Fp1','AF7','AF3','F1' ,'F3' ,'F5' ,'F7' ,'FT7',
#                  'FC5','FC3','FC1','C1' ,'C3' ,'C5' ,'T7' ,'TP7',
#                  'CP5','CP3','CP1','P1' ,'P3' ,'P5' ,'P7' ,'P9' ,
#                  'PO7','PO3','O1' ,'Iz' ,'Oz' ,'POz','Pz' ,'CPz',
#                  'Fpz','Fp2','AF8','AF4','AFz','Fz' ,'F2' ,'F4' ,
#                  'F6' ,'F8' ,'FT8','FC6','FC4','FC2','FCz','Cz' ,
#                  'C2' ,'C4' ,'C6' ,'T8' ,'TP8','CP6','CP4','CP2',
#                  'P2' ,'P4' ,'P6' ,'P8' ,'P10','PO8','PO4','O2'  ]
# ---- Buffer Size of the TCP-communication (HCI) 
BUFSIZ = 1024
# ---- # @@@@@ Default Stages of Session 1,2,3 @@@@@
default_stages = [['STAGE 1 - Motor Imagery Training','STAGE 2 - Command Training','STAGE 3 - GUI Training'],\
                  ['STAGE 1 - GUI Training', 'STAGE 2 - GUI Testing'],['STAGE 3 - BCI Synchronous Control']]
# --- TCP message to mark the start of a Stage (it includes the trigger code for the BDF-file)
default_TCPmsg = [['10*Tutorial_MI', '20*Tutorial_CMD', '30*Training_GUI'],\
                  [['40*Training_GUI', '50*Testing_GUI'], ['70*Training_GUI', '80*Testing_GUI']],\
                  ['60*Cue-Driven', '90*Target-Driven']]
# ---- XY-Plot Variables
Titles = [['LEFT MI: All the Features', 'LEFT MI: DBI-Features'],\
          ['RIGHT MI: All the Features', 'RIGHT MI: DBI-Features'],\
          ['IDLE State: All the Features', 'IDLE State: DBI-Features']]
# ---- Exp2 Stages
Exp2_Stages = [' 1.1 MI-Training',' 1.2 Command-Training',' 1.3 GUI-Training',\
               ' 2.1 User Training',' 2.2 System Control',' 3.1 User Training',' 3.2 System Control']
# --- Triggers for commands in BCI systems
trig_cmds = {'left':'7*', 'right':'8*', 'idle':'9*'}
# --- Variable to test the Target-Driven System
COMMANDS = ['left', 'right', 'idle']
POINTERS = {'*target1-Doorbell.mp3':[1,1,0,1,2,2,0,1,1,2,0],\
            '*target2-Hello.wav':[1,1,1,1,1,0,1,0,1,1,1,1,1,1,2,2,2,0],\
            '*target3-WaterPouring.mp3':[1,0,1,0,1,1,1,1,1,1,0],\
            '*target4-HandWashing.mp3':[1,1,1,0],\
            '*target5-BaconFrying.mp3':[1,1,1,1,1,2,2,0],\
            '*target6-GoodBye.mp3':[1,1,0,1,1,1,0,2,0,1,1,1,1,2,2,2,2,2,2,0,1,1,1,1,2,2,0,2,2,0],\
            '*target7-Farting.mp3':[1,1,1,1,1,1,1,0,1,0,1,1,1,2,2,0],\
            '*target8-BrushingTeeth.mp3':[1,1,1,1,1,1,2,2,2,0],\
            '*target9-Yawning.wav':[1,1,1,1,1,1,2,2,2,2,2,2,2,0]}
# --- color lines for UniquePlot
color_lines = ['#bc8f8f','#cd5c5c','#8b4513','#cd853f','#deb887','#f4a460','#d2691e','#b22222','#fa8072','#ff8c00','#ff4500','#ff0000']


# ==========================================================
# |4| FUNCTION DECLARATION
# ==========================================================

# ----------- F1. New BioSemi Layout Creation --------------
def BS_layout(channels):
    new_layout = np.zeros((9,9), dtype = int)
    for ch in channels:
        (i, j) = np.where(layout == (ch+1))
        new_layout[i, j] = layout[i, j]
    return new_layout
# ----------------------------------------------------------


# ------------- F2. Active vs Reference Signals ------------
def BSref_Split(eeg_data, ref_indices):
    'Splitting active brain states and referencing signals'
    
    Class_Label = cp.copy(bci_output[4][1])
    eeg_bs, eeg_ref, bsMAT_idxs, refMAT_idxs = [], [], [], []            
    # CASE 1: if there are N active states and N references
    if len(ref_indices) == len(eeg_data)/2:
        for idx in range(len(eeg_data)):
            if idx in ref_indices:
                eeg_ref.append(eeg_data[idx])
                refMAT_idxs.append(idx)
            else:
                eeg_bs.append(eeg_data[idx])
                bsMAT_idxs.append(idx)  
        eeg_data = eeg_bs      
    # CASE 2: if there is only one reference index
    else:
        # --- finding if the given reference index is an brain state too
        ZERO = [x==0 for x in Class_Label]
        if any(ZERO): 
            ZERO_idx = ZERO.index(True)
            Class_Label.pop(ZERO_idx)                
        BS_locs = range(len(Class_Label))
        ZERO = BS_locs.count(ref_indices[0])
        if ZERO == 0: 
            eeg_ref.append(eeg_data.pop(ref_indices[0]))            
            refMAT_idxs.append(ref_indices[0])
            bsMAT_idxs.remove(ref_indices[0])           
        else:
            eeg_ref.append(eeg_data[ref_indices[0]])            
            refMAT_idxs.append(ref_indices[0])            
        # --- completing the reference-indexes with a copy of the unique item
        while len(eeg_ref) != len(eeg_data): 
            eeg_ref.append(eeg_ref[0])
            refMAT_idxs.append(refMAT_idxs[0])           
    return eeg_data, eeg_ref, bsMAT_idxs, refMAT_idxs
# ----------------------------------------------------------



# -------------------- F3. Final Results -------------------
def InitialReport():
    'Analysis Report'

    print ' ___________________________________________________________________________'
    print '|                                                                           |'
    print '|UNIVERSITY OF ESSEX                                                        |'
    print '|School of Computer Science and Electronic Engineering                      |'
    print '|PROJECT:                                                                   |'
    print '|A Virtual Environment Platform for Simulated BCI-Enabled Independent Living|'
    print '|SUPERVISOR:                                                                |'
    print '|Dr. Francisco Sepulveda                                                    |'
    print '|PhD STUDENT:                                                               |'
    print '|Luz Maria Alonso Valerdi                                                   |'
    print ' ___________________________________________________________________________'
    print '\n\n\n'
    print datetime.datetime.today()
    print '\n\n\n'
    print '.............................................................................'
    print '.................... BRAIN COMPUTER INTERFACE DESIGN ........................'
    print '................... AND SYSTEM CONTROL IMPLEMENTATION .......................'
    print '.............................................................................'
    print '\n\n\n'
    print 'The system is being configurated . . .'
# ----------------------------------------------------------
def FinalReport(OFFLineAnalysis):
    'OffLine Analysis Report'

    print '\nO F F L I N E   A N A L Y S I S   R E P O R T\n'
    print '1.- Filename: OFFLineAnalysis.p'
    print '\n'
    print '''2.- Command to open the file: output = cPickle.load(open('filename.p', 'rb'))'''
    print '\n'
    print '3.- Data organization:'
    print '\n'
    print 'OFFLineAnalysis = (eeg_dsp, eeg_feaext, selection_out, selection_labels, class_out)'
    print '\n'
    print 'eeg_dsp         = [mentaltask1, mentaltask2,...]'                     
    print '                   mental task --> channels x trials x samples'
    print 'eeg_feaext      = [mentaltask1, mentaltask2,...]'
    print '                   mental task --> trials x features'
    print 'selection_out   = {''DBI'': array1, ''RFE'': array1, ''DBIvalues'': array2, ''RFEvalues'': array2}'
    print '                   array1 --> indices of selected features, array2 --> values of selected features'
    print 'selection_labels= {''DBI'': list , ''RFE'': list }'
    print '                   list  --> labels of selected features'
    print 'class_output    = {''dataset1'': {''grid_search'':[gs_run1,gs_run2,...],''accuracy'':[acc_run1,acc_run2,...],''predictions'':[pred_vals_run1,pred_vals_run2,...],''dataset_conf'':[step,stop]}...}'
    print '                   grid_search --> best C and gamma parameters per run'
    print '                   accuracy    --> classifier performance per run'
    print '                   predictions --> predicted classifier values per run'
    print '                   [step,stop] --> [number of features per subset, number of features of the final subset]'
    print '\n'
    print '4.- Main Outcomes:'
    print '\n'
    print '==> SigCon_data: ' 
    for item in OFFLineAnalysis[0]: print np.shape(item)
    print '==> FeaExt_data: '
    for item in OFFLineAnalysis[1]: print np.shape(item)
    print '==> DBI_data: ', np.shape(OFFLineAnalysis[2]['DBI'])
    print '==> RFE_data: ', np.shape(OFFLineAnalysis[2]['RFE'])
    print '==> Maximum Classification Accuracy per Dataset: '
    for idx in range(len(OFFLineAnalysis[-1])): print OFFLineAnalysis[-1]['dataset'+str(idx+1)]['BestRun_acc&feas'][0]
# ----------------------------------------------------------


# ==========================================================
# |5| CLASS DECLARATION - BrainComputerInterface
# ==========================================================

# ******************************************************************************
# **************************** 5.1 BCI Interface *******************************
# ******************************************************************************
class BCI_gui():
    'Class to acquire the necessary data for the BCI System'

    #.............Method 5.1.1: Initial Performance.........
    def __init__(self):        
        'Initial method to generate the Essex BCI - GUI'

        # ================interface creation================        
        # (1) WINDOW 
        ## --window creation
        window = gtk.Window()
        window.set_title('The miBCI Software')
        background = gtk.gdk.color_parse(ground)
        window.modify_bg(gtk.STATE_NORMAL, background)
        window.set_border_width(7)
        window.set_resizable(False)
        ## --window events connection
        window.connect('destroy', self.destroy)
        window.show()

        # (2) TABLE: General widget container
        table = gtk.Table(3, 8, False)
        table.show()
        window.add(table)
        
        # (3) NOTEBOOK
        ## --notebook properties
        general_menu = gtk.Notebook()
        general_menu.set_show_border(True)
        general_menu.set_show_tabs(True)
        style = general_menu.get_style().copy()
        style.bg[gtk.STATE_NORMAL] = general_menu.get_colormap().alloc_color(tab_bg)
        general_menu.set_style(style)
        ## --'DAQ_interface' tab insertion
        daq_label = Label(' Data Acquisition ', small_font, 'black', 0.5, 0.5)
        DAQ = DAQ_menu()
        daq_table = DAQ.container()
        general_menu.append_page(daq_table, daq_label)
        ## --'SigCon_interface' tab insertion
        sigcon_label = Label(' Signal Processing ', small_font, 'black', 0.5, 0.5)
        SigCon = SigCon_menu()
        sigcon_table = SigCon.container()
        general_menu.append_page(sigcon_table, sigcon_label)
        ## --'FeaExt_interface' tab insertion
        feaextclass_label = Label(' Feature Extractor, Selector & Classifier ', small_font, 'black', 0.5, 0.5)
        FeaExtSelClass = FeaExtSelClass_menu()
        feaextclass_table = FeaExtSelClass.container()
        general_menu.append_page(feaextclass_table, feaextclass_label)
        ## --'PlotS_interface' tab insertion
        plots_label = Label(' Plots ', small_font, 'black', 0.5, 0.5)
        Plots = PlotS_menu()
        plots_table = Plots.container()
        general_menu.append_page(plots_table, plots_label)
        # --notebook insertion to table
        general_menu.show()
        table.attach(general_menu, 0, 8, 0, 1)

        # (4) BUTTONS: tools to accept or cancel tasks
        ## -- non-useful buttons (only for filling gaps proposes)
        a, b =Button_Label('', 'black', font)
        a.hide()
        table.attach(a, 2, 3, 2, 3)
        a, b =Button_Label('', 'black', font)
        a.hide()
        table.attach(a, 3, 4, 2, 3)
        a, b =Button_Label('', 'black', font)
        a.hide()
        table.attach(a, 4, 5, 2, 3)
        a, b =Button_Label('', 'black', font)
        a.hide()
        table.attach(a, 5, 6, 2, 3)
        ## -- useful buttons
        ok, label = Button_Label('OK', tab_bg, font)
        table.attach(ok, 6, 7, 2, 3)
        ok.connect('clicked', self.Accept)
        cancel, label = Button_Label('Cancel', tab_bg, font)
        table.attach(cancel, 7, 8, 2, 3)
        cancel.connect('clicked', self.Cancel)

        # (5) LABEL: copyright
        label = Label('COPYRIGHT', small_font, 'black', 0, 0.5)
        table.attach(label, 0, 2, 1, 2)
        label = Label('COPYRIGHT\nLuz Ma. Alonso Valerdi  &  Francisco Sepulveda', small_font, tab_bg, 0, 0.5)
        table.attach(label, 0, 2, 2, 3)
        
        # (6) Variable Assignment
        self.DAQ = DAQ
        self.FeaExtSelClass = FeaExtSelClass
        self.Plots = Plots
        self.SigCon = SigCon
        self.window = window        
        
        
    # ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.1.2: Killing GUI ╦╦╦╦╦╦╦╦╦╦╦╦
    def destroy(self, widget, data=None):
        
        gtk.main_quit()
        return False
    

    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.1.3: Accept Buttton ╦╦╦╦╦╦╦╦╦╦╦╦
    def Accept(self, widget):
        'Stopping by missing information or initialization BCI process'

        # (1) Conversion of Tab-Variables
        daq_output = self.DAQ.outcomes()
        print '==> DAQ outcomes:', daq_output
        m1, e1, daq_output = daq_error(daq_output)        
        sigcon_output = self.SigCon.outcomes()
        print '==> SIGCON outcomes:', sigcon_output  
        m2, e2, sigcon_output = sigcon_error(sigcon_output)      
        feaext_output, feasel_output, class_output = self.FeaExtSelClass.outcomes() 
        print '==> FEAEXT outcomes:', feaext_output
        print '==> FEASEL outcomes:', feasel_output
        print '==> CLASS outcomes:', class_output
        m3, e3, feaext_output = feaext_error(feaext_output)        
        m4, e4, feasel_output = feasel_error(feasel_output)        
        m5, e5, class_output  = class_error(class_output, daq_output)        
        plots_output = self.Plots.outcomes()
        print '==> PLOT outcomes:', plots_output
        tempo = []
        for item in plots_output[:7]: tempo.append(item == 'off')
        if all(tempo):
            m6, e6 = '', False
        else:
            m6, e6, plots_output  = plots_error(plots_output, daq_output)   
        error = any([e1, e2, e3, e4, e5, e6])
        # (2) Stopping the program owing to missing information
        if error:
            m7 = '\n\t\tTHE PROGRAM CANNOT START\n'
            m = ['\n', m1, m2, m3, m4, m5, m6, m7]
            m = '\n'.join(m)
            message = Label(m, font, 'black', 0.5, 0.5)
            dialog = gtk.Dialog('One or more errors have been occurred',None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,('OK', True))
            STYLE = dialog.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL] = dialog.get_colormap().alloc_color('#DCDCDC')
            dialog.set_style(STYLE)
            dialog.vbox.pack_start(message)
            dialog.show_all()
            dialog.run()
            dialog.destroy()
            result = False
        # (3) Saving the final results as a list (BCI_OUTPUT)
        else:
            # --- dialog creation            
            dialog = gtk.Dialog('Ready to Start?',None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,('START', True, 'CANCEL', False))
            STYLE = dialog.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL] = dialog.get_colormap().alloc_color('#DCDCDC')
            dialog.set_style(STYLE)           
            # --- starting point for online BCI-system
            if daq_output[0] == 'online':      
                # table design
                table = gtk.Table(10, 2, False)
                table.show()
                dialog.vbox.pack_start(table)  
                # label design
                label = Label('\n 1| USER TUTORIAL', font, 'black', 0, 0.5)
                table.attach(label, 0, 2, 0, 1)
                label = Label('\n 2| CUE-DRIVEN SYSTEM', font, 'black', 0, 0.5)
                table.attach(label, 0, 2, 4, 5)
                label = Label('\n 3| TARGET-DRIVEN SYSTEM', font, 'black', 0, 0.5)
                table.attach(label, 0, 2, 7, 8)
                # radio~button design                  
                buttonA,label = Radio_Button(None, Exp2_Stages[0], font, 'black')
                buttonA.connect("toggled", self.On_Stages, label)                
                table.attach(buttonA, 1, 2, 1, 2)
                locs = [2, 3, 5, 6, 8, 9]
                for item in Exp2_Stages[1:]: 
                    i = locs.pop(0)       
                    buttonB,label = Radio_Button(buttonA, item, font, lblue)
                    buttonB.connect("toggled", self.On_Stages, label)
                    table.attach(buttonB, 1, 2, i, i+1)
                    buttonA = buttonB             
            # --- dialog exection
            dialog.show_all()
            result = dialog.run()
            dialog.destroy()            
        # (4) bci_GUI exit
        self.window.emit('destroy')
        # (5) saving bci_output
        global bci_output
        if result: bci_output = [daq_output,sigcon_output,feaext_output,feasel_output,class_output,plots_output]
        return


    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.1.4: Cancel Buttton ╦╦╦╦╦╦╦╦╦╦╦╦
    def Cancel(self, widget):
        'Callback to quit the main menu'
        
        gtk.main_quit()


    # ╦╦╦╦╦ Method 5.1.5: Starting Point - Online SYS ╦╦╦╦╦╦
    def On_Stages(self, widget, label):
        'Callback to quit the radio buttons of the Online-System'
        
        global current_stage
        if widget.get_active():
            current_stage = label.get_text()
        else:
            label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 
        


# ******************************************************************************
# ************************** 5.2 OnLine BCI System *****************************
# ******************************************************************************
class essexVE_OnLineBCI(threading.Thread):
    'Class to control the ONLINE Brain Computer Interface Module'


    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.1 - Initialization ╦╦╦╦╦╦╦╦╦╦╦
    def __init__(self):
        'USER INTERFACE: required information insertion, \
         PRE-PROCESSING and BCI MODULE STATUS gui'

        # (a) Thread to run the online BCI Module along with a Stopping Mini-GUI
        threading.Thread.__init__(self)        
        # (b) ***** Data Unpacking ***** 
        # --- daq_output
        EEGhost      = bci_output[0][1]
        TCP_array    = bci_output[0][2]
        channels     = bci_output[0][3]
        ext_ch       = bci_output[0][4]
        Fs           = bci_output[0][5] 
        SegLen       = bci_output[0][6]
        overlapping  = bci_output[0][7]
        MI_Samples   = bci_output[0][8]
        RefSamples   = bci_output[0][9]       
        # --- sigcon_output
        Fdown        = bci_output[1][0]
        reference    = bci_output[1][1]    
        ch_pos       = bci_output[1][2]    
        Rej50        = bci_output[1][3]
        DCremove     = bci_output[1][4]
        BW           = bci_output[1][5]
        # --- feaext_output
        FeaExtractor = bci_output[2][0]
        # --- feasel_output
        DBI          = bci_output[3][0]
        sel_DBI      = bci_output[3][2][0]
        # --- class_output
        Classifier   = bci_output[4][0]
        Class_Label  = bci_output[4][1]
        numtr_run    = bci_output[4][2]
        StandardScore= bci_output[4][3]        
        # --- plot_output
        Plot         = bci_output[5][6] 
        # (c) ***** Online System SetUp *****        
        # 1.- Socket Designs (TCP Communication)
        # --- BioSemi connection address
        PORT = 778
        ADDR = (EEGhost, PORT)  
        # --- Exit of the System
        EXIT = False
        # --- number of channels to receive from TCP-Biosemi
        if all([len(ext_ch)==1, ext_ch[0]==0]): 
            TCP_ch = len(channels)
        else:
            TCP_ch = len(channels) + len(ext_ch)
        # --- number of samples to receive from TCP-Biosemi
        TCP_samples = TCP_array//TCP_ch//3
        # --- HCI socket
        Client_HCI = socket(AF_INET, SOCK_STREAM)
        # 2.- Data Acquisition        
        # --- creating the current BioSemi layout
        LAYOUT = BS_layout(channels)         
        # --- number of samples per segment    
        SegSamples = int(round(SegLen * Fdown))
        # --- downsample rate
        downsample_rate = Fs//Fdown
        # --- idle availability
        if Class_Label[-1] != 0:
            Idle_ON = True
            num_BS  = len(Class_Label)
        else:
            Idle_ON = False
            num_BS  = len(Class_Label[:-1])
        # 3.- Previous Digital Signal Processing Designs
        # --- total number of channels in use
        total_chs = cp.copy(channels)
        total_chs.extend(ext_ch)
        # --- re-assignment of the number channel for monopolar referencing
        if reference[0] == 'Monopolar': 
            for idx in range(len(reference[1])): reference[1][idx] = total_chs.index(reference[1][idx])
        # --- highpass and lowpass Butterworth filter for bandwidth
        bandwidth = [BW[0], [0,0], [0,0]]
        if BW[0] == 'on': 
            bandwidth[1][0], bandwidth[1][1] = spectral_filter(Fdown, BW[1][0], 0, 4, 'highpass')   
            bandwidth[2][0], bandwidth[2][1] = spectral_filter(Fdown, 0, BW[1][1], 7, 'lowpass')                    
        # --- lowpass and highpass Butterworth filter for band-rejection
        bandrejection = [Rej50, [0,0]]
        if Rej50 == 'on': 
            bandrejection[1][0], bandrejection[1][1] = spectral_filter(Fdown, 48, 52, 2, 'bandstop')     
        # --- DC removing (high pass filter)
        if DCremove == 'on': 
            DCband = ['on', (np.array([1, -1]), np.array([1, -0.9979]))]
        else:
            DCband = ['off', (0,0)]
        # 4.- Previous Feature Extraction Designs
        # --- whole band coefficients
        whole_fL, whole_fH = [], []
        # --- number of samples per non-overlapping segment
        OverlapSamples = ((100 - overlapping) * SegSamples) // 100        
        # --- bandpass_filtering = [Ltheta, Utheta, Lalpha, Ualpha, Lbeta, Ubeta, gamma]
        bandpass_filtering = [[bci_output[2][2][0], [0,0], [0,0]],\
                              [bci_output[2][3][0], [0,0], [0,0]],\
                              [bci_output[2][4][0], [0,0], [0,0]],\
                              [bci_output[2][5][0], [0,0], [0,0]],\
                              [bci_output[2][6][0], [0,0], [0,0]],\
                              [bci_output[2][7][0], [0,0], [0,0]],\
                              [bci_output[2][8][0], [0,0], [0,0]],\
                              [bci_output[2][9][0], [0,0], [0,0]],\
                              [bci_output[2][10][0],[0,0], [0,0]],\
                              [bci_output[2][11][0],[0,0], [0,0]],\
                              ['off',               [0,0], [0,0]]] #whole band
        for index in range(len(bandpass_filtering)):
            if bandpass_filtering[index][0] == 'on':
                fL = bci_output[2][index+2][1][0]
                fH = bci_output[2][index+2][1][1]
                whole_fL.append(fL)
                whole_fH.append(fH)
                bandpass_filtering[index][1][0], bandpass_filtering[index][1][1] = spectral_filter(Fdown, fL,  0, 7, 'highpass')
                bandpass_filtering[index][2][0], bandpass_filtering[index][2][1] = spectral_filter(Fdown,  0, fH, 7,  'lowpass')                     
        # --- absolute power including broadband and relative power: FILTER
        if any([FeaExtractor == 'relative', FeaExtractor == 'absolute_bb']):
            fL, fH = min(whole_fL), max(whole_fH)
            bandpass_filtering[10][1][0], bandpass_filtering[10][1][1] = spectral_filter(Fdown, fL,  0, 7, 'highpass')
            bandpass_filtering[10][2][0], bandpass_filtering[10][2][1] = spectral_filter(Fdown,  0, fH, 7, 'lowpass')
            if FeaExtractor == 'absolute_bb': bandpass_filtering[10][0] = 'on'   
        # --- referencing signal for ERD/ERS
        eeg_epoch_ref = [False, None]    
        # 5.- Previous Feature Selection Designs    
        # --- selection of the most appropriate features according to the current classification
        FeaChoice = ['class_all', -1]
        # --- models for each feature-choice
        # a-  class_all := all the features across the current run (the last item engages all the runs)
        # b-  class_best:= the best features across the current run (the last item engages all the runs)
        fea_idxs = {'class_all':[], 'class_best':[]}
        Models = {'class_all':[], 'class_best':[]}
        # 6.- Plot Configuration
        if Plot == 'on': 
            Plot = True
        elif Plot == 'off': 
            Plot = False
        # 7.- Sessions of Experiment 2
        cue_labels = ['cue_left', 'cue_right']
        if Idle_ON: cue_labels.append('cue_idle')
        # 8.- Stopping Mini-GUI Design
        # --- window 
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Essex Virtual Environment: Brain Computer Interface')
        background = gtk.gdk.color_parse('#DCDCDC')
        window.modify_bg(gtk.STATE_NORMAL, background)
        window.set_border_width(10)
        window.set_resizable(False)
        window.connect('destroy', self.destroy)
        window.show()
        # --- table
        table = gtk.Table(20, 10, False)
        window.add(table)
        table.show()
        # --- window characteristics
        titulo = Label('University of Essex - BCI Group', 'Neuropol 20', blue, 0, 0.5)
        table.attach(titulo, 0, 8, 0, 1)
        subtitulo = Label('A VE Plataform for Simulated BCI-Enabled Indenpendent Living', 'Neuropol 17', orange, 0, 0.5)
        table.attach(subtitulo, 0, 8, 1, 2)       
        # --- logo and classifier reselector 
        logo = Image('Images\\minilogo.jpg')      
        logo.set_alignment(xalign = 0.85, yalign = 0.5)        
        table.attach(logo, 7, 10, 0, 2)    
        # --- title 1: Online Analysis Report
        logo = Image('Images\\on.png')      
        logo.set_alignment(xalign = 0, yalign = 0.5)    
        table.attach(logo, 0, 2, 2, 4) 
        title = Label('   Online Analysis Report', large_font, 'black', 0, 0.5)
        table.attach(title, 1, 10, 2, 4)               
        message1 = Label('>>> Welcome to Essex MI-Based BCI', font, 'black', 0, 0.5)
        message1.set_size_request(500, 35)
        table.attach(message1, 1, 10, 4, 5)
        message2 = Label('', font, 'black', 0, 0.5)
        message2.set_size_request(500, 35)
        table.attach(message2, 1, 10, 5, 6)
        message3 = Label('', font, 'black', 0, 0.5)
        message3.set_size_request(500, 35)
        table.attach(message3, 1, 10, 6, 7)
        # --- title 2: System Interruption
        logo = Image('Images\\interrupt.png')
        logo.set_alignment(xalign = 0, yalign = 0.5)
        table.attach(logo, 0, 2, 7, 9)
        title = Label('   Interrupt the System Operation by closing Dialog~Boxes', large_font, 'black', 0, 0.5)
        table.attach(title, 1, 10, 7, 9)                 
        # --- title 3: Features Plotting
        logo = Image('Images\\graph.png')
        logo.set_alignment(xalign = 0, yalign = 0.5)
        table.attach(logo, 0, 2, 9, 11)
        title = Label('   2D Plot - BP Estimates Vs Features per Pattern', large_font, 'black', 0, 0.5)
        table.attach(title, 1, 10, 9, 11)    
        # --- classifier reselector
        button, label = Button_Label('Classifier\nSelector', blue, 'Neuropol 11')
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        table.attach(button, 8, 10, 9, 11)
        button.connect('clicked', self.choose_MODEL)
        # (d) ***** Classifiers&Plots - Class Initialization *****
        CLASSp = Class_Plot(bci_output)            
        # (e) ***** Variable Assignment *****
        self.ADDR = ADDR
        self.bandpass_filtering = bandpass_filtering
        self.bandrejection = bandrejection
        self.bandwidth = bandwidth
        self.Classifier = Classifier
        self.CLASSp = CLASSp
        self.Client_HCI = Client_HCI
        self.cue_labels = cue_labels
        self.ch_pos = ch_pos
        self.channels = channels
        self.DBI = DBI
        self.DCband = DCband
        self.downsample_rate = downsample_rate
        self.eeg_epoch_ref = eeg_epoch_ref
        self.EXIT = EXIT
        self.fea_idxs = fea_idxs
        self.FeaChoice = FeaChoice
        self.FeaExtractor = FeaExtractor
        self.Fdown = Fdown
        self.Fs = Fs
        self.Idle_ON = Idle_ON
        self.LAYOUT = LAYOUT
        self.message1 = message1
        self.message2 = message2
        self.message3 = message3
        self.MI_Samples = MI_Samples
        self.Models = Models
        self.numtr_run = numtr_run
        self.num_BS = num_BS
        self.OverlapSamples = OverlapSamples
        self.Plot = Plot
        self.reference = reference
        self.RefSamples = RefSamples
        self.SegSamples = SegSamples
        self.StandardScore = StandardScore
        self.total_chs = total_chs
        self.TCP_array = TCP_array
        self.TCP_ch = TCP_ch
        self.TCP_samples = TCP_samples
        self.window = window
        self.table = table
                
        
    # ╦╦╦╦╦╦╦ Method 5.2.2 - Pathway of Experiment2 ╦╦╦╦╦╦╦╦
    def run(self):
        'Pathway of the Experiment 2'
        
        #     --------------------
        # |1| Variable Declaration
        #     --------------------
        # 1.1 Stage Selection according to the Current Session
        # --- plot image 
        self.prevImage = None
        # --- finding the current stage
        idx_stage, tutorial_stages = Exp2_Stages.index(current_stage), range(3)
        # --- assigning new stage-index
        if tutorial_stages.count(idx_stage) != 0: 
            idx_stage, tutorial_stages = 0, range(idx_stage, 3)   
        else:
            idx_stage -= 2
        # --- full range of stages
        stages_running = range(idx_stage, 5)
        #     ----------------------------
        # |2| Connection to the HCI Server
        #     ----------------------------
        # 2.1 HCI Connection Address
        HCIhost = bci_output[0][10]
        port = 21558
        addr = (HCIhost, port)
        # 2.2 Client Connection
        self.Client_HCI.connect(addr)   
        #     --------------------        
        # |3| Experiment Execution  
        #     --------------------     
        for idx_stage in stages_running:
            if idx_stage == 0:
                self.UserTutorial_S1(tutorial_stages)
                if self.EXIT: break 
            elif idx_stage == 1:
                mean_feaext = self.UserTraining_S23(2,'Cue~Driven System')
                if self.EXIT: break  
            elif idx_stage == 2:
                self.SystemControl_S23(2, 'cue-driven', mean_feaext)
                if self.EXIT: break  
            elif idx_stage == 3:
                mean_feaext = self.UserTraining_S23(3,'Target~Driven System')
                if self.EXIT: break
            elif idx_stage == 4:
                self.SystemControl_S23(3, 'target-driven', mean_feaext)
                if self.EXIT: break
        #     -----------    
        # |4| System Exit
        #     -----------       
        # 4.1 Pause current EEG Recording 
        self.Client_HCI.send('255')
        self.Client_HCI.recv(BUFSIZ)  
        # (c) TCP-communication closure
        TCPmsg = 'quit'
        self.Client_HCI.send(TCPmsg)
        self.Client_HCI.recv(BUFSIZ) 
        self.Client_HCI.close()
        # (d) System Exit: MiniGUI
        gobject.idle_add(self.guiUPDATEmsg, '>>> The Essex MI-Based BCI has concluded', 1)
        gobject.idle_add(self.guiUPDATEmsg, '', 2)
        gobject.idle_add(self.guiUPDATEmsg, '', 3)

    

    # ╦╦╦╦╦ Method 5.2.3 - User Tutorial to the System ╦╦╦╦╦
    def UserTutorial_S1(self, Stages):
        'System Pathway to introduce the BCI-software to the User: \
         1) MI-training, 2) command-training & 3) GUI-training'
           
        # (a) ***** Initialization of ANY STAGE *****
        # --- variable declaration
        OutFile, EEG_FEAEXT, Run, Stage_Labels = {}, [], 0, ['Stage 2','Stage 3','Session 2']
        messages = ['Next Run of Stage 1? or Move on to Stage 2?',\
                    'Next Run of Stage 2? or Move on to Stage 3?',\
                    'Next Run of Stage 3? or Move on to Session 2?']                       
        # (b) ***** System Pathway: One Run per Iteration *****
        #     General protocol for training sessions with offline evaluation 
        while not self.EXIT:
            Stage = Stages.pop(0)     
            while not self.EXIT:                   
                # b.1 Initialization     
                # --- stage_num := numberofstage ~ numberofrun
                Run += 1       
                # --- GUI Update
                gobject.idle_add(self.guiUPDATEmsg, '>>> SESSION 1 - User Tutorial: ' + default_stages[0][Stage], 1)
                gobject.idle_add(self.guiUPDATEmsg, '', 2)
                # --- START eeg-recording
                self.Client_HCI.send('254')
                self.Client_HCI.recv(BUFSIZ) 
                # --- TCP Communication                      
                self.Client_HCI.send(default_TCPmsg[0][Stage])        
                self.Client_HCI.recv(BUFSIZ)     
                time.sleep(5)            
                # --- uploading the trial sequence, current state & TCP-message
                cue_targets = Session1_Tracks(Stage, Run, self.Idle_ON, self.numtr_run)
                # b.2 Run Execution: DAQ + SigCon + FeaExt + FeaSel + Classification + Plot
                EEG_FEAEXT, class_out = self.Protocol_Tune(cue_targets, EEG_FEAEXT, 'training', 'SS1', 'stg'+str(Stage+1))     
                # b.3 Current Run - Data Storage
                # --- getting the last-in features
                eeg_feaext =[]
                for index in range(len(EEG_FEAEXT)): eeg_feaext.append(EEG_FEAEXT[index][-self.numtr_run[index]:,:])
                # --- 'RunN' = [eeg_feaext, class_out]
                key = 'Run' + str(Run)            
                OutFile.update({key: [eeg_feaext, class_out]})                              
                # b.4 NEXT RUN? or NEXT STAGE?: Waiting for the User's Response         
                # --- STOP eeg-recording
                time.sleep(5)  
                self.Client_HCI.send('255')
                self.Client_HCI.recv(BUFSIZ)      
                # --- avoid the dialog box if the current stage is the last
                if Run == 4: break  
                # --- GUI update & wait
                buttonR = Stage_Labels[Stage]
                buttonL = ''.join(['Run ', str(Run+1)]) 
                self.response = ''
                gobject.idle_add(self.guiDIALOG, default_stages[0][Stage], messages[Stage], buttonL, buttonR)                
                while self.response == '': None    
                # b.5 Switching between NEXT RUN or NEXT STAGE
                if any([self.response == 'Stage', self.response == 'Session']): break 
            # (c) ***** Feature Selection & Classification for all the Runs *****
            if Run != 1:
                if self.DBI: DBIlocs, DBIvalues, DBIlabels = self.On_FeaSel(EEG_FEAEXT)            
                class_out = self.On_ClassDesign(EEG_FEAEXT, DBIlocs, DBIvalues, DBIlabels, 'whole data')           
                OutFile.update({'AllRuns': [EEG_FEAEXT, class_out]})                             
            # (d) ***** Stage Configuration *****           
            # --- current stage ~ data storage
            filename = default_TCPmsg[0][Stage].replace('*','')
            filename = filename.replace('_','')
            filename = ''.join(['Session1_', filename, '.p'])
            cPickle.dump(OutFile, open(root + filename, 'wb'))             
            # --- reset of variables 
            OutFile, EEG_FEAEXT, Run = {}, [], 0  
            # --- exit if stage is 2
            if any([self.EXIT, Stage == 2]): break
            # --- exiting by finishing session
            message = 'Ready to Start Next Stage?'
            self.response = ''
            gobject.idle_add(self.guiDIALOG, default_stages[0][Stage], message, 'Ok', 'Exit')
            while self.response == '': None          
            # --- clear message 3
            gobject.idle_add(self.guiUPDATEmsg, '', 3)
            # --- clear current plot if available  
            if self.Plot: gobject.idle_add(self.guiPLOT_clear)                  
        # (e) ***** Exiting the System ***** 
        # --- exiting by emergency
        if self.EXIT: return
        # --- exiting by finishing session
        message = 'Move on to Session 2? or Exit the System?'
        self.response = ''
        gobject.idle_add(self.guiDIALOG, 'End of User-Tutorial Session', message, 'Session 2', 'Exit')
        while self.response == '': None
        # --- clear message 3
        gobject.idle_add(self.guiUPDATEmsg, '', 3)
        # --- clear current plot if available  
        if self.Plot: gobject.idle_add(self.guiPLOT_clear)  
            

    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.4 - User Training  ╦╦╦╦╦╦╦╦╦╦╦╦
    def UserTraining_S23(self, session, SysType):
        'System Pathway to set the User-Machine Interaction: \
         1) System-Training & 2) System-Testing'
        
        # (a) ***** Initialization of ANY STAGE *****
        # --- skipping this stage if the system has been previously trained
        box_title = ''.join(['Configuration of the ', SysType])
        if SysType == 'Target~Driven System': 
            message,buttonL,buttonR = 'Has the BCI-System already been trained?','Yes','No'
            self.response = ''
            gobject.idle_add(self.guiDIALOG, box_title, message, buttonL, buttonR)
            while self.response == '': None
            if self.response == 'Yes': return
        # --- variable declaration
        OutFile, EEG_FEAEXT, Run, mean_feaext = {}, [], 0, []
        # (b) ***** TRAINING SYSTEM: One Run per Iteration *****
        #     General protocol for TRAINING sessions with offline evaluation        
        while not self.EXIT:            
            Run += 1 
            # b.1 Initialization           
            # --- GUI Update
            text = ''.join(['>>> SESSION ', str(session), ' - ', SysType, ': ', default_stages[1][0]])
            gobject.idle_add(self.guiUPDATEmsg, text, 1)
            gobject.idle_add(self.guiUPDATEmsg, '', 2)
            # --- START eeg-recording
            self.Client_HCI.send('254')
            self.Client_HCI.recv(BUFSIZ)
            # --- TCP Communication                      
            self.Client_HCI.send(default_TCPmsg[1][session-2][0])        
            self.Client_HCI.recv(BUFSIZ)       
            time.sleep(5)    
            # --- uploading the trial sequence, current state & TCP-message
            cue_targets = Session23_Tracks(session, 'training', Run, self.Idle_ON, self.numtr_run)        
            # b.2 Run Execution: DAQ + SigCon + FeaExt + FeaSel + Classification + Plot
            EEG_FEAEXT, class_out = self.Protocol_Tune(cue_targets, EEG_FEAEXT, 'training', 'SS'+str(session), 'stg1')       
            # b.3 Current Run - Data Storage
            # --- getting the last-in features
            eeg_feaext =[]
            for index in range(len(EEG_FEAEXT)): eeg_feaext.append(EEG_FEAEXT[index][-self.numtr_run[index]:,:])
            # --- 'RunN' = [eeg_feaext, class_out]
            key = 'RunTrain' + str(Run)            
            OutFile.update({key: [eeg_feaext, class_out]})             
            # b.4 WHAT FEATURES?: Waiting for the User's Response
            # --- STOP eeg-recording
            time.sleep(5)  
            self.Client_HCI.send('255')
            self.Client_HCI.recv(BUFSIZ)
            # --- GUI update      
            message, buttonL, buttonR = [' all the features',' the best features'], 'Start', 'Exit'
            self.response = ''
            gobject.idle_add(self.guiDIALOG, default_stages[1][1], message, buttonL, buttonR)
            while self.response == '': None
            # +++++ Break point +++++
            if self.EXIT: break
            # (c) ***** TESTING SYSTEM: One Run per Iteration *****
            #     General protocol for TESTING sessions with online classification
            # c.1 Initialization
            # --- GUI Update
            text = ''.join(['>>> SESSION ', str(session), ' - ', SysType, ': ', default_stages[1][1]])
            gobject.idle_add(self.guiUPDATEmsg, text, 1)
            # --- START eeg-recording
            self.Client_HCI.send('254')
            self.Client_HCI.recv(BUFSIZ)
            # --- TCP Communication                      
            self.Client_HCI.send(default_TCPmsg[1][session-2][1])        
            self.Client_HCI.recv(BUFSIZ)        
            time.sleep(5) 
            # --- uploading the trial sequence, current state & TCP-message
            cue_targets = Session23_Tracks(session, 'testing', Run, self.Idle_ON, self.numtr_run)
            # c.2 Online Testing via DAQ + SigCon + FeaExt + FeaSel + Classification + Plot            
            EEG_FEAEXT, class_out = self.Protocol_Tune(cue_targets, EEG_FEAEXT, 'testing', 'SS'+str(session), 'stg2')              
            # c.3 Current Run - Data Storage
            # --- getting the last-in features
            eeg_feaext =[]
            for index in range(len(EEG_FEAEXT)): eeg_feaext.append(EEG_FEAEXT[index][-self.numtr_run[index]:,:])
            # --- 'RunN' = [eeg_feaext, class_out]
            key = 'RunTest' + str(Run)            
            OutFile.update({key: [eeg_feaext, class_out]})                          
            # c.4 NEXT RUN? or NEXT STAGE?: Waiting for the User's Response
            # --- STOP eeg-recording
            time.sleep(5)  
            self.Client_HCI.send('255')
            self.Client_HCI.recv(BUFSIZ)
            # --- avoid the dialog box if the current run is the last
            if Run == 4: break               
            # --- GUI update              
            message = 'Next Run of Stages 1 & 2? or Move on to Stage 3?'
            buttonL = ''.join(['Run', str(Run+1)])
            buttonR = 'Stage 3'
            self.response = ''
            gobject.idle_add(self.guiDIALOG, default_stages[1][1], message, buttonL, buttonR)
            while self.response == '': None         
            # c.5 Switching between NEXT RUN or NEXT STAGE
            if self.response == 'Stage': break      
        # (d) ***** Feature Selection & Classification for all the Runs *****
        # --- only if there are more than one run
        if self.DBI: DBIlocs, DBIvalues, DBIlabels = self.On_FeaSel(EEG_FEAEXT)    
        class_out = self.On_ClassDesign(EEG_FEAEXT, DBIlocs, DBIvalues, DBIlabels, 'whole data')           
        OutFile.update({'AllRuns': [EEG_FEAEXT, class_out]})   
        # --- mean of EEG_FEAEXT
        for matrix in EEG_FEAEXT: mean_feaext.append(np.mean(matrix, axis = 0))       
        # (e) ***** Current Stage ~ Data Storage *****
        filenameA = default_TCPmsg[1][session-2][0].replace('*','')
        filenameA = filenameA.replace('_','')
        filenameB = default_TCPmsg[1][session-2][1].replace('*','')
        filenameB = filenameB.replace('_','')
        filename = '_'.join(['Session'+str(session), filenameA, filenameB])
        cPickle.dump(OutFile, open(root + filename + '.p', 'wb'))       
        # --- clear current plot if available  
        if self.Plot: gobject.idle_add(self.guiPLOT_clear)                                                
        # (f) ***** Exiting the System ***** 
        # --- exiting by emergency
        if self.EXIT: return
        # --- exiting the user-training and configuring the bci-system session (cue-driven or target-driven)
        message   = [' all the features',' the best features',' all the runs']
        for run in range(Run*2): message.insert(-1, ' run ' + str(run+1))
        self.response = ''
        gobject.idle_add(self.guiDIALOG, box_title, message, 'Start', 'Exit')
        while self.response == '': None   
        # --- clear message 3
        gobject.idle_add(self.guiUPDATEmsg, '', 3)
        # --- run attribute
        self.Run = Run*2
        return mean_feaext


    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.5 - System Control ╦╦╦╦╦╦╦╦╦╦╦╦
    def SystemControl_S23(self, session, SysType, mean_feaext):
        'System Pathway to control the BCI-System: \
         1) Cue-Driven System & 2) Target-Driven System'
         
        # (a) ***** Initialization of ANY STAGE *****
        # --- variable declaration
        OutFile, Run, self.eeg_plot = {}, 0, np.zeros(0)
        # --- uploading the trial sequence for cue-driven systems
        #     and audio-targets for target-driven systems
        cues_targets = Session23_CueTarget(SysType) 
        # --- system set-up
        TCPmsg = default_TCPmsg[2][session-2]       
        # 1.- GUI Update
        # --- label modifications
        systype = SysType.replace('-','~')
        systype = systype.title()
        text = ''.join(['>>> SESSION ', str(session), ' - ', systype, ' System: ', default_stages[2][0]])
        gobject.idle_add(self.guiUPDATEmsg, text, 1)
        gobject.idle_add(self.guiUPDATEmsg, '', 2)
        gobject.idle_add(self.guiUPDATEmsg, '', 3)
        # 2.- TCP Communication      
        # --- START eeg-recording
        self.Client_HCI.send('254')
        self.Client_HCI.recv(BUFSIZ)
        # --- type of system                
        self.Client_HCI.send(TCPmsg)        
        self.Client_HCI.recv(BUFSIZ)  
        # --- system initialization
        if SysType == 'cue-driven': 
            gobject.idle_add(self.guiUPDATEmsg, '     The essexHCI is being configurated', 2)
            Initialization_CueDriven(self.Client_HCI) 
        time.sleep(5)   
        # (b) ***** Running the BCI-System *****
        while all([cues_targets != [], not self.EXIT]):   
            # b.1 Initialization
            Run += 1                                            
            # b.2 Run Execution: DAQ + SigCon + FeaExt + FeaSel + Classification
            eeg_feaext = self.Protocol_Assess(cues_targets.pop(0), SysType, mean_feaext)      
            # b.3 Current Run - Data Storage
            # --- 'RunN' = eeg_feaext
            key = 'Run' + str(Run)                  
            filename = '_'.join(['Session' + str(session), SysType, key])
            cPickle.dump(eeg_feaext, open(root + filename + '.p', 'wb'))                                    
        # (d) ***** Exiting the System ***** 
        # --- STOP eeg-recording
        time.sleep(5)  
        self.Client_HCI.send('255')
        self.Client_HCI.recv(BUFSIZ)
        # --- exiting by emergency
        if self.EXIT: return        
        # --- exiting by finishing session
        if SysType == 'cue-driven':            
            message,buttonL,buttonR = 'Move on to Session 3? or Exit the System?','Session 3','Exit'
        else:
            message,buttonL,buttonR = 'Please Press the Exit Button to Conclude the Experiment','None','Exit'
        self.response = ''
        gobject.idle_add(self.guiDIALOG, 'End of the BCI-System Session', message, buttonL, buttonR)
        while self.response == '': None
        # --- clear current plot if available  
        if self.Plot: gobject.idle_add(self.guiPLOT_clear) 


    # ╦╦╦ Method 5.2.6 - Protocol for Tuning the System ╦╦╦╦
    def Protocol_Tune(self, Cue_Target, EEG_FEAEXT, sys_type, ss, stg):
        'Tuning-Protocol: TimingParadigm, DAQ, SigCon, FeaSel, FeaExt & Plot per Run'
        
        # (a) ***** Initialization *****
        # --- features per run
        eeg_feaext, acc_test, mean_feaext = [np.zeros(0), np.zeros(0)], 0, []
        if self.Idle_ON: eeg_feaext.append(np.zeros(0))
        # --- DBI method per run
        DBIlocs, DBIvalues, DBIlabels = np.zeros(0), np.zeros(0), []    
        # --- testing variables
        if sys_type == 'testing':
            # *mean of EEG_FEAEXT
            for matrix in EEG_FEAEXT: mean_feaext.append(np.mean(matrix, axis = 0))
        # (b) ***** Communication Protocol for One Trial per Iteration *****
        while Cue_Target != []:              
            # b.1 Warning Signal
            # --- gui update
            TCPmsg = '1*warning'
            gobject.idle_add(self.guiUPDATEmsg, '>>> TCP~Communication - Instruction Sent: ' + TCPmsg, 2)
            # --- TCP communication
            self.Client_HCI.send(TCPmsg)
            self.Client_HCI.recv(BUFSIZ) 
            # --- protocol timing & signal analysis  
            time.sleep(0.5)    
            if self.FeaExtractor == 'ERD/ERS':
                eeg_epoch = self.On_DAQ(self.RefSamples)
                eeg_ref   = self.On_SigCon(self.RefSamples, eeg_epoch)
            else:
                eeg_ref = None
                time.sleep(self.RefSamples/self.Fs)
            # b.2 Cue Delivery
            # --- cue selection
            TCPmsg = Cue_Target.pop(0)
            # --- gui update  
            gobject.idle_add(self.guiUPDATEmsg, '>>> TCP~Communication - Instruction Sent: ' + TCPmsg, 2)
            # --- TCP communication
            self.Client_HCI.send(TCPmsg)
            self.Client_HCI.recv(BUFSIZ)
            # --- protocol timing
            time.sleep(0.5)
            # b.3 BCI Processing (MI Performance)
            # --- data acquisition
            eeg_epoch = self.On_DAQ(self.MI_Samples)
            # --- signal conditioning
            eeg_dsp   = self.On_SigCon(self.MI_Samples, eeg_epoch)
            # --- feature extraction
            features  = self.On_FeaExt(eeg_dsp, eeg_ref)       
            if self.fea_idxs[self.FeaChoice[0]] != []: 
                print 'DAQ_data:', np.shape(eeg_epoch),' SigCon_data:', np.shape(eeg_dsp),' FeaExt_data:', np.shape(features),
                print ' Class_data:', len(self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]][0]), len(self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]][-1])
            else:
                print 'DAQ_data:', np.shape(eeg_epoch),' SigCon_data:', np.shape(eeg_dsp),' FeaExt_data:', np.shape(features)
            # --- saving the features  
            TCPmsg = TCPmsg.split('*')[-1]
            idx = self.cue_labels.index(TCPmsg)
            eeg_feaext[idx] = np.append(eeg_feaext[idx], features)                              
            # b.4 blank -> rest + random intertrial gap
            cue  = TCPmsg.split('_')[-1]
            if sys_type == 'training':
                TCPmsg = '_'.join(['6*blank', cue])
            elif sys_type == 'testing':
                command = self.On_Classification(mean_feaext, features, self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]])      
                TCPmsg  = ''.join([trig_cmds[command], command, '_', cue])
                if cue == command: acc_test += 1
            gobject.idle_add(self.guiUPDATEmsg, '>>> TCP~Communication - Instruction Sent: ' + TCPmsg, 2)
            self.Client_HCI.send(TCPmsg)
            self.Client_HCI.recv(BUFSIZ)                
            time.sleep(rd.uniform(2, 3))    
        # b.5 Accuracy of testing stages
        if sys_type == 'testing':
            acc_test = 100 * (acc_test/np.sum(self.numtr_run))
            print '*Accuracy of Testing Stage: ', acc_test
            gobject.idle_add(self.guiUPDATEmsg, '>>> Accuracy of Testing Stage: ' + str(acc_test), 3)
            time.sleep(5)
        # (c) System Evaluation through Feature Selection
        # --- reshaping feature information into trials x features
        for index in range(len(eeg_feaext)): 
            eeg_feaext[index] = np.reshape(eeg_feaext[index],(self.numtr_run[index],len(features)))
        # --- feature selection if it's required
        if self.DBI: DBIlocs, DBIvalues, DBIlabels = self.On_FeaSel(eeg_feaext)
        # --- feature distribution (all the features and the current features)
        if EEG_FEAEXT == []:
            EEG_FEAEXT = eeg_feaext
        else:
            for index in range(len(EEG_FEAEXT)): EEG_FEAEXT[index] = np.concatenate((EEG_FEAEXT[index],eeg_feaext[index]),axis = 0)
        for item in EEG_FEAEXT: print '*ClassData_all: ', np.shape(item)
        # (d) ***** Classification Process *****
        # --- half data -> training, half data -> testing
        # --- for training systems, the ClassDesign takes only the 20 last-in trials (it means the last run)
        # --- for testing systems, the ClassDesign takes the 40 last-in trials (it means the last run of training and testing)
        for item in eeg_feaext: print '*ClassData_design: ', np.shape(item)
        class_out = self.On_ClassDesign(eeg_feaext, DBIlocs, DBIvalues, DBIlabels, 'current run')
        # (e) ***** Feature Plot *****
        if self.Plot: self.Eval_Plot(EEG_FEAEXT, ss, stg)        
        # (f) ***** Return of Variables *****
        return EEG_FEAEXT, class_out    


    # ╦╦ Method 5.2.7 - Protocol for Assessing the System ╦╦
    def Protocol_Assess(self, Cue_Target, sys_type, mean_feaext):
        'Assessing-Protocol: TimingParadigm, DAQ, SigCon, FeaSel, FeaExt & Plot per Switch'
        
        # (a) ***** Initialization *****
        # --- default variables
        TCPmsg, original_cue, eeg_feaext, cue, command = '', None, np.zeros(0), 'unknown_cue', 'unknown_command'
        self.response = 'No Stops'
        # --- splitting of targets and codes 
        targets, codes = Cue_Target[0], Cue_Target[-1]
        # --- sending audio-target for target-driven systems
        if sys_type == 'target-driven':
            AudioTrack = targets
            targets = ['5*cue_unknown']  
            self.Client_HCI.send(AudioTrack)
            self.Client_HCI.recv(BUFSIZ)                      
        # (b) ***** Communication Protocol for One Target *****
        while all([targets!=[], TCPmsg != codes, not self.EXIT]):   
            while self.response == '': None
            # b.1 Warning Signal
            # --- gui update
            TCPmsg = '1*warning'
            gobject.idle_add(self.guiUPDATEmsg, '>>> TCP~Communication - Instruction Sent: ' + TCPmsg, 2)
            # --- TCP communication
            self.Client_HCI.send(TCPmsg)
            ans = self.Client_HCI.recv(BUFSIZ) 
            if cue == command: targets = Achieved_Targets(ans,original_cue,targets,codes)
            # --- protocol timing & signal analysis  
            time.sleep(0.5)    
            if self.FeaExtractor == 'ERD/ERS':
                eeg_epoch = self.On_DAQ(self.RefSamples)
                eeg_ref   = self.On_SigCon(self.RefSamples, eeg_epoch)
            else:
                eeg_ref = None
                time.sleep(self.RefSamples/self.Fs)
            # b.2 Cue Delivery
            # --- cue selection
            TCPmsg = targets[0]
            # --- gui update  
            gobject.idle_add(self.guiUPDATEmsg, '>>> TCP~Communication - Instruction Sent: ' + TCPmsg, 2)
            # --- TCP communication
            self.Client_HCI.send(TCPmsg)
            self.Client_HCI.recv(BUFSIZ)
            # --- protocol timing
            time.sleep(0.5)
            # b.3 BCI Processing (MI Performance)
            # --- data acquisition
            eeg_epoch = self.On_DAQ(self.MI_Samples)
            # --- signal conditioning
            eeg_dsp   = self.On_SigCon(self.MI_Samples, eeg_epoch)
            # --- feature extraction
            features  = self.On_FeaExt(eeg_dsp, eeg_ref)   
            #    *print out data
            if self.fea_idxs[self.FeaChoice[0]] != []: 
                print 'DAQ_data:', np.shape(eeg_epoch),' SigCon_data:', np.shape(eeg_dsp),' FeaExt_data:', np.shape(features),
                print ' Class_data:', len(self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]][0]), len(self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]][-1])
            else:
                print 'DAQ_data:', np.shape(eeg_epoch),' SigCon_data:', np.shape(eeg_dsp),' FeaExt_data:', np.shape(features)
            # --- saving the features  
            eeg_feaext = np.append(eeg_feaext, features)                                    
            # b.4 blank -> rest + random intertrial gap
            # --- comparison between the cue & command
            #     if ans == correct: the target is removed from the list of cues
            command = self.On_Classification(mean_feaext, features, self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]])
            #!!!!!!!!!!!!!!!! This is only for testing purposes !!!!!!!!!!!!!!!!
            #if sys_type == 'target-driven':
            #    pointer = POINTERS[AudioTrack].pop(0)
            #    command = COMMANDS[pointer]
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!            
            cue     = TCPmsg.split('_')[-1]
            if cue == command: original_cue = targets.pop(0)
            # --- TCP-message delivery & gui update
            TCPmsg  = ''.join([trig_cmds[command], command, '_', cue])           
            gobject.idle_add(self.guiUPDATEmsg, '>>> TCP~Communication - Instruction Sent: ' + TCPmsg, 2)
            self.Client_HCI.send(TCPmsg)
            TCPmsg = self.Client_HCI.recv(BUFSIZ)           
            # --- break     
            time.sleep(rd.uniform(2, 3))                              
        # (c) ***** Data Re-Configuration *****
        ydim = len(features)
        xdim = np.size(eeg_feaext)//ydim
        eeg_feaext = np.reshape(eeg_feaext, (xdim, ydim))
        # (d) ***** Feature Plotting *****        
        if self.Plot: self.Eval_UniquePlot(eeg_feaext, self.fea_idxs[self.FeaChoice[0]][self.FeaChoice[-1]])        
        # (e) ***** Return of Variables *****
        return eeg_feaext

    
    # ╦╦╦╦╦╦ Method 5.2.8 - Data Acquisition (DAQ) ╦╦╦╦╦╦╦╦
    def On_DAQ(self, daq_samples):
        'Online Data Acquisition: The Whole Epoch in Use'

        # (a) ***** Local Variables Declaration *****
        current_samples, data = 0, ''
        eeg_epoch = np.zeros((self.TCP_ch, 1))             
        # (b) ***** BioSemi TCP Communication Start ******
        Client_T11 = socket(AF_INET, SOCK_STREAM)
        Client_T11.connect(self.ADDR)
        # ...........Data Acquisition per epoch.............
        while current_samples < daq_samples:        
        # (c) ***** Default Variables into the Loop *****
            tempo = np.zeros((self.TCP_ch, self.TCP_samples))            
        # (d) ***** Sample Collection per TCP_array *****
            # --- loop to ensure a complete TCP_array collection
            while len(data) < self.TCP_array: data += Client_T11.recv(self.TCP_array)
            # --- saving data till to get the require length (i.e., daq_samples)
            BYTES = data[:self.TCP_array]
            data =  data[self.TCP_array:]
        # (e) ***** Conversion from 24bits to Voltage ***** 
            BYTES = bits_float(BYTES)                
            # --- Converting in microvolts
            BYTES = BYTES * 31.25e-3
        # (f) ***** Data Re-Organization into Channels *****                
            new_ch_idx = 0
            for ch in range(self.TCP_ch):
                tempo[new_ch_idx, :] = BYTES[ch::self.TCP_ch]
                new_ch_idx += 1
            eeg_epoch = np.append(eeg_epoch, tempo, axis = 1)
            current_samples += self.TCP_samples
        # (g) ***** Delete the first column of eeg_epoch created by default *****          
        eeg_epoch = np.delete(eeg_epoch, 0, axis = 1)
        # (h) ***** BioSemi TCP client closure *****
        Client_T11.close()
        return eeg_epoch


    # ╦╦╦╦╦╦╦╦ Method 5.2.9 - Signal Conditioning ╦╦╦╦╦╦╦╦╦
    def On_SigCon(self, daq_samples, eeg_epoch):
        'Online Signal Conditioning'
 
        # (a) ***** Variable Declaration *****
        # --- spectral filtering
        num_ch, num_sam = np.shape(eeg_epoch)
        eeg_tempo = np.zeros((len(self.total_chs), num_sam))
        ch_idxsA  = zip(range(len(self.total_chs)), self.total_chs)
        # --- spatial filtering
        num_ch  = len(self.ch_pos)
        num_sam = daq_samples//self.downsample_rate
        eeg_dsp = np.zeros((num_ch, num_sam))
        ch_idxsB= zip(range(num_ch), self.ch_pos) 
        # (b) Spectral Filtering in order to avoid disturbance during the referencing procedure
        #     (it is applied to all the available channels)
        for new_ch, ch in ch_idxsA:     
            eeg_tempo[new_ch,:] = SiGCoN(ch,eeg_epoch,self.LAYOUT,self.reference,self.bandwidth,self.bandrejection,self.DCband,self.downsample_rate,'spectral',[])
        # (c) Spatial Filtering + Downsampling (applied only to the required channels)
        for new_chpos, ch_pos in ch_idxsB:
            eeg_dsp[new_chpos,:] = SiGCoN(ch_pos,eeg_tempo,self.LAYOUT,self.reference,self.bandwidth,self.bandrejection,self.DCband,self.downsample_rate,'spatial',[])    
        return eeg_dsp
    
    
    # ╦╦╦ Method 5.2.10 - Feature Extraction: BAND-POWER ╦╦╦
    def On_FeaExt(self, eeg_dsp, eeg_ref):
        'Online Feature Extraction'
        
        # (a) ***** Local Variable Declaration *****
        dimX= np.size(eeg_dsp, axis = 0)
        dimY= np.size(eeg_dsp, axis = 1)
        row, idx_ref = np.zeros(0), 0
        # --- reference calculation for ERD/ERS mode
        if self.FeaExtractor == 'ERD/ERS': EEG_REF = ERDSPower_REF(eeg_ref, self.bandpass_filtering)  
        # (b) Band power calculation according to ABSOLUTE/RELATIVE/ERDS modes
        # --- BP estimates according to SEGMENTATION and for the selected channels                        
        for ch in range(dimX):
            for band in self.bandpass_filtering:                           
                if band[0] == 'on':
                    if self.FeaExtractor == 'ERD/ERS': eeg_ref, idx_ref = EEG_REF[idx_ref], idx_ref+1
                    row = np.append(row, \
                    BandPower(self.FeaExtractor,eeg_dsp[ch, :],band,self.bandpass_filtering,eeg_ref,self.SegSamples,self.OverlapSamples,dimY))                           
        # (c) ***** Scaling Data *****
        # --- reshaping to have a 2D-array
        row = np.reshape(row, (1,len(row))) 
        # --- normalization 
        row = mlpy.data_normalize(row)
        # --- returning to 1D-array to keep consistence in the program
        row = np.squeeze(row)
        return row    


    # ╦╦╦╦ Method 5.2.11 - Feature Selection: DBI Method ╦╦╦
    def On_FeaSel(self, eeg_feaext):
        'Online Feature Selection: DBI Method'

        # (a) ***** GUI update *****
        gobject.idle_add(self.guiUPDATEmsg, '>>> Signal~Analysis - Feature Selection.', 2)
        # (b) ***** David-Bouldin Index Method *****
        # --- DBI calculation (DBIlocs := location of the features organized in ascending order,\
        #                      DBIarray:= DBI values organized in ascending order)
        DBIlocs, DBIvalues = DBI_Method(eeg_feaext)
        # --- DBI Labelling according to the channel, frequency band and time series
        DBIlabels = self.CLASSp.Feature_Labels(self.OverlapSamples, self.bandpass_filtering, DBIlocs, range(self.num_BS)) 
        return DBIlocs, DBIvalues, DBIlabels[0]       


    # ╦╦╦╦╦╦╦╦╦ Method 5.2.12 - Model of Classifier ╦╦╦╦╦╦╦╦
    def On_ClassDesign(self, EEG_feaext, DBIloc, DBIvalue, DBIlabel, MSG):
        'Modelling of a Classifier via Traning & Testing Data'
       
        # (a) ***** DatA PreprocessinG *****
        # a.1 General Variable Declaration      
        # --- data storage for consecutive iteration 
        #     (i.e., several runs to find the optimum number of features)      
        class_out = {}
        selection_out = {'DBI': DBIloc}
        # --- feature characteristics
        tr_train, tr_test = [], []
        for item in EEG_feaext:
            numtr, numfea = np.shape(item)
            tr_train.append(range(0,numtr,2))
            tr_test.append(range(1,numtr,2))
        # --- feature-indices used to classify
        FEATURE_IDX, Range, Step = self.CLASSp.Organization_Features(selection_out, numfea) 
        # --- outcome variables
        class_ALL, numfea_ALL, class_best, numfea_best, MODEL = None, None, None, None, None
        # (b) Dataset Construction for Classification Process
        self.CLASSp.Datasets(EEG_feaext, tr_train, tr_test)
        # ---------------------- Classification Process  -----------------------
        models, GridSearch, Accuracy, Predictions, RUN = [], [], [], [], 0
        for feature_indices in FEATURE_IDX:  
            RUN += 1      
            # (c) ***** Classfier Creation *****
            MODELS, GRID_SEARCH, ACCURACY, PREDICTIONS = self.CLASSp.Classifier_Creator(feature_indices)                                           
            # (d) *****  Saving the Outcomes of One Run *****
            # --- MODELS      = [Classifier 1, Classifier 2]
            # --- models      = [MODELS_Run1, MODELS_Run2, ..., MODELS_RunM]
            # --- GRID_SEARCH = [[bestparameters_C1, accuracy_C1],[bestparameters_C2, accuracy_C2]]   
            # --- GridSearch  = [GRID_SEARCH_Run1, GRID_SEARCH_Run2,..., GRID_SEARCH_RunM] 
            # --- ACCURACY    = testing hits for the current run (for each model)
            # --- Accuracy    = [accuracy_Run1, accuracy_Run2,..., accuracy_RunM]
            # --- PREDICTIONS = predicted labels during testing (for each model) 
            # --- Predictions = [predictions_Run1, predictions_Run2,..., predictions_RunM]
            models.append(MODELS)
            GridSearch.append(GRID_SEARCH)
            Accuracy.append(ACCURACY)
            Predictions.append(PREDICTIONS)               
            # (e) **** GUI update *****
            message1 = '>>> Signal~Analysis - Classification: '+'RUN='+str(RUN)+', ACC='+str(ACCURACY)
            gobject.idle_add(self.guiUPDATEmsg, message1, 2)
        # (f) ***** Saving Final Results *****
        class_out.update({'GridSearch_per_Run': GridSearch})
        class_out.update({'Accuracy_per_Run': Accuracy})
        class_out.update({'Predictions_per Run': Predictions})
        class_out.update({'RunStep_&_RunEnd': [Step, Range[-1]]})
        # ----------------------------------------------------------------------
        # (g) ***** Printing the Final Results *****
        # --- classification accuracy considering all the features, or
        #     considering the features selected by default (only one run)
        class_ALL, numfea_ALL, run_idx = Accuracy[-1], [], []
        for item in FEATURE_IDX[-1]: 
            numfea_ALL.append(len(item))
            run_idx.append(-1)
        # --- classification accuracy considering the best features
        #     across the runs executed (only available if DBIfeatures was filled in)
        if len(Accuracy) > 1:
            tempo_acc, class_best, run_idx, numfea_best = np.array(Accuracy), [], [], []
            for col in range(np.size(tempo_acc, axis = 1)):
                class_best.append(np.max(tempo_acc[:, col]))
                run_idx.append(np.where(tempo_acc[:, col] == class_best[-1])[0][0])
                numfea_best.append(len(FEATURE_IDX[run_idx[-1]][0]))             
            # --- gui update
            message2 =  '>>> This classification corresponds to the ' + MSG + ': '
            gobject.idle_add(self.guiUPDATEmsg, message2, 2)
            message3 = ['        ','class_all { (',str(class_ALL[0])[:4],', ',str(class_ALL[-1])[:4],')%, (',str(numfea_ALL[0])[:4],', ',str(numfea_ALL[-1])[:4],')#} ',\
                                   'class_best { (',str(class_best[0])[:4],', ',str(class_best[-1])[:4],')%, (',str(numfea_best[0])[:4],', ',str(numfea_best[-1])[:4],')#} ',]
            gobject.idle_add(self.guiUPDATEmsg, ''.join(message3), 3)
            # --- evaluation storage
            class_out.update({'class_all': [class_ALL, numfea_ALL]})
            class_out.update({'class_best': [class_best, numfea_best]})
            # (h) ***** Attribute Declaration *****
            self.fea_idxs['class_best'].append([])
            self.Models['class_best'].append([])
            for index in range(len(run_idx)):
                self.fea_idxs['class_best'][-1].append(FEATURE_IDX[run_idx[index]][index])        
                self.Models['class_best'][-1].append(models[run_idx[index]][index])
            self.fea_idxs['class_all'].append(FEATURE_IDX[-1])
            self.Models['class_all'].append(models[-1])
            # (i) ***** Evaluation of the Tree~Design *****
            # --- classification of all the features
            ACC_all = self.CLASSp.Tree_Evaluation(self.Models['class_all'][-1], self.fea_idxs['class_all'][-1])
            ACC_best = self.CLASSp.Tree_Evaluation(self.Models['class_best'][-1], self.fea_idxs['class_best'][-1])
            # --- screen printing
            print '--------------------------- Tree Assessment ---------------------------'
            print '--> The classification for all the features is: ', ACC_all
            print '--> The classification for the best features is: ', ACC_best
            print '-----------------------------------------------------------------------' 
        else:
            # --- gui update
            message2 =  '>>> This classification corresponds to the ' + MSG + ': '
            gobject.idle_add(self.guiUPDATEmsg, message2, 2)
            message3 = ['        ','class_all { (',str(class_ALL[0])[:4],', ',str(class_ALL[-1])[:4],')%, (',str(numfea_ALL[0])[:4],', ',str(numfea_ALL[-1])[:4],')#} ']
            gobject.idle_add(self.guiUPDATEmsg, ''.join(message3), 3)
            # --- evaluation storage
            class_out.update({'class_all': [class_ALL, numfea_ALL]})
            # (h) ***** Attribute Declaration *****
            self.Models['class_all'].append(models[-1])
            # (i) ***** Evaluation of the Tree~Design *****
            # --- classification of all the features
            ACC_all = self.CLASSp.Tree_Evaluation(self.Models['class_all'][-1], FEATURE_IDX[-1])
            # --- screen printing
            print '--------------------------- Tree Assessment ---------------------------'
            print '--> The classification for all the features is: ', ACC_all
            print '-----------------------------------------------------------------------'       
        print '''*self.Models['class_all']: ''', len(self.Models['class_all'])
        print '''*self.Models['class_best']: ''', len(self.Models['class_best'])                 
        return class_out

        
    # ╦╦╦╦╦╦╦╦ Method 5.2.13 - Online Classification ╦╦╦╦╦╦╦
    def On_Classification(self, Mean_Feaext, Features, Indices):
        'Online Classification'
    
        # (a) ***** Classification of Three Classes *****
        if self.Idle_ON:      
            # --- Variable Re-Assignment
            Classifier1 = self.Models[self.FeaChoice[0]][self.FeaChoice[-1]][0]
            Classifier2 = self.Models[self.FeaChoice[0]][self.FeaChoice[-1]][-1]  
            Features1 = Features[Indices[0]] 
            Features2 = Features[Indices[-1]] 
            # --- Fisher Discriminant Analysis (FDA)
            if self.Classifier == 'FDA':                    
                pred = Classifier1.predict(Features1)   
                # idle detection
                if pred == -1:
                    TCPmsg = 'idle'
                # MI detection
                else:
                    pred = Classifier2.predict(Features2)
                    # Right detection
                    if pred == -1:
                        TCPmsg = 'right'
                    # Left detection
                    else:
                        TCPmsg = 'left'
            # --- Support Vector Machine (SVM)
            else:
                pred, accuracy, dec_vals = libsvm.svm_predict([0], Features1.tolist(), Classifier1);
                # idle detection
                if int(pred[0]) == -1:
                    TCPmsg = 'idle'                    
                # MI detection
                else:
                    pred, accuracy, dec_vals = libsvm.svm_predict([0], Features2.tolist(), Classifier2);
                    # Right detection
                    if int(pred[0]) == -1:
                         TCPmsg = 'right'
                    # Left detection
                    else:
                        TCPmsg = 'left'               
        # (b) ***** Classification of only Two Classes *****
        else:
            # --- Variable Re-Assignment
            Classifier1 = self.Models[self.FeaChoice[0]][self.FeaChoice[-1]][0]
            Features1 = Features[:, Indices[0]] 
            # --- Fisher Discriminant Analysis (FDA)
            if self.Classifier == 'FDA':
                pred = Classifier1.predict(Features1)
                # Right detection
                if pred == -1:
                    TCPmsg = 'right'
                # Left detection
                else:
                    TCPmsg = 'left'                     
            # --- Support Vector Machine (SVM)
            else:
                pred, accuracy, dec_vals = libsvm.svm_predict([0], Features1.tolist(), Classifier1);
                # Right detection
                if int(pred[0]) == -1:
                     TCPmsg = 'right'
                # Left detection
                else:
                    TCPmsg = 'left'    
        # (c) ***** OnLine-Plotting *****
        # if self.Plot: self.On_Plot(Mean_Feaext, Features[0,:], Indices)
        return TCPmsg


    # ╦╦╦╦╦╦╦ Method 5.2.14 - XP-Plot Configuration ╦╦╦╦╦╦╦╦
    def Eval_Plot(self, eeg_data, ss, stg):
        'XY-Plot Configuration'    
        
        # (a) ***** Variable Declaration *****
        axs, max_ax1, min_ax1 = [], [], []
        # --- variables for plot-purposes
        brain_states, FIG, numcol, plot = [0, 1], plt.figure(), 1, 0
        if self.Idle_ON: brain_states.append(2)
        if self.DBI: numcol = 2
        # --- eeg_data shape
        numtr, numfea = np.shape(eeg_data[0])     
        # --- current run
        crun = numtr//self.numtr_run[0]
        for state in brain_states: 
            # --- variables for storing the plot lines
            tempo, lines, legend_labels = [], [], []
            plot += 1    
            # (b) ***** Plot of All the Features *****            
            # --- figure configuration           
            ax1 = FIG.add_subplot(len(brain_states), numcol, plot)
            ax1.set_title(Titles[state][0], fontname='Byington', fontsize= 10, color = 'white')     
            ax1.tick_params(labelsize = 8, labelcolor = 'white')                          
            ax1.grid(True)   
            # --- plot and legend creation (all the available data)   
            if numtr != self.numtr_run[0]:                                  
                # --- plot and legend creation (all the available data)
                signal = np.mean(eeg_data[state], axis = 0)
                max_ax1.append(np.max(signal))
                min_ax1.append(np.min(signal))
                tempo.append(ax1.plot(signal, color = blue, linewidth = 2.5))
                lines.append(tempo[-1][0])
                legend_labels.append('All the Runs') 
            # --- plot and legend creation (current data only)
            signal = np.mean(eeg_data[state][-self.numtr_run[state]:, :], axis = 0)
            max_ax1.append(np.max(signal))
            min_ax1.append(np.min(signal))                
            tempo.append(ax1.plot(signal, color = orange, linewidth = 1.25))
            lines.append(tempo[-1][0])
            legend_labels.append('Run ' + str(crun))   
            # --- axis storage
            axs.append(ax1)
            # (c) ***** Plot of Selected Features *****
            if self.DBI:
                plot += 1
                # --- figure configuration           
                ax2 = FIG.add_subplot(len(brain_states), numcol, plot)   
                ax2.set_title(Titles[state][-1], fontname='Byington', fontsize= 10, color = 'white')           
                ax2.tick_params(labelsize = 8, labelcolor = 'white')                          
                ax2.grid(True) 
                # --- plot and legend creation (best features across the current run)
                style_line, style_marker = ['r', 'g:'], ['r*', 'g.']
                for i in range(len(self.fea_idxs['class_best'][-1])):                    
                    signal = np.mean(eeg_data[state][-self.numtr_run[state]:, self.fea_idxs['class_best'][-1][i]], axis = 0)
                    tempo.append(ax2.stem(self.fea_idxs['class_best'][-1][i],signal,linefmt=style_line[i],markerfmt=style_marker[i],basefmt='k-'))
                    lines.append(tempo[-1][0])
                    legend_labels.append('Run ' + str(crun) + '_C' + str(i+1))    
        # (d) ***** Plot Configuration *****
        # --- plot~limit configuration
        for ax in axs:
            ax.set_xlim(0, numfea) 
            ax.set_ylim(min(min_ax1), max(max_ax1))
        # --- legend
        legend = plt.figlegend(lines,legend_labels,loc='lower center',shadow=True,ncol=len(lines),fancybox = True,borderpad=0.1)                     
        for t in legend.get_texts(): t.set_fontsize(10)
        for t in legend.get_texts(): t.set_fontname('Byington')
        for l in legend.get_lines(): l.set_linewidth(2)               
        FIG.subplots_adjust(left=0.075,right=0.95,bottom=0.1,top=0.925,hspace=0.3)
        # --- figure title
        filename = '_'.join(['features', ss, stg, str(crun)])
        filename = ''.join([root, filename, '.png'])
        plt.savefig(filename, facecolor = blue)                
        # (e) ***** GUI update *****           
        self.guiPLOT(Image(filename))


    # ╦╦╦╦╦╦╦ Method 5.2.15 - XP-Plot Configuration ╦╦╦╦╦╦╦╦
    def Eval_UniquePlot(self, eeg_data, idxs):
        'XY-Plot Configuration: Cue-Driven or Target-Driven Systems'    
        
        # (a) ***** Variable Declaration *****
        # --- figure creation
        FIG = plt.figure()
        # --- mean data 
        eeg_data = np.mean(eeg_data, axis = 0)       
        eeg_data = np.reshape(eeg_data, (1, len(eeg_data)))
        # --- variable update
        if self.eeg_plot.tolist() == []:
            self.eeg_plot = eeg_data
        else:           
            self.eeg_plot = np.append(self.eeg_plot, eeg_data, axis = 0)
        # --- data dimensions
        num_tar, num_fea = np.shape(self.eeg_plot) 
        # --- variables for storing the plot lines
        lines, legend_labels = [], []
        ax = FIG.add_subplot(111)
        # (b) ***** Plot of All the Features *****   
        # b.1 mean of all the features
        tempo = []                        
        # --- figure configuration           
        ax.set_title('Features per Pursuing Target', fontname='Byington', fontsize= 10, color = 'white')           
        ax.tick_params(labelsize = 8, labelcolor = 'white')                                                                
        # --- plot and legend creation (all the available data)
        if num_tar != 1:            
            eeg_mean = np.mean(self.eeg_plot, axis = 0)
            tempo.append(ax.plot(eeg_mean, color = blue, linewidth = 2.5))
            lines.append(tempo[-1][0])
            legend_labels.append('All Features') 
        # b.2 mean of the target N features                                             
        # --- plot and legend creation (current target data)
        tempo.append(ax.plot(self.eeg_plot[-1,:], color = orange, linewidth = 1.25))
        lines.append(tempo[-1][0])        
        legend_labels.append('Target' + str(num_tar) + ' Features')          
        # b.3 mean of the target selected features                                             
        # --- plot and legend creation (current selected target data)
        style_line, style_marker, i = ['r', 'g:'], ['r*', 'g.'], 0
        for idx in idxs:
            if num_fea != len(idx):
                tempo.append(ax.stem(idx, self.eeg_plot[-1, idx], linefmt = style_line[i], markerfmt = style_marker[i], basefmt='k-'))
                lines.append(tempo[-1][0])        
                legend_labels.append('Target' + str(num_tar) + ' DBI-Features' + 'C' + str(i+1))    
            i += 1   
        # --- axis configuration
        ax.set_xlim(0, num_fea) 
        ax.axhline(y = 0, xmin = 0, xmax = num_fea, color = 'black', linewidth = 0.5)
        # (c) ***** Legend Configuration *****                 
        legend = plt.figlegend(lines,legend_labels,loc='lower center',shadow=True,ncol=len(lines),fancybox = True,borderpad=0.1)                     
        for t in legend.get_texts(): t.set_fontsize(10)
        for t in legend.get_texts(): t.set_fontname('Byington')
        for l in legend.get_lines(): l.set_linewidth(2)               
        FIG.subplots_adjust(left=0.075,right=0.95,bottom=0.1,top=0.925,hspace=0.3)
        # --- filename figure
        filename = ''.join([root, 'features_', 'target', str(num_tar), '.png'])
        plt.savefig(filename, facecolor = blue)                
        # (c) GUI update           
        self.guiPLOT(Image(filename))


    # ╦╦╦╦╦╦╦ Method 5.2.16 - XP-Plot Configuration ╦╦╦╦╦╦╦╦
    def On_Plot(self, Mean_Feaext, Features, Indices):
        'XY-Plot Configuration: for Online-Classification Systems'    
        
        # (a) ***** Variable Declaration *****
        # --- figure creation
        FIG = plt.figure()       
        # (b) ***** Plot of the Features *****   
        # b.1 left MI 
        ax1 = FIG.add_subplot(311)
        # --- figure configuration           
        ax1.set_title('Left and Current Brain State', fontname='Byington', fontsize= 10, color = 'white')           
        ax1.tick_params(labelsize = 8, labelcolor = 'white')   
        ax1.grid(True)                                                             
        # --- plot and legend creation                   
        ax1.plot(Indices, Mean_Feaext[0][Indices], color = blue, marker = '.')
        ax1.plot(Indices, Features, color = 'm', marker = '*')    
        # b.2 right MI
        ax2 = FIG.add_subplot(312)
        # --- figure configuration           
        ax2.set_title('Right and Current Brain State', fontname='Byington', fontsize= 10, color = 'white')           
        ax2.tick_params(labelsize = 8, labelcolor = 'white')   
        ax2.grid(True)                
        # --- plot and legend creation                   
        ax2.plot(Indices, Mean_Feaext[1][Indices], color = orange, marker = '.')
        ax2.plot(Indices, Features, color = 'm', marker = '*')    
        # b.3 idle MI
        if self.Idle_ON:
            ax3 = FIG.add_subplot(313)
            # --- figure configuration           
            ax3.set_title('Idle and Current Brain State', fontname='Byington', fontsize= 10, color = 'white')           
            ax3.tick_params(labelsize = 8, labelcolor = 'white')   
            ax3.grid(True) 
            # --- plot and legend creation                   
            ax3.plot(Indices, Mean_Feaext[-1][Indices], color = 'k', marker = '.')
            ax3.plot(Indices, Features, color = 'm', marker = '*')               
        # (c) ***** Figure Configuration *****                               
        FIG.subplots_adjust(left=0.075,right=0.95,bottom=0.1,top=0.925,hspace=0.3)
        # --- filename figure
        filename = ''.join([root, 'features', '.png'])
        plt.savefig(filename, facecolor = blue)                
        # (c) GUI update           
        self.guiPLOT(Image(filename))


    # ╦╦╦╦╦╦╦ Method 5.2.17 - Classifier Selection ╦╦╦╦╦╦╦╦╦
    def choose_MODEL(self, widget):
        'Selection of the Classifier'
        
        message   = [' all the features',' the best features',' all the runs']
        for run in range(self.Run): message.insert(-1, ' run ' + str(run+1))
        self.response = ''
        gobject.idle_add(self.guiDIALOG, 'Reselection of the Classifier', message, 'Start', 'Exit')


    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.18 - miniGUI Update ╦╦╦╦╦╦╦╦╦╦╦
    def guiUPDATEmsg(self, msg, number):
        'MiniGUI Update - messages'
        
        if number == 1:
            self.message1.set_text(msg)
        elif number == 2:
            self.message2.set_text(msg)
        elif number == 3:
            self.message3.set_text(msg)
        return False
     
        
    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.19 -miniGUI Update ╦╦╦╦╦╦╦╦╦╦╦╦
    def guiPLOT(self, current_Image):
        'MiniGUI Update - plot'
        
        if self.prevImage != None: self.prevImage.clear()
        self.table.attach(current_Image, 0, 10, 11, 20)   
        self.prevImage = current_Image
        return False


    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.20 -miniGUI Update ╦╦╦╦╦╦╦╦╦╦╦╦
    def guiPLOT_clear(self):
        'MiniGUI Update - clear plot'
        
        if self.prevImage != None: 
            self.prevImage.clear()
            self.prevImage = None
        return False
       
        
    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.21 -miniGUI update ╦╦╦╦╦╦╦╦╦╦╦╦
    def guiDIALOG(self, title, message, buttonL, buttonR):
        'MiniGUI Update - Next Stage or Next Run?'
        
        # (a) Variable Declaration
        reply = 0
        # (b) Dialog Creation        
        if buttonL == 'None':
            Buttons = (buttonR, 2)
        else:
            Buttons = (buttonL, 1, buttonR, 2)
        dialog = gtk.Dialog(title,None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, Buttons)
        STYLE = dialog.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL] = dialog.get_colormap().alloc_color('#DCDCDC')
        dialog.set_style(STYLE)
        # (c) Added Widget to the Dialog
        # --- a message
        if type(message) == str:
            message = Label(message+'\n', font, 'black', 0, 0.5)
            dialog.vbox.pack_start(message)          
        # --- a serie of radio buttons
        else:
            self.FeaChoice = ['class_all', -1]
            print '*Current Classifier: ', self.FeaChoice
            table = gtk.Table(6, 2, False)
            table.show()
            dialog.vbox.pack_start(table) 
            label = Label('Making use of: ', font, 'black', 0, 0.5)    
            table.attach(label, 0, 2, 0, 1)                 
            button1,label1 = Radio_Button(None, message[0], font, 'black')
            button1.connect("toggled", self.guiCHOICE, label1, 'class_all')
            table.attach(button1, 0, 1, 1, 2)  
            button2,label2 = Radio_Button(button1, message[1], font, lblue)
            button2.connect("toggled", self.guiCHOICE, label2, 'class_best')
            table.attach(button2, 0, 1, 2, 3)    
            if len(message) > 2:
                button,label = Radio_Button(None, message[-1], font, 'black')
                button.connect("toggled", self.guiCHOICE, label, -1)
                table.attach(button, 1, 2, 1, 2)
                x, y = 0, 2
                for item in message[2:-1]:
                    button,label = Radio_Button(button, item, font, lblue)
                    button.connect("toggled", self.guiCHOICE, label, x)
                    table.attach(button, 1, 2, y, y+1) 
                    x, y = x+1, y+1           
        # (d) Running the Dialog   
        dialog.show_all()
        reply = dialog.run()
        if reply == 1:              
            self.response = buttonL.split(' ')[0]
        elif reply == 2:
            self.response = buttonR.split(' ')[0]
        else:
            self.EXIT = True
        # (e) Exit Selection
        if self.response == '': self.response = 'Exit'
        if self.response == 'Exit': self.EXIT = True
        dialog.destroy()
        return False             


    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.2.22 - miniGUI update ╦╦╦╦╦╦╦╦╦╦╦
    def guiCHOICE(self, widget, label_widget, text_num):
        'CallBack for the Selection of the Features'
        
        if widget.get_active():
            if type(text_num) == str:
                self.FeaChoice[0] = text_num
            else:
                self.FeaChoice[-1] = text_num
            print '*Current Classifier: ', self.FeaChoice
        else:
            label_widget.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 
        return False


    # ╦╦╦╦╦╦╦╦ Method 5.2.23 - Killing essexVE_BCI ╦╦╦╦╦╦╦╦╦
    def destroy(self, widget):
        'Exit of the BCI-System gui'
         
        # (a) Kill the run-thread 
        self.EXIT = True
        # (d) Closing MiniGUI       
        gtk.main_quit()





# ******************************************************************************
# ************************ 5.3 OffLine BCI System ******************************
# ******************************************************************************
class essexVE_OffLineBCI(threading.Thread):
    'Class to control the OFFLINE Brain Computer Interface Module'


    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.1 - Initialization ╦╦╦╦╦╦╦╦╦╦╦
    def __init__(self):
        'OffLine Processing Initialization'
        
        # (a) Thread to run the BCI Module along with a Stopping Mini-GUI
        threading.Thread.__init__(self)        
        # (b) ***** Stopping Mini-GUI Design ***** 
        # --- window 
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Essex Virtual Environment: Brain Computer Interface')
        background = gtk.gdk.color_parse('#DCDCDC')
        window.modify_bg(gtk.STATE_NORMAL, background)
        window.set_border_width(7)
        window.set_resizable(False)
        window.connect('destroy', self.guiDESTROY)
        window.show()
        # --- table
        table = gtk.Table(12, 10, False)
        window.add(table)
        table.show()        
        # --- window characteristics
        titulo = Label('University of Essex - BCI Group', 'Neuropol 20', blue, 0, 0.5)
        table.attach(titulo, 0, 8, 0, 1)
        subtitulo = Label('A VE Plataform for Simulated BCI-Enabled Indenpendent Living\n', 'Neuropol 17', orange, 0, 0.5)
        table.attach(subtitulo, 0, 8, 1, 2)      
        logo = Image('Images\\minilogo.jpg')
        table.attach(logo, 8, 10, 0, 2)        
        # --- title 1: Offline Analysis Report
        icon = Image('Images\\off.png')
        icon.set_alignment(xalign=0, yalign=0.5)
        table.attach(icon, 0, 2, 2, 4)
        title = Label('OffLine Analysis Report', large_font, 'black', 0, 0.5)
        table.attach(title, 1, 10, 2, 4)  
        # --- submessage 1
        message1 = Label('', font, 'black', 0, 0.5)
        table.attach(message1, 1, 10, 4, 5)
        # --- submessage 2
        message2 = Label('', font, 'black', 0, 0.5)
        table.attach(message2, 1, 10, 5, 6)
        # --- submessage 3
        message3 = Label('', font, 'black', 0, 0.5)
        table.attach(message3, 1, 10, 6, 7)
        # --- title 2
        icon = Image('Images\\stop.png')
        icon.set_alignment(xalign=0, yalign=0.5)
        table.attach(icon, 0, 2, 7, 9)
        title = Label('The Data Process could take a long time to conclude', large_font, 'black', 0, 0.5)
        table.attach(title, 1, 10, 7, 9)   
        # --- title 3
        icon = Image('Images\\results.png')
        icon.set_alignment(xalign=0, yalign=0.5)
        table.attach(icon, 0, 2, 9, 11)
        title = Label('Final Results', large_font, 'black', 0, 0.5)
        table.attach(title, 1, 10, 9, 11) 
        # --- submessage 4
        message4 = Label('', font, 'black', 0, 0.5)
        table.attach(message4, 1, 10, 11, 12)           
        # (c) ***** Classifiers&Plots-Class Initialization *****
        CLASSp = Class_Plot(bci_output)          
        # (d) ***** Variable Assignment *****
        self.CLASSp   = CLASSp
        self.message1 = message1
        self.message2 = message2
        self.message3 = message3
        self.message4 = message4
        self.title    = title
        

    # ╦╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.2 - SystemControl ╦╦╦╦╦╦╦╦╦╦╦
    def run(self):
        'System Control'
        
        # ***** Variable Declaration *****
        # --- ending the OffLine Thread if the window is closed
        self.OffLine_Thread = True      
        # ***** EEG Signal Analysis *****
        # 1) signal conditioning
        gobject.idle_add(self.guiUPDATE, 1)        
        eeg_dsp = self.Off_SigCon()
        if not(self.OffLine_Thread): return
        # 2) feature extraction
        gobject.idle_add(self.guiUPDATE, 2)
        eeg_feaext, mean_feaext, min_feaext, max_feaext = self.Off_FeaExt(eeg_dsp)
        if not(self.OffLine_Thread): return
        # 3) feature selection
        gobject.idle_add(self.guiUPDATE, 3)
        selection_out, selection_labels  = self.Off_FeaSel(eeg_feaext)
        if not(self.OffLine_Thread): return
        # 4) feature classification
        gobject.idle_add(self.guiUPDATE, 4)
        class_out  = self.Off_Classification(eeg_feaext, selection_out)
        if not(self.OffLine_Thread): return
        # 5) plotting
        self.Off_Plots(eeg_dsp, eeg_feaext)
        if not(self.OffLine_Thread): return
        # ***** Saving Data *****        
        OFFLineAnalysis = (eeg_dsp, eeg_feaext, selection_out, selection_labels, class_out)   
        cPickle.dump(OFFLineAnalysis, open(root + 'OFFLineAnalysis.p', 'wb'))  
        ONLineAnalysis  = (mean_feaext, min_feaext, max_feaext, class_out['dataset1']['GridSearch_per_Run'])
        cPickle.dump(ONLineAnalysis, open(root + 'ONLineAnalysis.p', 'wb'))   
        if not(self.OffLine_Thread): return
        # ***** Final Report *****
        gobject.idle_add(self.guiUPDATE, 6)
        FinalReport(OFFLineAnalysis)
        if not(self.OffLine_Thread): return
        

    # ╦╦╦╦╦╦╦╦╦╦ Method 5.3.3 - Signal Conditioning ╦╦╦╦╦╦╦╦
    def Off_SigCon(self):
        'OffLine Signal Conditioning'

        # (a) ***** Data Unpacking *****        
        matrices      = bci_output[0][1]
        channels      = bci_output[0][2]
        samples       = bci_output[0][4]
        trials_train  = bci_output[0][5]
        trials_test   = bci_output[0][6]
        Fs            = bci_output[0][7]
        bad_electrodes= bci_output[0][10]
        Fdown         = bci_output[1][0]
        reference     = bci_output[1][1]
        ch_pos        = bci_output[1][2]
        Rej50         = bci_output[1][3]
        DCremove      = bci_output[1][4]
        BW            = bci_output[1][5]
        FeaExtractor  = bci_output[2][0]
        Class_Label   = bci_output[4][1]
        erds2D        = bci_output[5][4]
        erds3D        = bci_output[5][5]    
        # --- Idle-State availability
        if Class_Label[-1] != 0:
            Idle_ON = True
        else:
            Idle_ON = False
        self.Idle_ON = Idle_ON
        # --- reference matrix    
        if FeaExtractor == 'ERD/ERS':
            Ref_matrices = bci_output[2][1]        
        elif any([erds2D == 'on', erds3D == 'on']):
            Ref_matrices = bci_output[5][7][9]       
        # (b) ***** Data Selection ******
        # --- total used trials organization
        # {
        trials = []
        for index in range(len(trials_train)):
            # extracting all the required trials
            total_trials = []
            total_trials.extend(trials_train[index])
            total_trials.extend(trials_test[index])
            total_trials.sort()     
            # saving train+test trials
            trials.append(total_trials)
        # }
        # --- necessary default variables to class & plot methods
        eeg_ref, bsMAT_idxs, refMAT_idxs = [], range(len(matrices)), []
        # --- extraction of the raw matrices
        eeg_raw = []
        for index in range(len(matrices)):
            trial_idxs  = trials[index]
            sample_idxs = samples[index]          
            m = np.take(matrices[index], trial_idxs, axis = 1)
            m = np.take(m, sample_idxs, axis = 2)
            eeg_raw.append(m)
        # (c) ***** Parameters Declaration or Calculation *****
        # --- re-naming the selected channels
        new_chpos = range(len(ch_pos))
        # --- downsampling rate
        downsample_rate = Fs//Fdown
        # --- eeg_dsp: list of all the matrices
        eeg_dsp = []
        for index in range(len(matrices)):
            dimz = len(samples[index])//downsample_rate
            eeg_dsp.append(np.zeros((len(ch_pos),len(trials[index]),dimz)))         
        # --- new electrode layout
        LAYOUT = BS_layout(channels)        
        # (d) ***** Previous Digital Signal Processing Designs *****
        # --- highpass and lowpass Butterworth filter
        bandwidth = [BW[0], [0,0], [0,0]]
        if BW[0] == 'on': 
            bandwidth[1][0], bandwidth[1][1] = spectral_filter(Fdown, BW[1][0], 0, 4, 'highpass')   
            bandwidth[2][0], bandwidth[2][1] = spectral_filter(Fdown, 0, BW[1][1], 7, 'lowpass')                    
        # --- lowpass and highpass Butterworth filter
        bandrejection = [Rej50, [0,0]]
        if Rej50 == 'on': 
            bandrejection[1][0], bandrejection[1][1] = spectral_filter(Fdown, 48, 52, 2, 'bandstop')
        # --- DC removing (high pass filter)
        if DCremove == 'on': 
            DCband = ['on', (np.array([1, -1]), np.array([1, -0.9979]))]
        else:
            DCband = ['off', (0,0)]
        # (e) ***** Signal Conditioning *****         
        for index in range(len(eeg_raw)):
            # --- spectral filtering in order to avoid disturtion during the referencing procedure
            #     (applied to all the available channels) -- only if it's necessary
            if any([BW, Rej50, DCremove]):
                all_CHs = np.size(eeg_raw[index], axis = 0)
                for ch in range(all_CHs): 
                    # gui update
                    gobject.idle_add(self.guiSIGCON, 'Spectral - Brain State ', index, ch)
                    eeg_raw[index][ch,:,:] = SiGCoN(ch,eeg_raw[index],LAYOUT,reference,bandwidth,bandrejection,DCband,downsample_rate,'spectral',bad_electrodes)            
            # --- spatial filtering + downsampling (applied only to the required channels)
            channels_idx = zip(ch_pos, new_chpos)
            for ch, new_ch in channels_idx: 
                # gui update
                gobject.idle_add(self.guiSIGCON, 'Spatial - Brain State ', index, ch)
                eeg_dsp[index][new_ch,:,:] = SiGCoN(ch,eeg_raw[index],LAYOUT,reference,bandwidth,bandrejection,DCband,downsample_rate,'spatial',bad_electrodes)    
            # --- bad electrode replacement after all the digital processing
            if bad_electrodes != []:
                for electrode in bad_electrodes: 
                    replacement_idx = replace_electrodes(electrode, bad_electrodes, LAYOUT, ch_pos)   
                    # electrode label update
                    new_ch = np.setmember1d(np.array(ch_pos), np.array([electrode]))
                    new_ch = np.where(new_ch == True)          
                    # replacement for each trial
                    for tr in trials[index]: eeg_dsp[index][new_ch[0], tr, :] = np.mean(eeg_dsp[index][replacement_idx,tr,:], axis = 0)                       
        # (f) ***** Data distribution between brain states and reference matrices *****  
        if any([FeaExtractor == 'ERD/ERS', erds2D == 'on', erds3D == 'on']): 
            eeg_dsp, eeg_ref, bsMAT_idxs, refMAT_idxs =  BSref_Split(eeg_dsp, Ref_matrices)
        # (g) Variable Assignment
        self.eeg_ref = eeg_ref
        self.bsMAT_idxs = bsMAT_idxs
        self.refMAT_idxs = refMAT_idxs
        self.total_trials = trials
        return eeg_dsp


    # ╦╦╦╦╦╦╦╦╦ Method 5.3.4 - Feature Extraction ╦╦╦╦╦╦╦╦╦╦
    def Off_FeaExt(self, eeg_dsp):
        'OffLine Feature Extraction'

        # (a) ***** Data Unpacking *****
        SegLen       = bci_output[0][8]
        overlapping  = bci_output[0][9]
        Fdown        = bci_output[1][0]
        FeaExtractor = bci_output[2][0]
        StandardScore= bci_output[4][3]
        # (b) ***** Local Variables Declaration *****
        referencing = None
        # --- whole band coefficients
        whole_fL, whole_fH = [], []
        # --- number of samples per segment and per non-overlapping segment
        SegSamples, OverlapSamples = [], []
        for item in SegLen: 
            tempo = int(round(item * Fdown))
            SegSamples.append(tempo)
            OverlapSamples.append(((100 - overlapping) * tempo) // 100)
        # --- dimension of the eeg_dsp matrix & average values of features for online plot proposes
        eeg_feaext, dimX, dimY, dimZ, mean_feaext, min_feaext, max_feaext = [], [], [], [], [], [], []
        for index in range(len(eeg_dsp)):
            dimX.append(np.size(eeg_dsp[index], axis = 0))
            dimY.append(np.size(eeg_dsp[index], axis = 1))
            dimZ.append(np.size(eeg_dsp[index], axis = 2)) 
            mean_feaext.append(np.zeros(0))     
            max_feaext.append(np.zeros(0))
            min_feaext.append(np.zeros(0))                              
        # (c) ***** Previous Digital Signal Processing Designs *****
        # --  bandpass_filtering = [Ltheta, Utheta, Lalpha, Ualpha, Lbeta, Ubeta, gamma]
        bandpass_filtering = [[bci_output[2][2][0], [0,0], [0,0]],\
                              [bci_output[2][3][0], [0,0], [0,0]],\
                              [bci_output[2][4][0], [0,0], [0,0]],\
                              [bci_output[2][5][0], [0,0], [0,0]],\
                              [bci_output[2][6][0], [0,0], [0,0]],\
                              [bci_output[2][7][0], [0,0], [0,0]],\
                              [bci_output[2][8][0], [0,0], [0,0]],\
                              [bci_output[2][9][0], [0,0], [0,0]],\
                              [bci_output[2][10][0],[0,0], [0,0]],\
                              [bci_output[2][11][0],[0,0], [0,0]],\
                              ['off',               [0,0], [0,0]]] #whole band
        for index in range(len(bandpass_filtering)):
            if bandpass_filtering[index][0] == 'on':
                fL = bci_output[2][index+2][1][0]
                fH = bci_output[2][index+2][1][1]
                whole_fL.append(fL)
                whole_fH.append(fH)
                bandpass_filtering[index][1][0], bandpass_filtering[index][1][1] = spectral_filter(Fdown, fL,  0, 7, 'highpass')
                bandpass_filtering[index][2][0], bandpass_filtering[index][2][1] = spectral_filter(Fdown,  0, fH, 7,  'lowpass')                
        # -- absolute power including broadband and relative power: FILTER
        if any([FeaExtractor == 'relative', FeaExtractor == 'absolute_bb']):
            fL, fH = min(whole_fL), max(whole_fH)
            bandpass_filtering[10][1][0], bandpass_filtering[10][1][1] = spectral_filter(Fdown, fL,  0, 7, 'highpass')
            bandpass_filtering[10][2][0], bandpass_filtering[10][2][1] = spectral_filter(Fdown,  0, fH, 7, 'lowpass')
            if FeaExtractor == 'absolute_bb': bandpass_filtering[10][0] = 'on'        
        # (d) ***** Feature Extraction *****
        row = np.zeros(0)
        # --- Reference calculation for ERD/ERS mode
        if FeaExtractor == 'ERD/ERS': Reference = ERDSPower_REF(self.eeg_ref, bandpass_filtering)            
        # --- Band power calculation according to ABSOLUTE/RELATIVE/ERDS modes
        for index in range(len(eeg_dsp)):                
            for trial in range(dimY[index]):   
                ref_idx = -1            
                # BP estimates according to SEGMENTATION and for the selected channels                        
                for ch in range(dimX[index]):
                    for band in bandpass_filtering:                           
                        if band[0] == 'on':
                            ref_idx += 1     
                            if FeaExtractor == 'ERD/ERS': referencing = Reference[index][trial, ref_idx]                        
                            row = np.append(row, BandPower(FeaExtractor,eeg_dsp[index][ch, trial, :],band,bandpass_filtering,\
                                                 referencing,SegSamples[index],OverlapSamples[index],dimZ[index]))
                # -- Matrix creation according to the number of features
                if trial == 0: 
                    eeg_feaext.append(np.zeros((1, len(row))))
                    eeg_feaext[index][0, :] = row.copy()
                else:
                    row = np.reshape(row, (1, len(row)))
                    eeg_feaext[index] = np.append(eeg_feaext[index], row.copy(), axis = 0)                    
                # -- row reset                  
                row = np.zeros(0)  
                gobject.idle_add(self.guiFE, index, trial)    
            # (e) ***** Average values of Features for OnLine Analysis *****
            mean_feaext[index] = np.append(mean_feaext[index], np.average(eeg_feaext[index], axis = 0)) 
            min_feaext[index]  = np.append(min_feaext[index], np.min(eeg_feaext[index], axis = 0))
            max_feaext[index]  = np.append(max_feaext[index], np.max(eeg_feaext[index], axis = 0))           
        # (f) ***** Scaling data by mlpy.normalization --> [-1 1] *****
        #     ***** or by mlpy.standardization                    *****
        # --- Stardardization (it always requires 3 brain states)
        if all([self.Idle_ON, StandardScore]):
            tempo, eeg_feaext[0] = mlpy.data_standardize(eeg_feaext[2], eeg_feaext[0])
            eeg_feaext[2], eeg_feaext[1] = mlpy.data_standardize(eeg_feaext[2], eeg_feaext[1])
        # --- Normalization 
        else:
            for index in range(len(eeg_feaext)): eeg_feaext[index] = mlpy.data_normalize(eeg_feaext[index])           
        # (g) ***** Variable Assignment *****
        self.bandpass_filtering = bandpass_filtering     
        self.NOverlapSamples = OverlapSamples       
        return eeg_feaext, mean_feaext, min_feaext, max_feaext   


    # ╦╦╦╦╦╦╦╦╦ Method 5.3.5 - Feature Selection ╦╦╦╦╦╦╦╦╦╦╦
    def Off_FeaSel(self, eeg_feaext):
        'OffLine Feature Selection'

        # (a) ***** Data Unpacking *****
        DBI          = bci_output[3][0]
        RFE          = bci_output[3][1][0]
        ClassSel     = bci_output[3][1][1]
        sel_DBI      = bci_output[3][2][0]
        sel_RFE      = bci_output[3][3][0]
        # (b) ***** Variable Declaration *****        
        selection_out    = {'DBI':np.zeros(0), 'RFE':np.zeros(0)}   
        selection_labels = {'DBI':[], 'RFE':[]}
        if all([not(DBI),not(RFE),not(sel_DBI),not(sel_RFE)]): return selection_out, selection_labels        
        # (c) ***** David-Bouldin Index Method *****
        if DBI:
            # --- GUI update
            gobject.idle_add(self.guiSEL, 'David-Bouldin Index Method', 0)
            # --- DBI calculation (DBIlocs := location of the features organized in ascending order,\
            #                      DBIarray:= DBI values organized in ascending order)
            DBIlocs, DBIarray = DBI_Method(eeg_feaext)
            # --- saving the data into dictionary       
            selection_out['DBI'] = DBIlocs     
            selection_out.update({'DBIvalues': DBIarray})
            # c.4 DBI Labelling according to the channel, frequency band and time series
            selection_labels['DBI'] = self.CLASSp.Feature_Labels(self.NOverlapSamples[0],self.bandpass_filtering,selection_out['DBI'],self.bsMAT_idxs)              
        # (d) ***** Recursive Feature Elimination Method *****
        if RFE:
            gobject.idle_add(self.guiSEL, 'Recursive Feature Elimination', 0)            
            # d.1 Data Organization
            FEATURES, TARGETS = [], []
            # --- datasets of trials and targets in the case of idle availability
            if self.Idle_ON: 
                # variable declaration
                targets = np.zeros(0, dtype = int)
                MI_trials   = np.size(eeg_feaext[0], axis = 0) + np.size(eeg_feaext[1], axis = 0)
                idle_trials = np.size(eeg_feaext[2], axis = 0)
                # features for left+right+idle
                FEATURES.append(np.concatenate((eeg_feaext[0],eeg_feaext[1],eeg_feaext[2]), axis = 0))
                # targets for left+right
                targets = np.append(targets, np.repeat(1, MI_trials))
                # targets for idle
                targets = np.append(targets, np.repeat(-1,idle_trials))
                TARGETS.append(targets)
            # --- datasets of trials and targets for left + right
            # variable declaration            
            targets = np.zeros(0, dtype = int)
            left_trials  = np.size(eeg_feaext[0], axis = 0)
            right_trials = np.size(eeg_feaext[1], axis = 0)
            # features for left+right
            FEATURES.append(np.concatenate((eeg_feaext[0],eeg_feaext[1]), axis = 0))
            # targets for left
            targets = np.append(targets, np.repeat(1, left_trials))
            # targets for right
            targets = np.append(targets, np.repeat(-1, right_trials))
            TARGETS.append(targets) 
            # d.2 Mixing the trials of feature-sets and target-sets
            for index in range(len(FEATURES)):            
                features, targets = FEATURES[index], TARGETS[index]
                # --- random integer list creation
                indices, rand_indices = range(len(targets)), []
                while indices != []:
                    idx = rd.choice(indices)
                    rand_indices.append(idx)
                    indices.remove(idx)
                # --- reset the organization of the datasets
                FEATURES[index], TARGETS[index] = features[rand_indices,:], targets[rand_indices,:]  
            # d.3 Ranking the Features
            for index in range(len(FEATURES)):   
                features, targets = FEATURES[index], TARGETS[index]
                # --- initialize ranking class
                rank = mlpy.Ranking()
                # --- implementing feature weighting method
                if ClassSel == 'FDA':
                    weighting = mlpy.Fda()
                elif ClassSel == 'Linear_SVM':
                    weighting = mlpy.Svm()
                elif ClassSel == 'RBF_SVM':
                    weighting = mlpy.Svm(kernel = 'gaussian')
                # --- GUI update
                gobject.idle_add(self.guiSEL, 'Recursive Feature Elimination', index+1)
                # --- computing feature ranking
                ranked_features = rank.compute(features, targets, weighting, debug = True)
                # --- saving data 
                selection_out['RFE'] = np.append(selection_out['RFE'], ranked_features)
            # d.4 DBI Labelling according to the channel, frequency band and time series
            selection_labels['RFE'] = self.CLASSp.Feature_Labels(self.NOverlapSamples[0],self.bandpass_filtering,selection_out['RFE'],self.bsMAT_idxs)     
        return selection_out, selection_labels
  

    # ╦╦╦╦╦╦╦ Method 5.3.6 - OffLine Classification ╦╦╦╦╦╦╦╦
    def Off_Classification(self, eeg_feaext, selection_out):
        'OffLine EEG Data Analysis'

        # (a) ***** Data Unpacking *****
        trials_train = bci_output[0][5]
        trials_test  = bci_output[0][6]                
        # (b) ***** DatA PreprocessinG *****
        # b.1 General Variable Declaration
        # --- finding the new locations of the train/test trials after the previous processing
        new_trials_train, new_trials_test = [], []
        for index in self.bsMAT_idxs:
            new_trials_train.append(np.searchsorted(self.total_trials[index], trials_train[index]))
            new_trials_test.append(np.searchsorted(self.total_trials[index], trials_test[index]))          
        # --- data storage for consecutive iteration 
        #     (i.e., several runs to find the optimum number of features)
        class_out = {}
        # --- number of features
        numfea = np.size(eeg_feaext[0],axis=1)
        # --- feature-indices used to classify
        FEATURE_IDX, Range, Step = self.CLASSp.Organization_Features(selection_out, numfea) 
        # b.2 Dataset Construction for Classification Process
        self.CLASSp.Datasets(eeg_feaext, new_trials_train, new_trials_test)
        # ~~~~~~~~~ Re-Adjustment of the DATASET & Process Repeatability ~~~~~~~
        DataSet, prev_step, gamma = 0, 0, None
        while True:
            DataSet += 1
            # ------------ Classification Process for One DATASET --------------       
            GridSearch, Accuracy, Predictions, Gral_Acc, RUN = [], [], [], [], 0
            for feature_indices in FEATURE_IDX:  
                RUN += 1  
                # (c) ***** Classfier Creation *****
                # --- the classifier design is per couple of BS
                MODELS,GRID_SEARCH,ACCURACY,PREDICTIONS = self.CLASSp.Classifier_Creator(feature_indices)
                # (d) ***** Evaluation for reaching an unique accuracy *****
                ACC = self.CLASSp.Tree_Evaluation(MODELS, feature_indices)
                # (e) *****  Saving the Outcomes of One Run *****
                # --- GRID_SEARCH = [[bestparameters_C1, accuracy_C1],[bestparameters_C2, accuracy_C2]]   
                # --- GridSearch  = [GRID_SEARCH_Run1, GRID_SEARCH_Run2,..., GRID_SEARCH_RunM] 
                # --- ACCURACY    = testing hits for the current run
                # --- Accuracy    = [accuracy_Run1, accuracy_Run2,..., accuracy_RunM]
                # --- PREDICTIONS = predicted labels during testing   
                # --- Predictions = [predictions_Run1, predictions_Run2,..., predictions_RunM]
                GridSearch.append(GRID_SEARCH)
                Accuracy.append(ACCURACY)
                Predictions.append(PREDICTIONS)   
                Gral_Acc.append(ACC)            
                # (f) ***** GUI update *****
                gobject.idle_add(self.guiCLASS, DataSet, RUN, ACC)            
            # (g) ***** Saving Final Results for the current Run *****  
            key = 'dataset' + str(DataSet)
            class_out.update({key:{}})
            class_out[key].update({'GridSearch_per_Run': GridSearch})
            class_out[key].update({'Accuracy_per_Run': Accuracy})
            class_out[key].update({'GralACC_per_Run': Gral_Acc})
            class_out[key].update({'Predictions_per_Run': Predictions})
            class_out[key].update({'RunStep_RunEnd': [Step, Range[-1]]})
            # ------------------------------------------------------------------
            # (h) ***** Re-Selection of the Feature Dataset *****  
            # --- extracting the best run by its accuracy
            idx_max_acc = Gral_Acc.index(max(Gral_Acc))   
            selection_out_tempo = np.array(FEATURE_IDX[idx_max_acc], dtype = int)
            class_out[key].update({'BestRun_acc&feas': (max(Gral_Acc), selection_out_tempo)})
            # --- only ONE dataset available
            if Step <= 1: break
            # --- SEVERAL dataset: slicing the current dataset according to the best current performance
            else:
                # 1- obtaining the step value according to the 5% of the total samples
                while Step > 1:      
                    prev_step, stop = Step, len(selection_out_tempo[0])
                    start, Step = 0, int(np.ceil((5 * stop)/100)) 
                    if prev_step != Step: break      
                    Gral_Acc[idx_max_acc] = Gral_Acc[idx_max_acc] * -1    
                    idx_max_acc = Gral_Acc.index(max(Gral_Acc))
                    selection_out_tempo = np.array(FEATURE_IDX[idx_max_acc], dtype = int)                           
                # 2- range values    
                Range = range(0, stop, Step)    
                Range.append(Range[-1]+Step) 
                # 3- resetting values to start a new dataset process                        
                FEATURE_IDX, feature_indices = [], []                                              
                for end in Range[1:]:
                    # three classes
                    if self.Idle_ON: 
                        indices = selection_out_tempo[0][start:end].tolist()
                        feature_indices.append(indices)
                        indices = selection_out_tempo[1][start:end].tolist()
                        feature_indices.append(indices)
                    # two classes
                    else:
                        indices = selection_out_tempo[0][start:end].tolist()
                        feature_indices.append(indices)                        
                    FEATURE_IDX.append(feature_indices)   
                    feature_indices = []                                
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # (i) ***** Variable Assignment *****
        self.feature_indices = selection_out_tempo
        return class_out      
     

    # ╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.7 - OffLine Plotting ╦╦╦╦╦╦╦╦╦╦
    def Off_Plots(self,eeg_dsp,eeg_feaext):
        'OffLine EEG Data Analysis'

        
        # (a) ***** Data Unpacking *****        
        samples_daq   = bci_output[0][4]
        Fs            = bci_output[0][7]
        Fdown         = bci_output[1][0]
        ch_pos        = bci_output[1][2]               
        spectrogram   = bci_output[5][0]
        psd           = bci_output[5][1]
        boxplot       = bci_output[5][2]
        histogram     = bci_output[5][3]
        erds2D        = bci_output[5][4]
        erds3D        = bci_output[5][5]           
        labels_ch     = bci_output[5][7][1]
        trials        = bci_output[5][7][2]
        samples_plot  = bci_output[5][7][3]                     
        # (b) ***** Default Operations *****
        # --- get out if there are not selected plots
        if all([spectrogram=='off',psd=='off',boxplot=='off',histogram=='off',erds2D=='off',erds3D=='off']): return          
        # --- GUI update
        gobject.idle_add(self.guiUPDATE, 5)
        # (c) ***** Declaration of Local Variables *****
        # --- channels and samples in use
        if any([spectrogram=='on',psd=='on',erds2D=='on',erds3D=='on']):   
            # --- trial re-assignment (only for brain-states, i.e., bsMAT_idxs)
            new_trials = []
            for index in self.bsMAT_idxs: new_trials.append(np.searchsorted(self.total_trials[index], trials[index]))     
            # --- channels in use
            if labels_ch != 'off':
                channels = []
                for ch in labels_ch: channels.append(ch_pos.index(ch))                            
            # --- sample re-assignment (only for brain-states, i.e., bsMAT_idxs)
            new_samples = []
            for index in self.bsMAT_idxs:
                # sample-case
                new_samples.append(np.searchsorted(samples_daq[index], samples_plot[index]))
                time = np.array(new_samples[-1])/Fs
                new_samples[-1] = np.unique1d(np.array(time*Fdown, dtype = int))                 
        # --- feature organization according to feature selection
        if any([boxplot == 'on', histogram == 'on']):
            tempo = cp.copy(eeg_feaext)
            eeg_feaext = []
            if self.Idle_ON:
                # left + right for the Classifier 1
                eeg_feaext.append(np.concatenate((tempo[0][:,self.feature_indices[0]], tempo[1][:,self.feature_indices[0]]), axis = 0))
                # idle for the Classifier 1
                eeg_feaext.append(tempo[2][:,self.feature_indices[0]])
                # left for the Classifier 2
                eeg_feaext.append(tempo[0][:,self.feature_indices[1]])
                # right for the Classifier 2
                eeg_feaext.append(tempo[1][:,self.feature_indices[1]])
                feaext_labels = ['LEFT & RIGHT Imaginary Movements','IDLE Brain State','LEFT Imaginary Movement','RIGHT Imaginary Movement']
            else:
                # left for the Classifier 2
                eeg_feaext.append(tempo[0][:,self.feature_indices[0]])
                # right for the Classifier 2
                eeg_feaext.append(tempo[1][:,self.feature_indices[0]])   
                feaext_labels = ['LEFT Imaginary Movement','RIGHT Imaginary Movement'] 
        # --- only for 2D & 3D Plot cases
        if any([erds2D == 'on', erds3D == 'on']): 
            # 1- selected eeg bands
            current_bands, greek_bd = [], []
            Bands = ['Theta','LowerTheta','UpperTheta','Alpha','LowerAlpha','UpperAlpha',\
                     'Beta','LowerBeta','UpperBeta','Gamma','Whole']
            greek_Bds = [r'$\theta$', r'$\theta_L$', r'$\theta_U$', r'$\alpha$', r'$\alpha_L$', r'$\alpha_U$',\
                         r'$\beta$',  r'$\beta_L$',  r'$\beta_U$',  r'$\gamma$', r'$\sqcup$']
            for index in range(len(Bands)): 
                if self.bandpass_filtering[index][0] == 'on': 
                    current_bands.append(Bands[index])
                    greek_bd.append(greek_Bds[index])           
            # 2- sample/trial re-assignment (only for reference-states, i.e., refMAT_idxs)
            ref_samples, ref_trials = [], []
            for item in self.eeg_ref:
                # sample-case
                ref_samples.append(np.arange(np.size(item, axis = 2)))
                # trial-case
                ref_trials.append(np.arange(np.size(item, axis = 1)))             
            # 3- processing for all the Brain States            
            Power_ERDS    = ERDS_PreProcessing(eeg_dsp, new_samples, new_trials, self.bandpass_filtering, channels)
            Power_ERDSref = ERDS_PreProcessing(self.eeg_ref, ref_samples, ref_trials, self.bandpass_filtering, channels)
            # 4- calculation of average power in the reference interval
            Reference = []
            for item in Power_ERDSref: Reference.append(np.average(item, axis = 2))       
        # (d) ***** Spectrogram *****
        if spectrogram == 'on': FIG1 = self.CLASSp.Spectrogram(eeg_dsp, channels, new_trials, new_samples)       
        # (e) ***** PSD (Power Spectral Density) *****
        if psd == 'on': FIG2 = self.CLASSp.PSD(eeg_dsp, channels, new_trials, new_samples)             
        # (f) ***** BoxPlot (plotting the features) *****
        if boxplot == 'on': FIG3 = self.CLASSp.BoxPlot(eeg_feaext, feaext_labels)                       
        # (g) ***** Histogram (feature distribution) *****
        if histogram == 'on': FIG4 = self.CLASSp.Histogram(eeg_feaext, feaext_labels)                   
        # (h) ***** ERD/ERS Maps (2D) *****
        if erds2D == 'on': FIG5 = self.CLASSp.ERDS2d(channels, Power_ERDS, Reference, current_bands, greek_bd)            
        # (i) ***** ERD/ERS Maps (3D) *****
        if erds3D == 'on': FIG6 = self.CLASSp.ERDS3d(channels, Power_ERDS, Reference, current_bands)
        # (j) ***** Graph Display  *****            
        plt.show()


    # ╦╦╦╦╦╦╦╦╦ Method 5.3.8 - Killing essexVE_BCI ╦╦╦╦╦╦╦╦╦
    def guiDESTROY(self, widget):
        'Exiting from the GUI of the System'
        
        # --- end the OffLine thread
        self.OffLine_Thread = False
        # --- end the main thread (i.e., the gui thread)
        gtk.main_quit()
        
    
    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.9 - MiniGUI Update ╦╦╦╦╦╦╦╦╦╦╦
    def guiUPDATE(self, stage):
        'Mini Graphical User Interface Update'
        
        if stage == 1:
            self.message1.set_text('>>> The BCI system is conditioning the EEG Signals.')
        elif stage == 2:            
            self.message1.set_text('>>> The BCI system is extracting the Features.')
        elif stage == 3:          
            self.message1.set_text('>>> The BCI system is ranking the Features.')
        elif stage == 4:
            self.message1.set_text('>>> The BCI system is training the Classifier.')
        elif stage == 5:
            self.message1.set_text('>>> The BCI system is plotting the selected Modes.')
            self.message2.set_text('')
            self.message3.set_text('')            
        elif stage == 6:            
            self.title.set_text('Final Results: OffLineAnalysis.p')
            self.message4.set_text('>>> OffLineAnalysis = (eeg_dsp,eeg_feaext,selection_out,selection_labels,class_out).')           


    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.10 - MiniGUI Update ╦╦╦╦╦╦╦╦╦╦
    def guiSIGCON(self, mode, current_BS, current_ch):
        'Mini Graphical User Interface Update --> Feature Extraction'
        
        self.message2.set_text('>>> Conditioning Mode: ' + mode + str(current_BS+1))
        self.message3.set_text('>>> Channel Number: ' + str(current_ch))

            
    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.11 - MiniGUI Update ╦╦╦╦╦╦╦╦╦╦
    def guiFE(self, index, trial):
        'Mini Graphical User Interface Update --> Feature Extraction'
        
        self.message2.set_text('>>> Brain State: ' + str(int(index+1)))
        self.message3.set_text('>>> Trial Number: ' + str(int(trial+1)))
    
    
    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.12 - MiniGUI Update ╦╦╦╦╦╦╦╦╦╦
    def guiSEL(self, selector, RUN):
        'Mini Graphical User Interface Update --> Feature Selection'
        
        self.message2.set_text('>>> Method of Selection: ' + selector)
        self.message3.set_text('>>> Dataset Number: ' + str(RUN))
        

    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method 5.3.13 - MiniGUI Update ╦╦╦╦╦╦╦╦╦╦
    def guiCLASS(self, DataSet, RUN, accuracy):
        'Mini Graphical User Interface Update --> Classifier'
        
        self.message2.set_text('>>> Dataset Number: ' + str(DataSet) + ', Run Number: ' + str(RUN))
        self.message3.set_text('>>> Classification Accuracy = ' + str(accuracy))
        
# ==========================================================
# |6| MAIN BODY - Main Calling Process
# ==========================================================
if __name__ == "__main__":

    # >>>>>>>>>Programmer's Configuration via a GUI<<<<<<<<<
    InitialReport()
    BCI_gui()
    gtk.main() 
    # ------------------------------------------------------
    # (A) None System Selection
    if bci_output == []:
        print '... the system has been aborted.'
    # ------------------------------------------------------    
    # (B) ONLine System
    elif bci_output[0][0] == 'online':
        # --- Initialization of the Threads
        gobject.threads_init()
        OnLine = essexVE_OnLineBCI()
        # --- starting essexVE_OnLine class
        OnLine.start()       
        gtk.main()        
    # ------------------------------------------------------
    # (C) OFFLine System
    elif bci_output[0][0] == 'offline':
        gobject.threads_init()
        OffLine = essexVE_OffLineBCI()
        # --- starting essexVE_OffLine class
        OffLine.start()
        # --- starting stopping MiniGUI
        gtk.main()
    
    
# ==========================================================
# |7| NOTES
# ==========================================================
# 1 - This program has exactly the same configuration for the
#     Online and the Offline modules.
# 2 - The filtering process is performed on entire signal,
#     it means that it doesn't consider the fragmentation of 
#     the signals (in signal conditioning & feature extraction)
# 3 - The code cannot be cut off in other files because of 
#     the dependency among varibles (e.g., bci_output, gui
#     monitoring).
# 4 - From this file is extracted the first flowchart 