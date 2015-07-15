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
## February 2nd, 2011

## .........................................................
## ........... BRAIN COMPUTER INTERFACE DESIGN: ............
## ............... Motor Imaginary Training ................
## .........................................................

# ==========================================================
# |1| SEQUENCE DESCRIPTION
# ==========================================================
#
# 1.1 MI Training Design
# --- One session = 4 runs
# --- One run = 30 trials
#               15 trials for left motor imaginary movement
#               15 trials for right motor imaginary movement
# a)  trigger 1 (start)
# b)  warning signal (stood man)        
# c)  beep
# d)  trigger 2 --> cue onset
# e)  trigger 3 --> left cue
#     trigger 4 --> right cue
# f)  mental task performance (pointing man)
# g)  trigger 5 (end)
# h)  break time (1 second)
# i)  no control signal extraction (2 seconds)
# j)  random intertrial gap (from 0 upto 1 second)
# --- 120 trials in total and 60 trials per class
# --- 30 trials for training and 30 trials for testing
#
# 1.2 Conversion from BDF File to 3D matrices data (.mat)


# ==========================================================
# |2| MODULES IMPORTING
# ==========================================================
#
# 2.1 PythonXY modules
from __future__ import division
from ctypes import windll
import datetime
import pygtk
pygtk.require('2.0')
import sys
import gtk
import gobject
import threading
import time
import winsound
import numpy as np
import random as rd
import scipy as sp
from scipy import io
#
# 2.2 LMAV classes for PythonXY
from Constructors_gui import Image, Label
#
# 2.3 PluG-Ins
sys.path.append('C:/Python25/Lib/site-packages/biosig4python')
from biosig import *


# ==========================================================
# |3| GLOBAL CONSTANT DECLARATION
# ==========================================================
#
# 3.1 MI Training Design
Fs = 512
experiment = 'interrupted'
# --- number of runs per session
num_runs = 4
# --- number of left mov trials
left_tr = 15
# --- number of right mov trials
right_tr = 15
# --- number of recorded channels
recorded_ch = 64
# --- number of used channels
used_ch = 64
orange = '#FA6121'
light_orange = '#FABF8F'
#
# 3.2 Timing Paradigm
# --- beep (200 ms/44.1kHz/1kbps)
beep = 'Sounds\\Cue.wav'
#
# 3.3 Trigger SetUp
pdll = windll.inpout32
# --- parallel port data register
datareg = 0x378
# --- parallel port clean-up
pdll.Out32(datareg, 0)
#
# 3.4 BDF File Converter
# a).-BDF reader
# --- default directory storage
url = 'C:\\Documents and Settings\\Lucy\\Escritorio\\Testdata.bdf'
# --- "blocks" is the number of blocks to read
# --- -1 to read all blocks until the end
blocks = -1
# --- "start" is the block to begin reading with
start = 0
# --- default output directory
FILENAME = ['C:\\Documents and Settings\\Lucy\\Escritorio\\Pre-MI.mat',\
            'C:\\Documents and Settings\\Lucy\\Escritorio\\MI_left.mat',\
            'C:\\Documents and Settings\\Lucy\\Escritorio\\MI_right.mat',\
            'C:\\Documents and Settings\\Lucy\\Escritorio\\Post-MI.mat']


# ==========================================================
# |4| FUNCTION DECLARATION
# ==========================================================
#
# 4.1 Trigger Search into BDF-files
def SearchTrig(target, triggers):
    'Trigger Search into BDF-files'

    pointer = 1
    result  = []
    SelTrig = np.where(triggers == target)
    result.append(SelTrig[0][0])
    for item in SelTrig[0][1:]:
        if item-pointer != result[len(result)-1]:
            result.append(item)
            pointer = 1
        else:
            pointer += 1
    return result
#
# 4.2 BDF-Files to 3D Matrix
def BDF2Matrix(markers, filename, Data):
    'BDF-file to mat-file'

    # --- 64 default channels 
    channels = range(0, used_ch)
    # --- extracted samples as trials
    if len(markers) == num_runs * left_tr:
        # Fs * 4 seconds --> control commands
        samples_start, samples_end = 0, Fs * 4        
    else:
        # Fs * 2 seconds --> Pre-MI Performance
        if filename == 'Pre-MI':
            samples_start, samples_end = 0, Fs * 2
        else:
        # Fs * 3 seconds --> Post-MI Performance
            samples_start, samples_end = 0, Fs * 3            
    # --- matrix creation
    matrix = np.zeros((len(channels), len(markers), samples_end))
    index = 0
    for trigger in markers:
        if (trigger+samples_end) > np.size(Data, 0): 
            M = matrix[:, :index, :]  
            sp.io.savemat(filename, mdict = {'array': M})   
            return
        matrix[:,index,:] = np.transpose(Data[trigger+samples_start:trigger+samples_end, channels])
        index += 1
    sp.io.savemat(filename, mdict = {'array': matrix})

# 4.3 Final Report
def FinalReport_start():
    'MI Training Report'

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
    print '.................... BRAIN COMPUTER INTERFACE DESIGN: .......................'
    print '................... MOTOR IMAGINARY MOVEMENTS TRAINING ......................'
    print '.............................................................................'
    print '\n\n\n'
    print '============================================================================='
    print 'OFFLine EEG Signal Analysis                                                  '
    print '============================================================================='
    print '\n'
    print '''1.- Before starting the training session, open an BDF-file and save it as 'Testdata.bdf'.\n'''
    print '2.- When the training session has been terminated, stop the Actiview program \n in order to start the BDF-file conversion to MAT-file data.\n'
    
def FinalReport_concluded():
    'MI Training Report'
    
    print '\n'
    print '3.- Output: Pre-MI.mat, MI_left.mat, MI_right.mat, Post-MI.mat'
    print '\n'
    print '4.- Default Directory: C:\\Documents and Settings\\Lucy\\Escritorio'
    print '\n'
    print 'Starting the conversion from BDF-file to mat-file . . .'

def FinalReport_interrupted():
    'MI Training Report'
    
    print '\n'
    print 'The Session has been interrupted.'

def FinalReport_end():
    'MI Training Report'

    print '. . . the matrices are ready in the default directory.'
            
    
# ==========================================================
# |5| CLASS DECLARATION - BCI Motor Imaginary Training
# ==========================================================
#
class MITraining(threading.Thread):
    'Class to control motor imaginary movements training session'

    #:::::::::::::  Method A - Initialization  :::::::::::::
    def __init__(self):
        'Interface Creation'

        threading.Thread.__init__(self)
        # (1) WINDOW 
        ## -- window creation
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("ESSEX Virtual Environment: Motor Imaginary Movements Training")
        background = gtk.gdk.color_parse('white')
        self.window.modify_bg(gtk.STATE_NORMAL, background)
        ## -- window events connection
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.window.show()

        # (2) TABLE - Widget container
        table = gtk.Table(9, 3, False)
        table.show()
        self.window.add(table)

        # (3) PRESENTATION
        # --- Title
        self.Title = []
        msg = '    BRAIN  COMPUTER  INTERFACE  DESIGN\n     Motor Imaginary Movements Training\n'
        self.Title.append(Label(msg, 'Neuropol 20', '#466289', 0, 0.5))
        table.attach(self.Title[0], 0, 2, 0, 2)
        self.Title.append(Image('Images\\essex_bcis_logo.jpg'))
        # --- Instructions
        self.Instructions = []
        self.Instructions.append(Label(' 1.- Session Structure\n', 'Tahoma 18', 'black', 0, 0.5))
        table.attach(self.Instructions[0], 0, 3, 2, 3)
        self.Instructions.append(Image('Images\\instructions.png'))
        table.attach(self.Instructions[1], 0, 3, 3, 4)
        self.Instructions.append(Label('\n 2.- Instructions', 'Tahoma 18', 'black', 0, 0.5))
        table.attach(self.Instructions[2], 0, 3, 4, 5)
        self.Instructions.append(Label('STOP', 'Tahoma 24', 'red', 0.5, 0.5))
        table.attach(self.Instructions[3], 0, 1, 5, 6)
        self.Instructions.append(Label('GET READY', 'Tahoma 24', 'yellow', 0.5, 0.5))
        table.attach(self.Instructions[4], 0, 1, 6, 7)
        self.Instructions.append(Label('GO', 'Tahoma 24', 'green', 0.5, 0.5))
        table.attach(self.Instructions[5], 0, 1, 7, 8)
        self.Instructions.append(Image('Images\\inst_blank.gif'))
        table.attach(self.Instructions[6], 1, 2, 5, 6)
        self.Instructions.append(Image('Images\\inst_stop.gif'))
        table.attach(self.Instructions[7], 1, 2, 6, 7)
        self.Instructions.append(Image('Images\\inst_left.gif'))
        table.attach(self.Instructions[8], 1, 2, 7, 8)
        msg = 'Stop doing any mental task and\ntry to move, blink, or yawn during\nthis period.'
        self.Instructions.append(Label(msg, 'Tahoma 18', 'black', 0, 0.5))
        table.attach(self.Instructions[9], 2, 3, 5, 6)
        msg = 'Get ready to perform a mental\ntask according to the following cue.'
        self.Instructions.append(Label(msg, 'Tahoma 18', 'black', 0, 0.5))
        table.attach(self.Instructions[10], 2, 3, 6, 7)
        msg = 'Imagine the movement of your\nleft/right hand, for example:'
        self.Instructions.append(Label(msg, 'Tahoma 18', 'black', 0, 0.5))
        table.attach(self.Instructions[11], 2, 3, 7, 8)
        self.Instructions.append(Image('Images\\hands.jpg'))
        table.attach(self.Instructions[12], 1, 3, 8, 9)

        # (4) CUE Images and ON/OFF Event_Box
        self.mental_task = [Image('Images\\stop.gif'), Image('Images\\blank.png'), \
                            Image('Images\\left.gif'), Image('Images\\right.gif')]
        ## -- event box
        self.event_box = gtk.EventBox()
        STYLE = self.event_box.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.event_box.get_colormap().alloc_color('#FFFFFF')
        self.event_box.set_style(STYLE)
        self.event_box.add(self.Title[1])
        self.event_box.connect('button_press_event', self.Control)
        self.event_box.show()
        table.attach(self.event_box, 2, 3, 0, 2)        

        # (5) Control Signals
        ## -- on/off system signal
        self.ON = True
        ## -- one run performance signal
        self.OneRun = False
        ## -- number of current runs
        self.runs = 0

    #:::::::::::::::: Method B: Killing GUI ::::::::::::::::
    def delete_event(self, widget, event, data = None):
        self.OneRun = False
        gtk.main_quit()
        return False

    def destroy(self,widget,data = None):
        self.OneRun = False
        gtk.main_quit()

    #:::::::::::: Method C: Stimuli Control ::::::::::::::::
    def Control(self, widget, event):
        'Stimulation Control'

        # (1) ON Stimuli
        if self.ON == True:
            if self.runs == 0:
                self.ON = False
                self.OneRun = True
                self.current = self.Title[1]
                for widget in self.Title: widget.hide()
                for widget in self.Instructions: widget.hide()
                self.event_box.set_border_width(250)
                self.window.fullscreen()
            else:
                self.ON = False            

        # (2) OFF Stimuli
        else:
            # -- break time setup
            self.window.unfullscreen()
            self.OneRun = False
            
    #:::::::::::: Method D: One Run Control ::::::::::::::::
    def run(self):
        'One Session Control'

        while self.runs < num_runs:
            # I. Session Control
            # -- hanging the thread until a user's signal is sent
            #    by a mouse click
            while self.ON: None
            # -- start saving continuos eeg data (PauseOff)
            pdll.Out32(datareg, 10)
            time.sleep(1)
            pdll.Out32(datareg, 0)
            time.sleep(1)
            # (1) Run Setup
            trials = [3, 4] * (left_tr + right_tr) 
            # (2) Run Performance
            while all([self.OneRun, trials != []]):
                # Warning Signal
                # *writing trigger 1 --> 1/Fs sec
                pdll.Out32(datareg, 1)
                time.sleep(0.002)
                pdll.Out32(datareg, 0)
                # *warning --> 2 sec
                gobject.idle_add(self.Warning)
                time.sleep(1.998)
                # Cue Onset
                # *writing trigger 2 --> 1/Fs sec
                pdll.Out32(datareg, 2)
                time.sleep(0.002)
                pdll.Out32(datareg, 0)
                # *beep --> 200ms
                winsound.PlaySound(beep, winsound.SND_FILENAME)
                # *cue onset 
                tr = rd.choice(trials)
                trials.remove(tr)
                gobject.idle_add(self.CueOnset, tr)  
                time.sleep(0.998)              
                # MI Performance                
                # *writing trigger 3,4 --> 1/Fs sec
                pdll.Out32(datareg, tr)
                time.sleep(0.002)
                pdll.Out32(datareg, 0)
                time.sleep(3.998)
                # Break Period
                # writing trigger 5 --> 1/Fs sec
                pdll.Out32(datareg, 5)
                time.sleep(0.002)
                pdll.Out32(datareg, 0)            
                # break --> from 3sec up to 4sec
                gobject.idle_add(self.Break, tr)
                time.sleep(rd.uniform(2.998, 3.998))
                self.current = self.mental_task[1]
            # (3) Run End (break)
            if not(all([self.OneRun, trials == []])): break
            # -- stop saving continuos eeg data (PauseOn)
            pdll.Out32(datareg, 11)
            time.sleep(1)
            pdll.Out32(datareg,  0)
            time.sleep(1)
            # -- break message
            self.event_box.remove(self.current)
            self.current = Image('Images\\break.png')
            self.event_box.add(self.current)
            self.runs += 1
            self.ON = True
        if not(all([self.OneRun, trials == []])):
            pdll.Out32(datareg, 11)
            time.sleep(1)
            pdll.Out32(datareg,  0)
            time.sleep(1)
            return
        self.event_box.remove(self.current)
        self.event_box.add(Image('Images\\end.png'))
        msg = 'Dear Participant:\n\n\
               Your collaboration has been really helpful\n\
               for our rearch. Thank you!'
        self.Title[0].set_text(msg)
        self.Title[0].show()
        self.ON = False
        global experiment
        experiment = 'concluded'

    #:::::::::::::::::: Method E: Warning ::::::::::::::::::
    def Warning(self):
        'Warning Control'
        
        self.event_box.remove(self.current)
        self.event_box.add(self.mental_task[0])
        STYLE = self.event_box.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.event_box.get_colormap().alloc_color(light_orange)
        self.event_box.set_style(STYLE)

    #::::::::::::::: Method F: Cue Onset :::::::::::::::::::
    def CueOnset(self, tr):
        'Motor Imaginary Performance'
        
        self.event_box.remove(self.mental_task[0])
        self.event_box.add(self.mental_task[tr])
        STYLE = self.event_box.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.event_box.get_colormap().alloc_color(orange)
        self.event_box.set_style(STYLE)
        
    #:::::::::::::::::::: Method G: Break ::::::::::::::::::
    def Break(self, tr):
        'Random Break'
        
        self.event_box.remove(self.mental_task[tr])
        self.event_box.add(self.mental_task[1])
        STYLE = self.event_box.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.event_box.get_colormap().alloc_color('white')
        self.event_box.set_style(STYLE)
# ==========================================================
# |6| MAIN BODY
# ==========================================================
#
if __name__ == '__main__':
    # START
    FinalReport_start()
    # 6.1 MI training stimuli control --> threading design
    gobject.threads_init()
    MI = MITraining()
    MI.start()
    # 6.2 GUI control --> main thread
    gtk.main()
    MI.quit = True
    # 6.3 BDF file conversion
    if experiment == 'concluded':
        FinalReport_concluded()
        # --- reading bdf file
        BDF = sopen(url)
        Data = sread(BDF, blocks, start)
        BDF = sclose(BDF)
        # --- trigger information extraction
        triggers = Data[:, recorded_ch]
        # --- conversion from two's complement format to desired triggers
        for index in range(len(triggers)): triggers[index] = (int(triggers[index]))& 255
        MARKERS = []
        # --- trigger 1 extraction: Pre-MI performance (2 seconds)
        MARKERS.append(SearchTrig(1, triggers))
        # --- trigger 2 extraction: left motor imaginary movement (4 seconds)
        MARKERS.append(SearchTrig(3, triggers))
        # --- trigger 3 extraction: right motor imaginary movement(4 seconds)
        MARKERS.append(SearchTrig(4, triggers))
        # --- trigger 4 extraction: Post-MI performance (3 seconds)
        MARKERS.append(SearchTrig(5, triggers))
        # --- conversion
        for markers in MARKERS:
            filename = FILENAME.pop(0)
            BDF2Matrix(markers, filename, Data)
        # END
        FinalReport_end()
    elif experiment == 'interrupted':
        FinalReport_interrupted()
        

# ==========================================================
# |7| USEFUL NOTES
# ==========================================================
##
## -It's really important to design a good programm considering
##  functions and classes,
##  because this reduces memory owing to the temporal data storage.
##
## -Use global variables in very particular cases.
##
## -The Default.cfg of ActiveView has been modified in order to
##  control the Pause Button:
##  PauseOff = 10 (the ActiveView continues saving data)
##  PauseOn  = 11 (the ActiveViee stops saving data)
