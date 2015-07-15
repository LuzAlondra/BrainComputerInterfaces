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
import copy
import datetime
import gobject
import gtk
import pango
import pygtk
pygtk.require('2.0')
import random
import threading
import time
import SendKeys as sks
import win32com.client as comclt
from ctypes import windll
from socket import *
# ...................GUI Design Libraries...................
from Constructors import Image,Label,Frame,Button_Label,Button_Image,Frame_Image
from nd_menu import nd_menu
from mob_menu import mob_menu
from EC_menu  import EC_menu
from msg_menu import msg_menu
from UT_menu import UT_menu



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL CONSTANTS DECLARATION
# (a) HCI Server 
HOST = ''
PORT = 21558
BUFSIZ = 1024
ADDR = (HOST, PORT)
HCISerSock = socket(AF_INET, SOCK_STREAM)
HCISerSock.bind(ADDR)
HCISerSock.listen(2)
#
# (b) Trigger SetUp
pdll = windll.inpout32
datareg = 0x378
pdll.Out32(datareg, 0)
#
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
                              '307': 'Sounds\\WellDone.wav',\
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
distractor_rpts = [6, 4, 1, 3, 2, 5, 3, 4]
#
# (g) 3D Render for Target-Driven Systems
room_labels = ['Entrance', 'Kitchen', 'My Bedroom', 'Bathroom', 'Carer-Room', 'Living-Room']
room_len    = {'Entrance':2, 'Kitchen':5, 'My Bedroom':11, 'Bathroom':13, 'Carer-Room':16, 'Living-Room':20}
target_rooms= ['Entrance', 'Kitchen', 'Bathroom', 'Kitchen', 'Bathroom', 'My Bedroom']
target_codes= ['start', '017', '066', '030', '075']
#
# (h) Active Application
APP = comclt.Dispatch("WScript.Shell")
#
# (i) Messages/Images for Target-Driven Systems
Instructions = [['Well Done!','Images\\WellDone.png', 10],\
                ['Listen the\nNext Target','Images\\Listen.png', 10],\
                ['Get Ready','Images\\GetReady.png', 10],\
                ['Go!','Images\\Go.png', 2]]



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION
# ....................... Fuction I ........................
def ParallelPort(trigger, TrigNum):
    'Trigger Sender to the Parallel Port'
    
    trigger = int(trigger) + int(TrigNum)
    pdll.Out32(datareg, trigger)
    time.sleep(0.004)
    pdll.Out32(datareg, 0)


# ...................... Function II ......................
def Config_Video(sys_type):
    'Video Configuration to start the Visual Feedback'
    
    sks.SendKeys("""{LWIN}{PAUSE 1}
                 e{PAUSE 1}
                 CMD{ENTER}{PAUSE 1}
                 cd..{ENTER}{PAUSE 1}
                 cd..{ENTER}{PAUSE 1}
                 cd{SPACE}+7Archivos{SPACE}de{SPACE}programa+7VideoLAN+7VLC{ENTER}{PAUSE 1}
                 vlc{SPACE}VideoExp2.mp4{SPACE}--rate{SPACE}0.25{ENTER}{PAUSE 120}""")
    if sys_type == 'Target-Driven': VLC_Window(VideoDuration())
    return    
    

# ..................... Function III .......................
def VideoDuration():
    'Calculation of the time that needs the Video to play during the visual feedback'
    
    video_len = 0
    target_codes.append(target_codes.pop(0))
    target_rooms.append(target_rooms.pop(0))
    while target_rooms[-1] != room_labels[0]: room_labels.append(room_labels.pop(0))
    label_idx = room_labels.index(target_rooms[0])
    for index in range(1, label_idx+1): video_len += room_len[room_labels[index]]
    return video_len

# ...................... Function IV .......................
def VLC_Window(video_len):
    'Control of the VLC media player via Key Emulation'
    
    pause = ' '.join(["""{SPACE}{PAUSE""", str(video_len), """}"""])       
    APP.AppActivate("VLC media player")
    sks.SendKeys(pause)
    APP.AppActivate("VLC media player")
    sks.SendKeys("""{SPACE}""")


# ....................... Function V .......................
def HCI_Presentation():
    'Heading of the Printed Code'
    
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
    print '............. H U M A N   C O M P U T E R   I N T E R F A C E ...............'
    print '.............................................................................'
    print '\n\n\n'
    print '============================================================================='
    print 'Program Status                                                               '
    print '============================================================================='



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "essexHCI_Thread" CLASS DECLARATION

class essexHCI_Thread(threading.Thread):
    'Class to control the Essex human computer interface by means of a new thread'

    # ╦╦╦╦╦╦╦╦╦╦╦ Method A: Initial Performance ╦╦╦╦╦╦╦╦╦╦╦╦
    def __init__(self):
        'Initial method to generate the Essex HCI'

        # ==================thread creation=================
        threading.Thread.__init__(self)
        
        # ================interface creation================        
        # (1) WINDOW 
        ## -- window creation
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        ## --window configuration
        self.window.set_title("ESSEX Virtual Environment: Human-Computer Interface")
        background = gtk.gdk.color_parse(ground)
        self.window.modify_bg(gtk.STATE_NORMAL, background)
        self.window.set_border_width(7)
        self.window.set_resizable(True)
        self.window.resize(1275, 770)
        self.window.move(-1, -2)
        ## -- window events connection
        self.window.connect('destroy', self.destroy)
        
        # (2) TABLE: General widget container
        table = gtk.Table(3, 4, False)
        table.show()
        self.window.add(table)
        
        # (3) NOTEBOOK: General widget container
        ## -- notebook creation
        general_menu = gtk.Notebook()
        ## -- notebook configuration
        general_menu.set_show_border(True)
        general_menu.set_show_tabs(True)     
        general_menu.set_size_request(1260, 705)   
        style = general_menu.get_style().copy()
        style.bg[gtk.STATE_NORMAL] = general_menu.get_colormap().alloc_color(tab_bg)
        general_menu.set_style(style)
        ## -- 'necessities & desires' tab insertion
        nd_label = Label('Necessities&Desires ', small_font, orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        necessities = nd_menu()
        nd_table = necessities.nd_container()
        general_menu.append_page(nd_table, nd_label)        
        ## -- 'mobility' tab insertion
        mob_label = Label('Mobility ', small_font, orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        mobility = mob_menu()
        mob_table = mobility.mob_container()
        general_menu.append_page(mob_table, mob_label)        
        ## -- 'environment control' (EC) tab insertion
        EC_label = Label('EnvironmentControl ', small_font, orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        EC = EC_menu()
        EC_table = EC.EC_container()
        general_menu.append_page(EC_table, EC_label)        
        ## -- 'messenger' tab insertion
        msg_label = Label('Messenger ', small_font, orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        messenger = msg_menu()
        msg_table = messenger.msg_container()
        general_menu.append_page(msg_table, msg_label)
        ## -- 'user-training' tab insertion
        ut_label = Label('User-Training ', small_font, orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        tutorial = UT_menu()
        ut_table = tutorial.UT_container()
        general_menu.append_page(ut_table, ut_label)
        ## -- notebook insertion to table
        table.attach(general_menu, 0, 4, 0, 1)
        general_menu.show()
        self.window.show()
        
        # (4) Copyright
        label = Label(' University of Essex ~ BCI Group', small_font, lblue, 0, 1, gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 1, 2)
        label = Label(' Luz Ma. Alonso Valerdi & Francisco Sepulveda', small_font, lblue, 0, 0.5, gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 2, 3)  
        border = Image('Images\\Border.png')
        border.set_alignment(xalign = 0.3, yalign = 0.75)
        table.attach(border, 1, 3, 1, 3) 
        logo = Image('Images\\logo.jpg')
        logo.set_alignment(xalign = 0.95, yalign = 1)
        table.attach(logo, 3, 4, 1, 3)
        general_menu.set_current_page(-1)             
                
        # (5) Attribute assignation to enable them in following
        #     methods
        ## -- main window
        self.general_menu = general_menu
        ## -- each instance corresponding to each tab        
        self.necessities = necessities
        self.mobility = mobility
        self.EC = EC
        self.messenger = messenger
        self.tutorial = tutorial
        ## -- each widget container (table) corresponding to each tab
        self.TabTables = (nd_table, mob_table, EC_table, msg_table)
        self.quit = False
        
        
    # ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦ Method B: Killing GUI ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦
    def destroy(self, widget):
        'Callback to QUIT the messenger menu and the infinite loop in Method C'

        self.quit = True
        gtk.main_quit()
        
       
    # ╦ Method C: Attending to essexHCI_Thread Requirements ╦
    def run(self):
        'This sequence is performed according to the available\
        time to do it, because the main thread is used by gtk.main()'
        
        # ======================
        # |1| HCI Initialization
        # ======================
        ## -- default variables
        codes, distractors, source_id, distractor, repeats = ['None'], [], 0, None, 0
        ## -- default attributes
        self.submenu,self.HOME,self.targets,self.current_subutton,self.current_len,self.video_len,self.ready,self.repeat,self.PLAY = \
        False       ,True     ,[None]      ,'unknown_task'       ,'unknown_len'   ,0             ,False     ,0          ,False
        ## -- starting a device to play sounds by means of the 'audiere' library
        device = audiere.open_device()
        ## -- loading the cue-sounds
        beep    = device.open_file(beep_loc)
        correct = device.open_file(correct_loc)
        wrong   = device.open_file(wrong_loc)
        click   = device.open_file(click_loc)
        ## -- loading the distractor-sounds
        #for track in distractor_locs: distractors.append(device.open_file(track))
        ## -- intro report
        HCI_Presentation()
        ## -- waiting a client request (i.e., BCI System Connection)
        print 'Waiting for connection . . .'
        BCICliSock, addr = HCISerSock.accept()
        print '. . . connected from:', addr    
        # ==================================================================         
        # |2| Infinite loop to not lose the control thread (OnLine Paradigm)
        # ==================================================================
        while not self.quit:       
            # (a) +++++ Receiving an instruction from BCI client +++++
            instruction = BCICliSock.recv(BUFSIZ)
            if not instruction: break
            print 'The received instruction is:', instruction           
            # (b) +++++ Decoding the received instruction +++++
            TrigNum = instruction.split('*')[0]
            instruction = instruction.split('*')[-1]
            command = instruction.split('_')[0] 
            target  = instruction.split('_')[-1]  
            # (c) +++++ Reset of Variables +++++
            code, self.GUI_VE = codes[0], '' 
            # (d) +++++ Calling the appropiated method according to the TCP-message +++++
            # --> Start saving continuos eeg data (PauseOff) or
            #     Pause saving continous eeg data (PauseOn)
            if command.isdigit():
                time.sleep(1)
                ParallelPort(TrigNum, 0)
                time.sleep(1)
            # --> Type Of System: Tutorial_MI or Tutorial_CMD
            elif command == 'Tutorial':
                ## - variable declaration
                UT_status, sys_type, trigger = True, target, TrigNum 
                ## - configuration of the Tutorial_Command System                
                if target == 'CMD': 
                    self.submenu, self.HOME = False, True
                    gobject.idle_add(self.tutorial.UT_CMDSysConfig)   
                ## - trigger delivery
                ParallelPort(trigger, 0)
            # --> Type Of System: Training_GUI & Testing_GUI
            elif any([command=='Training',command=='Testing']):   
                ## - switch to first tab & interface~reset
                self.ready = False
                gobject.idle_add(self.GUI_ResetTabs, self.submenu)  
                while not self.ready: None
                ## - variable reset
                UT_status, sys_type, trigger, self.submenu, self.HOME = False, command, TrigNum, False, True 
                ## - trigger delivery
                ParallelPort(trigger, 0)            
            # --> Type Of System: Cue-Driven & Target-Driven
            elif any([command=='Cue-Driven',command=='Target-Driven']):
                ## - initialize the video~play
                Config_Video(command)   
                ## - switch to first tab & interface~reset
                self.ready = False
                gobject.idle_add(self.GUI_ResetTabs, self.submenu)
                while not self.ready: None
                ## - variable reset
                UT_status, sys_type, trigger, self.submenu, self.HOME = False, command, TrigNum, False, True 
                ## - load of the system-targets
                codes = HCI_codes[sys_type]                
                ## - trigger delivery
                ParallelPort(trigger, 0)
            # --> Warning Sign: Preparation for the MI Movement
            elif command == 'warning':
                ## - GUI modification            
                self.ready = False
                gobject.idle_add(self.Warning_Sign, UT_status, sys_type) 
                while not self.ready: None
                ## - trigger delivery
                ParallelPort(trigger, TrigNum)                               
            # --> Cue Onset: MI Movement Performance
            elif command == 'cue':
                ## - beep performance
                beep.play()
                ## - GUI modification
                self.ready = False
                gobject.idle_add(self.Cue_Onset, UT_status, target, sys_type)
                while not self.ready: None 
                ## - trigger delivery
                ParallelPort(trigger, TrigNum)                   
            # --> Blank: random inter-trial interval (only Tutorial_MI, Tutorial_CMD & Training_GUI)
            #    "Execution of the sent cue in order to do a demostration of the command"
            elif command == 'blank':
                ## - CASE 1: Tutorial_MI
                if sys_type == 'MI':
                    gobject.idle_add(self.tutorial.UT_BlankMI, target)
                ## - CASE 2: Tutorial_CMD and Training_GUI 
                else:
                    self.ready = False
                    if target == 'left':
                        click.play()
                        gobject.idle_add(self.Select_Command, UT_status, target, sys_type, code) 
                    elif target == 'right':
                        click.play()
                        gobject.idle_add(self.Navigate_Command, UT_status, target, sys_type, code)       
                    elif target == 'idle':
                        gobject.idle_add(self.No_Command, UT_status, sys_type, target, command)  
                    while not self.ready: None
                ## - trigger delivery
                ParallelPort(trigger, TrigNum) 
            # --> Left: user's command interpretation
            elif command == 'left': 
                self.ready = False            
                ## - CASE 1 & 2: Testing_GUI & Cue-Driven System
                if any([sys_type == 'Testing', sys_type == 'Cue-Driven']):
                    if command == target:
                        correct.play()
                        gobject.idle_add(self.Select_Command, UT_status, target, sys_type, code)
                    else:
                        wrong.play()
                        gobject.idle_add(self.No_Command, UT_status, sys_type, target, command) 
                ## - CASE 3: Target-Driven System
                elif sys_type == 'Target-Driven':
                    click.play()    
                    gobject.idle_add(self.Select_Command, UT_status, target, sys_type, code)  
                ## - trigger delivery
                while not self.ready: None
                ParallelPort(trigger, TrigNum)                                    
            # --> Right: user's command interpretation
            elif command == 'right': 
                self.ready = False
                ## - CASES 1 & 2: Testing GUI & Cue-Driven System
                if any([sys_type == 'Testing', sys_type == 'Cue-Driven']):
                    if command == target:
                        correct.play()
                        gobject.idle_add(self.Navigate_Command, UT_status, target, sys_type, code)
                    else:
                        wrong.play()
                        gobject.idle_add(self.No_Command, UT_status, sys_type, target, command)
                ## - CASE 3: Target-Driven System
                elif sys_type == 'Target-Driven':
                    click.play()  
                    gobject.idle_add(self.Navigate_Command, UT_status, target, sys_type, code)   
                ## - trigger delivery
                while not self.ready: None
                ParallelPort(trigger, TrigNum)         
            # --> Idle: user's command interpretation
            elif command == 'idle':
                self.ready = False
                ## - CASES 1 & 2: Testing GUI & Cue-Driven System
                if any([sys_type == 'Testing', sys_type == 'Cue-Driven']):
                    if command == target:
                        correct.play()
                    else:
                        wrong.play()                                             
                ## - GUI modification
                gobject.idle_add(self.No_Command, UT_status, sys_type, target, command)        
                ## - trigger delivery
                while not self.ready: None
                ParallelPort(trigger, TrigNum)             
            # --> Stopping HCI manipulation
            elif command == 'quit':
                ## - System Exit
                print 'The TCP connection has been closed.'                
                break                                                       
            # --> Audio-Target for Target-Driven Systems
            else:
                ## -- Current Table
                self.container = self.TabTables[self.general_menu.get_current_page()]
                ## -- Sequence of Instructions
                for idx in range(len(Instructions)):
                    # variable assignment
                    m, i, wait = Instructions[idx][0], Instructions[idx][1], Instructions[idx][2]
                    # GUI modification according to the current tab
                    self.ready = False
                    gobject.idle_add(self.HCI_InstON, m, i, idx, codes)
                    while not self.ready: None                      
                    # wait for 4 or 1.5 seconds
                    time.sleep(wait)  
                    # play record
                    if idx == 1:
                        track = '\\'.join(['Sounds\\Target-DrivenSys', target])
                        track = device.open_file(track)
                        # playing 3 times the target-
                        track.play()
                        while track.playing == 1: None
                        time.sleep(1)
                        track.play()
                        while track.playing == 1: None   
                    # GUI modification according to the current tab
                    self.ready = False
                    gobject.idle_add(self.HCI_InstOFF)
                    while not self.ready: None                                                      
            # (e) +++++ self.GUI_VE (HCIresponse) Assessment +++++
            # e.1 CASE 1: HCI-codes (next target if one option from the correct submenu is selected)
            if self.GUI_VE == code:
                # --> play feedback
                TCPmsg, codes = self.HCI_Feedback(sys_type, codes, device, source_id)
                # --> play distractor randomly
                #if sys_type == 'Target-Driven': 
                #    distractor, repeats, rand_time = distractors.pop(0), distractor_rpts.pop(0), random.randint(40000, 80000)
                #    source_id = gobject.timeout_add(rand_time, self.HCI_Distractors, repeats)
            # e.2 Any other case (there are no targets to pursue)                               
            else:
                # --> TCP message (ready + current_subutton): Cue-Driven System Proposes
                TCPmsg = '_'.join(['Task/MenuLength', str(self.current_subutton), str(self.current_len)])
            # (f) +++++ Play of the Distractor if it is available +++++
            #if all([self.PLAY, self.repeat > 0]): 
            #    distractor.play()
            #    self.PLAY = False            
            # (g) +++++ Reply to BCI-System +++++
            BCICliSock.send(TCPmsg)   
            print 'Satisfactory reply to the TCP client: ', TCPmsg
        # ================================
        # |3| Closure of TCP-communication
        # ================================ 
        BCICliSock.close()
        HCISerSock.close()
            
    
    # ╦╦╦╦╦╦╦╦╦╦╦╦╦╦ Method D: Warning Signal ╦╦╦╦╦╦╦╦╦╦╦╦╦╦
    def Warning_Sign(self, UT_status, sys_type):
        'Warning Delivery (Light Orange Background)'
        
        # 1.- User-Tutorial Mode
        if UT_status:
            # -- Motor Imagery Stage
            if sys_type == 'MI':                
                self.tutorial.UT_WarningMI()            
            # -- Command Stage
            else:
                self.tutorial.UT_WarningCMD(self.submenu)          
        # 2.- Modes: User_Training, Cue-Driven & Target-Driven 
        else:
            tab = self.general_menu.get_current_page()
            if tab == 0:
                self.current_subutton, self.current_len = self.necessities.nd_WarningSign(self.submenu)
            elif tab == 1:
                self.current_subutton, self.current_len = self.mobility.mob_WarningSign(self.submenu)
            elif tab == 2:
                self.current_subutton, self.current_len = self.EC.EC_WarningSign(self.submenu)
            elif tab == 3:
                self.current_subutton, self.current_len = self.messenger.msg_WarningSign(self.submenu) 
        # 3.- The idle_fuction has completed its performance
        self.ready = True
        return False
   
    
    # ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦ Method E: Cue Onset ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦
    def Cue_Onset(self, UT_status, target, sys_type):
        'Cue Onset (Allowance of the MI Mov Performace)'
        
        # 1.- User-Tutorial Mode
        if UT_status:
            # -- Motor Imagery stage
            if sys_type == 'MI':                
                self.tutorial.UT_CueMI(target)            
            # -- Command stage
            else:
                self.tutorial.UT_CueCMD(self.submenu, target)          
        # 2.- Modes: User_Training, Cue-Driven & Target-Driven 
        else:        
            tab = self.general_menu.get_current_page()
            if tab == 0:
                self.necessities.nd_MIPerformance(self.submenu, target)
            elif tab == 1:
                self.mobility.mob_MIPerformance(self.submenu, target)
            elif tab == 2:
                self.EC.EC_MIPerformance(self.submenu, target)
            elif tab == 3:
                self.messenger.msg_MIPerformance(self.submenu, target) 
        # 3.- The idle_fuction has completed its performance
        self.ready = True
        return False


    # ╦╦╦╦╦╦╦╦╦╦╦╦ Method F: NAVIGATE command ╦╦╦╦╦╦╦╦╦╦╦╦╦╦
    def Navigate_Command(self, UT_status, target, sys_type, code):
        'Control of the "Navigate" command'
        
        # ***** 'Navigate' command available for the general menu *****
        if not(self.submenu):
            # 1.- User-Tutorial Mode: CMD
            if UT_status:                
                self.tutorial.UT_BlankCMD(target)    
                self.tutorial.UT_NextIcon()                                  
            # 2.- Modes: User_Training, Cue-Driven & Target-Driven 
            else:            
                tab = self.general_menu.get_current_page()
                if tab == 0:
                    self.general_menu.next_page()
                    self.necessities.nd_Blank(target)
                    self.necessities.nd_Reset()
                elif tab == 1:
                    self.general_menu.next_page()
                    self.mobility.mob_Blank(target)
                    self.mobility.mob_Reset()
                elif tab == 2:
                    self.general_menu.next_page()
                    self.EC.EC_Blank(target)
                    self.EC.EC_Reset()
                elif tab == 3:
                    self.general_menu.set_current_page(0)
                    self.messenger.msg_Blank(target)
                    self.messenger.msg_Reset()        
        # ****** 'Navigate' command available for the main menu *****
        else:
            if self.HOME:
                # -- unabling oportunity to quit from main menu
                # -- selecting the correct menu according to the current page
                # 1.- User-Tutorial Mode: CMD
                if UT_status:    
                    self.tutorial.UT_BlankCMD(target)                
                    self.HOME = self.tutorial.UT_Reactivation()                                            
                # 2.- Modes: User_Training, Cue-Driven & Target-Driven 
                else:
                    tab = self.general_menu.get_current_page()
                    if tab == 0:
                        self.necessities.nd_Blank(target)
                        self.HOME = self.necessities.nd_Reactivation(self.targets)
                    elif tab == 1:
                        self.mobility.mob_Blank(target)
                        self.HOME = self.mobility.mob_Reactivation()
                    elif tab == 2:
                        self.EC.EC_Blank(target)
                        self.HOME = self.EC.EC_Reactivation(self.targets)
                    elif tab == 3:
                        self.messenger.msg_Blank(target)
                        self.HOME = self.messenger.msg_Reactivation()
            else:
                # -- user is not at HOME button
                # -- selecting the correct menu according to the current page
                # 1.- User-Tutorial Mode: CMD
                if UT_status: 
                    self.tutorial.UT_BlankCMD(target)                      
                    self.HOME = self.tutorial.UT_Control()                                          
                # 2.- Modes: User_Training, Cue-Driven & Target-Driven
                else:
                    # -- current tab
                    tab = self.general_menu.get_current_page()
                    # -- switching among the tabs
                    if tab == 0:
                        #{only Cue-Driven Systems
                        if sys_type == 'Cue-Driven': 
                            self.targets = copy.copy(CueSys_codes[tab][int(code[1])])
                            self.targets.append(int(code[1])) #}
                        self.necessities.nd_Blank(target)
                        self.HOME = self.necessities.nd_Control(self.targets)             
                    elif tab == 1:
                        self.mobility.mob_Blank(target)
                        self.HOME = self.mobility.mob_Control()
                    elif tab == 2:
                        #{only Cue-Driven Systems
                        if sys_type == 'Cue-Driven': 
                            self.targets = copy.copy(CueSys_codes[tab][int(code[1])])
                            self.targets.append(int(code[1])) #}
                        self.EC.EC_Blank(target)
                        self.HOME = self.EC.EC_Control(self.targets)
                    elif tab == 3:                
                        self.messenger.msg_Blank(target)
                        self.HOME = self.messenger.msg_Control()        
        # ***** The idle_fuction has completed its performance *****
        self.ready = True            
        return False
        

    # ╦╦╦╦╦╦╦╦╦╦╦╦╦╦ Method G: SELECT command ╦╦╦╦╦╦╦╦╦╦╦╦╦╦
    def Select_Command(self, UT_status, target, sys_type, code):
        'Control of the "Select" command'
        
        # ***** 'Select' command available for the general menu *****
        if not(self.submenu):
            ## -- Turn on the submenu option
            self.submenu = True
            ## -- Calling the "activation" method for initializing
            ##     the corresponding menu performance
            # 1.- User-Tutorial Mode: CMD
            if UT_status:                               
                self.tutorial.UT_BlankCMD(target)
                self.HOME = self.tutorial.UT_Activation()                                       
            # 2.- Modes: User_Training, Cue-Driven & Target-Driven 
            else:
                tab = self.general_menu.get_current_page()            
                if tab == 0:
                    #{only Cue-Driven Systems
                    if sys_type == 'Cue-Driven': 
                        self.targets = copy.copy(CueSys_codes[tab][int(code[1])])
                        self.targets.append(int(code[1])) #}
                    self.necessities.nd_Blank(target)
                    self.HOME = self.necessities.nd_Activation(self.targets)
                elif tab == 1:
                    self.mobility.mob_Blank(target)
                    self.HOME = self.mobility.mob_Activation()
                elif tab == 2:
                    #{only Cue-Driven Systems
                    if sys_type == 'Cue-Driven': 
                        self.targets = copy.copy(CueSys_codes[tab][int(code[1])])
                        self.targets.append(int(code[1])) #}
                    self.EC.EC_Blank(target)
                    self.HOME = self.EC.EC_Activation(self.targets)
                elif tab == 3:
                    self.messenger.msg_Blank(target)
                    self.HOME = self.messenger.msg_Activation()
        # ***** 'Select' command available for the main menu *****
        else:
            if self.HOME:
                # -- switch to the general menu
                self.submenu = False
                # -- selecting the correct menu according to the current page
                # 1.- User-Tutorial Mode: CMD
                if UT_status:                    
                    self.tutorial.UT_BlankCMD(target)
                    self.tutorial.UT_Deactivation()                                                              
                # 2.- Modes: User_Training, Cue-Driven & Target-Driven
                else:                    
                    tab = self.general_menu.get_current_page()
                    if tab == 0:
                        self.necessities.nd_Blank(target)
                        self.necessities.nd_Deactivation()
                    elif tab == 1:
                        self.mobility.mob_Blank(target)
                        self.mobility.mob_Deactivation()
                    elif tab == 2:
                        self.EC.EC_Blank(target)
                        self.EC.EC_Deactivation()
                    elif tab == 3:
                        self.messenger.msg_Blank(target)
                        self.messenger.msg_Deactivation()
            else:
                # -- selecting the correct menu according to the current page
                # 1.- User-Tutorial Mode: CMD
                if UT_status:
                    self.tutorial.UT_BlankCMD(target)                       
                    self.tutorial.UT_Writing()                                                              
                # 2.- Modes: User_Training, Cue-Driven & Target-Driven
                else:                     
                    tab = self.general_menu.get_current_page()
                    if tab == 0:
                        self.necessities.nd_Blank(target)
                        self.GUI_VE = self.necessities.nd_Writing()
                    elif tab == 1:
                        self.mobility.mob_Blank(target)
                        self.GUI_VE, self.video_len = self.mobility.mob_Writing()
                    elif tab == 2:
                        self.EC.EC_Blank(target)
                        self.GUI_VE = self.EC.EC_Writing()
                    elif tab == 3:
                        self.messenger.msg_Blank(target)
                        self.GUI_VE = self.messenger.msg_Writing()
                print '\n'
                print 'The selected task is: ', self.GUI_VE
        # ***** The idle_fuction has completed its performance *****
        self.ready = True
        return False
        
    
    # ╦╦╦╦╦╦╦╦╦╦╦ Method H: No Command Detection ╦╦╦╦╦╦╦╦╦╦╦
    def No_Command(self, UT_status, sys_type, target, command):
        'Weak MI Perfomance or No Detection of MI-Movement'
        
        # 1.- User-Tutorial Mode: CMD
        if UT_status:      
            self.tutorial.UT_BlankCMD(target)                           
            self.tutorial.UT_NoControl(self.submenu)                        
        # 2.- Modes: User_Training, Cue-Driven & Target-Driven
        else:        
            tab = self.general_menu.get_current_page()
            reset1 = all([sys_type == 'Cue-Driven', target == 'idle', command != 'idle'])
            reset2 = all([sys_type == 'Cue-Driven', target == 'left', command != 'left'])
            if tab == 0:
                self.necessities.nd_Blank(target)
                self.necessities.nd_NoControl(self.submenu, any([reset1, reset2]))
            elif tab == 1:
                self.mobility.mob_Blank(target)
                self.mobility.mob_NoControl(self.submenu)
            elif tab == 2:
                self.EC.EC_Blank(target)
                self.EC.EC_NoControl(self.submenu, any([reset1, reset2]))
            else:
                self.messenger.msg_Blank(target)
                self.messenger.msg_NoControl(self.submenu, any([reset1, reset2])) 
        # 3.- The idle_fuction has completed its performance
        self.ready = True
        return False
    
    
    # ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦ Method I: GUI Reset ╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦
    def GUI_ResetTabs(self, submenu): 
        'Reset of all the Interacting Tabs'
        
        # 1.- Resetting each tab
        self.necessities.nd_ResetALL(submenu, self.general_menu.get_current_page())
        self.mobility.mob_ResetALL(submenu, self.general_menu.get_current_page())
        self.EC.EC_ResetALL(submenu, self.general_menu.get_current_page())
        self.messenger.msg_ResetALL(submenu, self.general_menu.get_current_page())
        self.general_menu.set_current_page(0)
        # 2.- The idle_fuction has completed its performance
        self.ready = True
        return False


    # ╦╦╦╦╦╦╦╦ Method J: Target-Driven Instructions ╦╦╦╦╦╦╦╦
    def HCI_InstON(self, m, i, idx, codes): 
        '''Appending the Instructions to follow the Next Target in 
           "Target-Driven System" according to the current Tab'''
                   
        ## -- Variable Declaration        
        message = Label('', 'Elephant 17', 'orange', 0, 0.5, gtk.JUSTIFY_LEFT)
        self.container.attach(message, 1, 2, 0, 2)           
        ## -- Label Update
        if all([codes[0] == '230', idx == 0]):
            message.set_text(m.replace(' Done', 'come'))
        elif all([codes[0] == '230', idx == 1]):
            message.set_text(m.replace('Next', 'First'))
        else:
            message.set_text(m)
        ## -- image widget
        cartoon = Image(i)
        cartoon.set_alignment(xalign = 0.9, yalign = 0.5)
        self.container.attach(cartoon, 0, 1, 0, 2)        
        ## -- reset variables
        self.message = message
        self.cartoon = cartoon
        self.ready = True
        return False        
    
    
    # ╦╦╦╦╦╦╦╦ Method K: Target-Driven Instructions ╦╦╦╦╦╦╦╦
    def HCI_InstOFF(self): 
        '''Appending the Instructions to follow the Next Target in 
           "Target-Driven System" according to the current Tab'''
        
        self.container.remove(self.message)
        self.container.remove(self.cartoon)
        self.ready = True
        return False        
    
    
    # ╦╦╦╦╦╦╦╦╦ Method L: HCI AudioVisual Feedback ╦╦╦╦╦╦╦╦╦
    def HCI_Feedback(self, sys_type, codes, device, source_id):
        'AudioVisual Feedback for Cue-Driven & Target-Driven Systems'
        
        # 1.- Cue-Driven System
        if sys_type == 'Cue-Driven':
            # -- display 3D render
            if len(self.GUI_VE) == 2:     
                VLC_Window(self.video_len)
            # -- play feedback
            else:
                time.sleep(1)
                track = feedbacks[sys_type][self.GUI_VE]
                track = device.open_file(track)
                track.play()
                while track.playing == 1: None
        # 2.- Target-Driven System
        elif sys_type == 'Target-Driven':
            # -- removing the active timeout function
            #if self.repeat > 0: 
            #    self.repeat, self.PLAY = -1, False
            #    gobject.source_remove(source_id)
            # -- display 3D render
            if self.GUI_VE == target_codes[0]:
                # video length: calculation
                self.video_len = VideoDuration()
                # playing video
                VLC_Window(self.video_len)
            # -- play feedback
            time.sleep(1)
            track = feedbacks[sys_type][codes[0]]
            track = device.open_file(track)
            track.play()
            while track.playing == 1: None
        # -- TCP reply
        TCPmsg = self.GUI_VE
        # -- last position for the achived target
        codes.append(codes.pop(0))
        return TCPmsg, codes
    
    
    # ╦╦╦╦╦╦╦╦╦╦╦ Method M: HCI Audio-Distractors ╦╦╦╦╦╦╦╦╦╦
    def HCI_Distractors(self, repeats):
        'Audio-Distractors only for Target-Driven Systems'
        
        if self.repeat < repeats:
            ## -- allowance of track play
            self.PLAY = True
            ## -- play track less one repeat
            self.repeat += 1
            return True
        else:            
            ## -- end timeout function
            self.repeat, self.PLAY = -1, False
            return False       



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MAIN BODY

if __name__ == "__main__":
    # STEP A: To allow only the main thread to touch the GUI (gtk) part,
    #         while letting other threads do background work.
    gobject.threads_init()
    # STEP B: Instantiation process calls __init__ method by which will
    #         create the 'GUI' and the required 'Thread' 
    HCI = essexHCI_Thread()
    # STEP C: Initialization of both threads: gtk.main() and essexHCI_Thread
    HCI.start()
    gtk.main()



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# USEFUL NOTES

# NOTE 1:
# The gobject.idle_add() function adds a function (specified by callback)
# to be called whenever there are no higher priority events pending to the
# default main loop (i.e. gtk.main).
#
# NOTE 2:
# Never delete something if you don't understand its function in the program!!!!
#
# NOTE 3:
# When the gobject_idle callback are called, the program returns to the main thread,
# although the callback hasn't completed. Owing to this fact, the self.ready 
# has been included in the program to force the flow to wait till the callback is
# concluded.