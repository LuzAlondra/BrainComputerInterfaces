# -*- coding: utf-8 -*-
### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### February 4th, 2011



# **********************************
# *    Graphical User Interface    *
# * (GUI suited for EXP2-purposes) *
# **********************************



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
import audiere
import gobject
import gtk
import pango
import pygtk
pygtk.require('2.0')
import random
import time

# ...................GUI Design Libraries...................
from Constructors import Image,Label,Frame,Button_Label,Button_Image,Frame_Image




# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL CONSTANTS DECLARATION

# (c) Cue Signal
beep_loc    = 'Sounds\\Cue.wav'
correct_loc = 'Sounds\\WellDone.wav'
wrong_loc   = 'Sounds\\TryAgain.wav'
click_loc   = 'Sounds\\Neutral.wav'
#
# (d) GUI Parameters
small_font = "Georgia 10"
medium_font = "Century Gothic 17"
orange = '#FA6121'
blue = '#466289'
lblue = '#A0AEC1'
tab_bg = '#DCDCDC'
ground = '#000000'  
#
# (e) Audio-Feedbacks for Cue-Driven & Target-Driven Systems (key := GUI_VE code)
feedbacks = {'Cue-Driven':   {'056': 'Sounds\\Cue-DrivenSys\\fdb1_Zipper.wav',\
                              '016': 'Sounds\\Cue-DrivenSys\\fdb2_FaceWashing.mp3',\
                              '017': 'Sounds\\Cue-DrivenSys\\fdb3_HandWashing.mp3',\
                              '020': 'Sounds\\Cue-DrivenSys\\fdb4_CombHair.wav',\
                              '033': 'Sounds\\Cue-DrivenSys\\fdb5_Urinating.wav',\
                              '212': 'Sounds\\Neutral.wav',\
                              '220': 'Sounds\\Cue-DrivenSys\\fdb6_OpeningBlinds.wav',\
                              '270': 'Sounds\\Cue-DrivenSys\\fdb7_OpeningWin.mp3',\
                              '060': 'Sounds\\Cue-DrivenSys\\fdb8_BiteApple.wav',\
                              '062': 'Sounds\\Cue-DrivenSys\\fdb9_Cereals.aif',\
                              '063': 'Sounds\\Cue-DrivenSys\\fdb10_Milk.wav'},\
             'Target-Driven':{'230': 'Sounds\\Target-DrivenSys\\target1-DoorOpen.mp3',\
                              '307': 'Sounds\\Neutral.wav',\
                              '064': 'Sounds\\Target-DrivenSys\\target3-SwallowingWater.wav',\
                              '017': 'Sounds\\Target-DrivenSys\\target4-BathroomExtractor.mp3',\
                              '066': 'Sounds\\Target-DrivenSys\\target5-Eating.mp3',\
                              '030': 'Sounds\\Target-DrivenSys\\target7-ToiletFlushing.mp3',\
                              '010': 'Sounds\\Target-DrivenSys\\target8-RinsingOut.wav',\
                              '075': 'Sounds\\Target-DrivenSys\\target9-Snoring.mp3'}}
HCI_codes = {'Cue-Driven':   ['13','056','12','016','017','020','033','17','212','220','270','060','062','063'],\
             'Target-Driven':['230','307','064','017','066','307','030','010','075']}
CueSys_codes = {0:([],[6,7],[0],[3],[],[6],[0,2,3],[]), 2:([],[2],[0],[],[],[],[],[0])}
#
# (f) Distractors (only Target-Driven Systems)
distractor_locs = ['Sounds\\Target-DrivenSys\\extra1-Knock.mp3',\
                   'Sounds\\Target-DrivenSys\\extra2-CuckooClock.mp3',\
                   'Sounds\\Target-DrivenSys\\extra3-PeopleTalking.mp3',\
                   'Sounds\\Target-DrivenSys\\extra4-TelephoneRinging.mp3',\
                   'Sounds\\Target-DrivenSys\\extra5-Steps.mp3',\
                   'Sounds\\Target-DrivenSys\\extra6-CellularPhone.mp3',\
                   'Sounds\\Target-DrivenSys\\extra7-MicrowaveOven.wav',\
                   'Sounds\\Target-DrivenSys\\extra8-KnockWin.mp3']
#
# (g) 3D Render for Target-Driven Systems
room_labels = ['Entrance', 'Kitchen', 'My Bedroom', 'Bathroom', 'Carer-Room', 'Living-Room']
room_len    = {'Entrance':2, 'Kitchen':5, 'My Bedroom':11, 'Bathroom':13, 'Carer-Room':16, 'Living-Room':20}
target_rooms= ['Entrance', 'Living-Room', 'Bathroom', 'Kitchen', 'Bathroom', 'My Bedroom']
target_codes= ['start', '230', '017', '066', '030', '075']
#
#
# (i) Messages/Images for Target-Driven Systems
Instructions = [['Well Done!','Images\\WellDone.png', 4],\
                ['Listen the\nNext Target','Images\\Listen.png', 4],\
                ['Get Ready','Images\\GetReady.png', 4],\
                ['Go!','Images\\Go.png', 1.5]]



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION



# ....................... Function V .......................
def DialogBox(device, target):
    'Instructions to listen the Audio-Targets in Target-Driven Systems'

    ## -- dialog box
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    ## --window configuration
    window.set_title("ESSEX Virtual Environment: Human-Computer Interface")
    background = gtk.gdk.color_parse(tab_bg)
    window.modify_bg(gtk.STATE_NORMAL, background)
    window.set_border_width(10)
    ## -- table: General widget container
    table = gtk.Table(1, 2, True)
    table.show()
    ## -- widget packing    
    window.add(table)
    # label widget
    message = Label('hello', 'Elephant 20', 'orange', 0, 0.5, gtk.JUSTIFY_LEFT)
    table.attach(message, 1, 2, 0, 1)
    cartoon = Image('Images\\GetReady.png')
    table.attach(cartoon, 0, 1, 0, 1)
    ## -- dialog display
    window.show_all()
    window.connect('destroy', destroy)
#    ## -- instruction sequence
#    for idx in range(len(Instructions)):
#        # -variable declaration-
#        m, i, wait = Instructions[idx][0], Instructions[idx][1], Instructions[idx][2]
#        # -label update-
#        message.set_text(m)
#        # -image widget-
#        cartoon = Image(i)
#        table.attach(cartoon, 0, 1, 0, 1)        
#        # -wait for 4 or 1.5 seconds-
#        time.sleep(wait)  
#        # -play record-
#        if idx == 2:
#            track = '\\'.join(['Sounds\\Target-DrivenSys', target])
#            track = device.open_file(track)
#            # playing 3 times the target-
#            track.play()
#            while track.playing == 1: None
#            track.play()
#            while track.playing == 1: None
#            track.play()
#            while track.playing == 1: None   
#        # -image widget deleting-
#        table.remove(cartoon)    
    ## -- window exit

def destroy(widget): gtk.main_quit()
    
device = audiere.open_device()
DialogBox(device, None)
gtk.main()
time.sleep(3)


