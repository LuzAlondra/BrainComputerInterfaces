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
import numpy as np
import random as rd
import scipy as sp
from scipy import io, fftpack, signal
from socket import *
import sys
# --- 2D/3D Plot Libraries
import matplotlib
matplotlib.use('TKAgg')
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
from guiDATA_Converter import daq_error,sigcon_error,feaext_error,feasel_error,\
                              class_error,plots_error

# 2.4 LMAV fuctions for Digital Signal Processing
from DSP_Functions import spectral_filter,bits_float,replace_refIDX,replace_electrodes,\
                          SiGCoN, ERDS_PreProcessing, ERDSPower_REF, WinLibrary

# 2.5 LMAV function for Feature Treatment
from Patterns_Functions import DBI_Method,BandPower

# 2.6 LMAV class for Classification Treatments
from CLASSIFIERS import ClassPlot

# 2.7 LMAV functions for Experiment2 Proposes
from EXP2_Functions import Session1_Tracks, Session23_Tracks, Session23_CueTarget,\
                           Achieved_Targets, Initialization_CueDriven


# ==========================================================
# |3| GLOBAL CONSTANT DECLARATION
# ==========================================================
# ---- BCI gui Output & Online System Stages
bci_output = []
current_stage = '1.1 MI-Training'
# ---- gui Constants
ground = '#000000'
tab_bg = '#DCDCDC'
white = '#FFFFFF'
lblue = '#A0AEC1'
blue = '#466289'
orange = '#FA6121'
small_font = 'Georgia 10'
font = 'Tahoma 13.5'
large_font = 'Tahoma 16'



# ==========================================================
# |4| FUNCTION
# ==========================================================
def destroy(widget):
    gtk.main_quit()
    return False


# ==========================================================
# |5| WINDOW DESIGN
# ==========================================================
# --- window 
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_title('Essex Virtual Environment: Brain Computer Interface')
background = gtk.gdk.color_parse('#DCDCDC')
window.modify_bg(gtk.STATE_NORMAL, background)
window.set_border_width(10)
window.connect('destroy', destroy)
window.show()
# --- table
table = gtk.Table(20, 10, False)
window.add(table)
table.show()
# --- window characteristics
titulo = Label('University of Essex - BCI Group', 'Neuropol 20', blue, 0, 0.5)
table.attach(titulo, 0, 8, 0, 1)
subtitulo = Label('VE Plataform for Simulated BCI-Enabled Indenpendent Living', 'Neuropol 17', orange, 0, 0.5)
table.attach(subtitulo, 0, 8, 1, 2)        
logo = Image('Images\\minilogo.jpg')     
logo.set_alignment(xalign = 1, yalign = 0.5)   
table.attach(logo, 7, 10, 0, 2)     
# --- title 1: Online Analysis Report
logo = Image('Images\\on.png')
logo.set_alignment(xalign = 0, yalign = 0.5)
table.attach(logo, 0, 2, 2, 4)
title = Label('Online Analysis Report', large_font, 'black', 0, 0.5)
title.set_size_request(500, 35)
table.attach(title, 1, 10, 2, 4)               
message1 = Label('>>> Welcome to Essex MI-Based BCI', font, 'black', 0, 0.5)
message1.set_size_request(500, 35)
table.attach(message1, 1, 10, 4, 5)
message2 = Label('>>> Welcome to Essex MI-Based BCI', font, 'black', 0, 0.5)
message2.set_size_request(500, 35)
table.attach(message2, 1, 10, 5, 6)
# --- title 2: System Interruption
logo = Image('Images\\interrupt.png')
logo.set_alignment(xalign = 0, yalign = 0.5)
table.attach(logo, 0, 2, 6, 8)
title = Label('Interrupt the System Operation by closing the Window', large_font, 'black', 0, 0.5)
title.set_size_request(500, 35)
table.attach(title, 1, 10, 6, 8)         
# --- title 3: Features Plotting
logo = Image('Images\\graph.png')
logo.set_alignment(xalign = 0, yalign = 0.5)
table.attach(logo, 0, 2, 8, 10)
title = Label('2D Plot - BP Estimates Vs Features per Pattern', large_font, 'black', 0, 0.5)
title.set_size_request(500, 35)
table.attach(title, 1, 10, 8, 10) 

p = Image('C:\\Documents and Settings\\lmalon\\Desktop\\features.png')
table.attach(p, 0, 10, 10, 20)
#p.hide()


gtk.main()