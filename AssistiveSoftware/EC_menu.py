### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### August 24th, 2010

# ****************************
# * Graphical User Interface:*
# *'ENVIRONMENT CONTROL MENU'*
# ****************************

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
import pygtk
pygtk.require('2.0')
import gtk
import pango
import copy
import gobject


# ...................GUI Design Libraries...................
from Constructors import Image,Label,Button_Label,Frame_Image,Event_Image,Frame_Label

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL CONSTANTS DECLARATION
# (1) Format constants
black = '#213240'
blue = '#466289'
lblue = '#A0AEC1'
orange = '#FA6121'
light_orange = '#FABF8F'
ground = '#DCDCDC'
font = "Century Gothic 25"
medium_font = "Century Gothic 17"
small_font = "Century Gothic 10"
# (2) Main menu dictionary (sub-buttons labels)
MainMenu = {0: ['','','','','','','',''],\
            1: ['My\nBedroom', 'Living-\nRoom', 'Kitchen', 'Bathroom', 'Carer-\nRoom','','',''],\
            2: [['Open\nblinds\n(desk)','Close\nblinds\n(desk)','Open\nblinds\n(PC)','Close\nblinds\n(PC)','Open\nblinds\n(bed)','Close\nblinds\n(bed)','',''],\
                ['Open\ncurtains','Close\ncurtains','','','','','',''],\
                ['Open\nblinds','Close\nblinds','','','','','',''],\
                ['Open\ncurtains\n(table)','Close\ncurtains\n(table)','Open\ncurtains\n(sink)','Close\ncurtains\n(sink)','','','',''],\
                ['Open\ncurtains','Close\ncurtains','','','','','','']],\
            3: [['Open\nmain\ndoor','Close\nmain\ndoor','Open\nscape\ndoor','Close\nscape\ndoor','','','',''],\
                ['','','','','','','',''],\
                ['Open\nentrance','Close\nentrance','','','','','',''],\
                ['Open\ndoor','Close\ndoor','','','','','',''],\
                ['','','','','','','','']],\
            4: [['Turn\non\nheating','Turn\noff\nheating','Turn\nup\nheating','Turn\ndown\nheating','','','',''],\
                ['Turn\non\nheating','Turn\noff\nheating','Turn\nup\nheating','Turn\ndown\nheating','','','',''],\
                ['Turn\non\nheating','Turn\noff\nheating','Turn\nup\nheating','Turn\ndown\nheating','','','',''],\
                ['Turn\non\nheating','Turn\noff\nheating','Turn\nup\nheating','Turn\ndown\nheating','','','',''],\
                ['Turn\non\nheating','Turn\noff\nheating','Turn\nup\nheating','Turn\ndown\nheating','','','','']],\
            5: [['Turn\non\nlight','Turn\noff\nlight','Turn\non\nlamp','Turn\noff\nlamp','','','',''],\
                ['Turn\non\nlight','Turn\noff\nlight','Turn\non\nlamp','Turn\noff\nlamp','','','',''],\
                ['Turn\non\nlight','Turn\noff\nlight','Turn\non\nlamp','Turn\noff\nlamp','','','',''],\
                ['Turn\non\nlight','Turn\noff\nlight','Turn\non\nlamp','Turn\noff\nlamp','','','',''],\
                ['Turn\non\nlight','Turn\noff\nlight','Turn\non\nlamp','Turn\noff\nlamp','','','','']],\
            6: [['Turn\non','Turn\noff','Turn\nup','Turn\ndown','Play','Stop','Next','Previous'],\
                ['Turn\non','Turn\noff','Turn\nup','Turn\ndown','Play','Stop','Next','Previous'],\
                ['Turn\non','Turn\noff','Turn\nup','Turn\ndown','Play','Stop','Next','Previous'],\
                ['Turn\non','Turn\noff','Turn\nup','Turn\ndown','Play','Stop','Next','Previous'],\
                ['Turn\non','Turn\noff','Turn\nup','Turn\ndown','Play','Stop','Next','Previous']],\
            7: [['Open\nwindow\n(desk)','Close\nwindow\n(desk)','Open\nwindow\n(PC)','Close\nwindow\n(PC)','Open\nwindow\n(bed)','Close\nwindow\n(bed)','',''],\
                ['Open\nwindow','Close\nwindow','','','','','',''],\
                ['Open\nwindow\n(table)','Close\nwindow\n(table)','Open\nwindow\n(sink)','Close\nwindow\n(sink)','','','',''],\
                ['Open\nwindow','Close\nwindows','','','','','',''],\
                ['Open\nwindow','Close\nwindow','','','','','','']]
           }   
ROOMS = ['M Y    B E D R O O M','L I V I N G - R O O M','K I T C H E N','B A T H R O O M','C A R E R - R O O M']

       

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "EC_menu" CLASS DECLARATION

class EC_menu():
    'Class to control the "Environment Control" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "Environment Control" menu'
        
        # ======== Environment Control tab creation=========        
        # (1) TABLE: Widget container
        ## --9 x 8 table creation
        self.table = gtk.Table(9, 8, True)
        self.table.show()

        # (2) LABEL: Window title
        titulo = Label('Environment\nControl', 'Neuropol 31', orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        self.table.attach(titulo, 6, 8, 0, 2)        

        # (3) FRAMES & IMAGES: General menu images
        GralIconsON = []
        ## --'Necessities and Desires' option
        url = 'Images\\Necessity&Desire\\SNecessities_on.png'
        GralIconsON.append(Image(url))
        self.table.attach(GralIconsON[0], 2, 3, 0, 2)
        ## --'Mobility' option
        url = 'Images\\Mobility\\SMobility_on.png'
        GralIconsON.append(Image(url))
        self.table.attach(GralIconsON[1], 3, 4, 0, 2)
        ## --'Environmental Control' option
        url = 'Images\\EnvControl\\LHomeControl_on.png'
        EC_event, EC_image = Event_Image(url, ground)
        EC_event.set_border_width(10)
        GralIconsON.append(EC_image)
        self.table.attach(EC_event, 4, 5, 0, 2)
        ## --'Messenger' option
        url = 'Images\\Messenger\\SChat_on.png'
        GralIconsON.append(Image(url))
        self.table.attach(GralIconsON[3], 5, 6, 0, 2)
        
        # (4) IMAGES: Icons for cue indication
        CueSignals = []
        # -- cue: Left MI performance
        url = 'Images\\User_Tutorial\\left.png'
        image = Image(url)
        CueSignals.append(image)        
        # -- cue: Right MI performance
        url = 'Images\\User_Tutorial\\right.png'
        image = Image(url)
        CueSignals.append(image) 
        # -- cue: Idle MI performance
        url = 'Images\\User_Tutorial\\idle.png'
        image = Image(url)
        CueSignals.append(image)  
        
        # (5) LABELS: Icon labels for main menu
        mainmenu_labels, x, y = [], 1, 4
        # --- exit
        label = Label('Exit', medium_font, lblue, 0.1, 0.8, gtk.JUSTIFY_LEFT)
        self.table.attach(label,0, 2, 2, 4)        
        mainmenu_labels.append(label)
        # --- switch room
        label = Label('Switch\nRoom', medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
        self.table.attach(label, 0, 3, 2, 4)       
        mainmenu_labels.append(label)
        # --- rooms
        # room label        
        self.table.attach(Image('Images\\EnvControl\\border.png'), 2, 6, 2, 3)
        Current_Room = Label(ROOMS[0], 'Neuropol 20', "#644080", 0.5, 0.5, gtk.JUSTIFY_CENTER)
        self.table.attach(Current_Room, 6, 8, 2, 3)
        # internal items
        Rooms = ['Blinds ||\nCurtains','Doors','Heating','Light','Stereo  ||\nTelevision','Windows']
        for room in Rooms[:-1]:
            label = Label(room, medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
            self.table.attach(label, x, y, 2, 4)            
            mainmenu_labels.append(label) 
            x += 1
            y += 1                    
        # last item
        label = Label(Rooms[-1], medium_font, lblue, 0.9, 0.8, gtk.JUSTIFY_RIGHT)
        self.table.attach(label, 6, 8, 2, 4)            
        mainmenu_labels.append(label)
        
        # (6) EVENTS & IMAGES: main menu images
        mainmenu_events, mainmenu_imagesOFF, x, y = [], [], 0, 1
        URLs = ['Images\\EnvControl\\Exit_off.png',\
                'Images\\EnvControl\\Switch_off.png',\
                'Images\\EnvControl\\Curtains_off.png',\
                'Images\\EnvControl\\Door_off.png',\
                'Images\\EnvControl\\Heating_off.png',\
                'Images\\EnvControl\\Light_off.png',\
                'Images\\EnvControl\\Television_off.png',\
                'Images\\EnvControl\\Windows_off.png']
        for url in URLs:
            eventbox, image = Event_Image(url, ground)
            self.table.attach(eventbox, x, y, 4, 6)
            mainmenu_events.append(eventbox)
            mainmenu_imagesOFF.append(image)
            x += 1
            y += 1 

        # (7) BUTTONS: list of EC Tasks
        submenu_labels, submenu_buttons= [], []
        for x in range(0,8):
            button, label = Button_Label('', lblue, 'white', medium_font)
            label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
            self.table.attach(button, x, x+1, 6, 8)
            submenu_labels.append(label)
            submenu_buttons.append(button)       
        
        # (8) IMAGES: general menu images for OFF state
        GralIconsOFF = []
        GralIconsOFF.append(Image('Images\\Necessity&Desire\\SNecessities_off.png')) 
        GralIconsOFF.append(Image('Images\\Mobility\\SMobility_off.png'))
        GralIconsOFF.append(Image('Images\\EnvControl\\LHomeControl_off.png'))
        GralIconsOFF.append(Image('Images\\Messenger\\SChat_off.png'))         
        
        # (9) IMAGES: main menu images for ON state
        mainmenu_imagesON = [] 
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Exit_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Switch_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Curtains_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Door_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Heating_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Light_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Television_on.png'))
        mainmenu_imagesON.append(Image('Images\\EnvControl\\Windows_on.png'))
        
        # (10) IMAGE: general menu image for MI state
        self.EC_MI = Image('Images\\EnvControl\\LHomeControl_MI.png')    
        
        #(11) FRAME & LABELS: history of the selected tasks
        frame, label = Frame_Label('HISTORY - Recently Selected Tasks', ground, lblue, small_font, 0, 0.5, gtk.JUSTIFY_CENTER)
        self.table.attach(frame, 0, 8, 8, 9)    
        History_Labels = []
        History_Labels.append(Label('', small_font, 'black', 0.1, 0.9, gtk.JUSTIFY_LEFT))
        self.table.attach(History_Labels[0], 0, 1, 8, 9)
        for index in range(1,8):
            History_Labels.append(Label('', small_font, lblue, 0.1, 0.9, gtk.JUSTIFY_LEFT))
            self.table.attach(History_Labels[index], index, index+1, 8, 9)              
            
        # (12) Widgets assignation to enable them in the following
        #     methods        
        # -- ButtonS
        self.submenu_buttons = submenu_buttons
        # -- ImageS
        self.GralIconsON  = GralIconsON
        self.GralIconsOFF = GralIconsOFF        
        self.mainmenu_imagesOFF = mainmenu_imagesOFF
        self.mainmenu_imagesON  = mainmenu_imagesON
        # -- Events        
        self.mainmenu_events = mainmenu_events
        # -- FrameS
        self.EC_event = EC_event
        # -- LabelS
        self.CueSignals = CueSignals
        self.Current_Room = Current_Room
        self.titulo = titulo
        self.mainmenu_labels = mainmenu_labels        
        self.submenu_labels = submenu_labels
        self.History_Labels = History_Labels
        # -- Variable Declaration
        self.History, self.CUE = ['','','','','','','',''], None


    #..........Method 2: Returning widgets container........
    def EC_container(self):
        'EC table for being appended to the notebook'
        return self.table


    #...............Method 3: EC menu activation............
    def EC_Activation(self, targets):
        '"navigation" and "select" commands switched to EC menu'

        # =======main menu variables initialization=========
        # (1) Current selected button and available message
        self.current_icons = range(8)
        self.current_subuttons = range(8)
        # (2) Submenu default value
        self.selected_subutton = 0
  
        # ============== EC menu modifications =============
        # (1) General menu icons modification to indicate INACCESSIBLE navigation
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))             
        # --- image changes ~ general menu     
        self.table.remove(self.GralIconsON[0])
        self.table.attach(self.GralIconsOFF[0], 2, 3, 0, 2)
        self.table.remove(self.GralIconsON[1])
        self.table.attach(self.GralIconsOFF[1], 3, 4, 0, 2)
        children = self.EC_event.get_children()
        self.EC_event.remove(children[0])       
        self.EC_event.add(self.GralIconsOFF[2])   
        STYLE = self.EC_event.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.EC_event.get_colormap().alloc_color(ground)
        self.EC_event.set_style(STYLE)     
        self.table.remove(self.GralIconsON[3])
        self.table.attach(self.GralIconsOFF[3], 5, 6, 0, 2)           
        # (2) Main Menu Activation
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        # --- image changes
        for index in range(len(self.mainmenu_events)):
            self.mainmenu_events[index].remove(self.mainmenu_imagesOFF[index])
            self.mainmenu_events[index].add(self.mainmenu_imagesON[index])
        # (3) Sub-menu buttons activation
        for item in self.submenu_buttons:
            STYLE = item.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= item.get_colormap().alloc_color(blue)
            item.set_style(STYLE)        
        # (4) Control of EC menu
        HOME = self.EC_Control(targets)        
        return HOME

    
    #........... Method 4: EC menu RE-activation ...........
    def EC_Reactivation(self, targets):
        'Main Menu Reactivation'

        # (1) Resetting the submenu labels
        for item in self.submenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))         
        # (2) Control of EC menu        
        HOME = self.EC_Control(targets)
        return HOME


    #........... Method 5: EC menu deactivation ............
    def EC_Deactivation(self):
        '"navigation" and "select" commands switched to general menu'

        # (1) General menu icons modification to indicate ACCESIBLE navigation
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))        
        # --- image changes ~ general menu     
        self.table.remove(self.GralIconsOFF[0])
        self.table.attach(self.GralIconsON[0], 2, 3, 0, 2)
        self.table.remove(self.GralIconsOFF[1])
        self.table.attach(self.GralIconsON[1], 3, 4, 0, 2)
        children = self.EC_event.get_children()
        self.EC_event.remove(children[0])       
        self.EC_event.add(self.GralIconsON[2])        
        self.table.remove(self.GralIconsOFF[3])
        self.table.attach(self.GralIconsON[3], 5, 6, 0, 2)              
        # (2) Main menu labels Deactivation
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
        self.mainmenu_labels[self.current_icons[0]].modify_font(pango.FontDescription(medium_font))
        # --- image changes
        for index in range(len(self.mainmenu_events)):
            self.mainmenu_events[index].remove(self.mainmenu_imagesON[index])
            self.mainmenu_events[index].add(self.mainmenu_imagesOFF[index])    
        # --- event background deselection
        STYLE = self.mainmenu_events[0].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[0].get_colormap().alloc_color(ground)
        self.mainmenu_events[0].set_style(STYLE)  
        self.mainmenu_labels[0].modify_font(pango.FontDescription(medium_font))          
        # (3) Sub-menu buttons background desactivation
        for item in self.submenu_buttons:
            STYLE = item.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= item.get_colormap().alloc_color(lblue)
            item.set_style(STYLE)
        

    #.............. Method 6: EC menu control ..............
    def EC_Control(self, targets):
        'Control of the EC menu'
        
        # (1) Updating the current selected button
        self.selected_icon = self.current_icons.pop(0)
        self.current_icons.append(self.selected_icon)
        # (2) Subutton labels modification
        ## -- current sub~label
        self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font)) 
        ## -- next sublabel pre-deselection
        self.submenu_labels[self.current_subuttons[0]].modify_font(pango.FontDescription(medium_font)) 
        if self.selected_icon < 2:            
            ## a.- Cue-Driven Systems
            if targets[-1] == self.selected_icon:
                for index in range(8): 
                    ## -- original label
                    label = MainMenu[self.selected_icon][index]
                    ## -- underline~process for Cue-Driven systems
                    if any([target==index for target in targets[:-1]]):
                        # label creation
                        labels = label.split('\n')
                        for i in range(len(labels)): labels[i] = labels[i].replace('','_')[:-1]
                        label = '\n'.join(labels)    
                        # re-design of the subutton
                        self.table.remove(self.submenu_buttons[index])
                        Button, Label = Button_Label(label, blue, 'white', medium_font)
                        Label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
                        self.table.attach(Button, index, index+1, 6, 8)
                        # button & label re-assignment
                        self.submenu_buttons[index], self.submenu_labels[index] = Button, Label            
                    ## -- submenu-labelling
                    else:
                        self.submenu_labels[index].set_label(label)          
            ## b.- Systems different to Cue-Driven systems
            else:       
                for index in range(8): self.submenu_labels[index].set_label(MainMenu[self.selected_icon][index])           
        else:
            room = self.Current_Room.get_text()
            self.room_index = ROOMS.index(room)
            ## a.- Cue-Driven Systems
            if targets[-1] == self.selected_icon:
                for index in range(8): 
                    ## -- original label
                    label = MainMenu[self.selected_icon][self.room_index][index]
                    ## -- underline~process for Cue-Driven systems
                    if any([target==index for target in targets[:-1]]):
                        # label creation
                        labels = label.split('\n')
                        for i in range(len(labels)): labels[i] = labels[i].replace('','_')[:-1]
                        label = '\n'.join(labels)                
                        # re-design of the subutton
                        self.table.remove(self.submenu_buttons[index])
                        Button, Label = Button_Label(label, blue, 'white', medium_font)
                        Label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
                        self.table.attach(Button, index, index+1, 6, 8)
                        # button & label re-assignment
                        self.submenu_buttons[index], self.submenu_labels[index] = Button, Label
                    ## -- submenu-labelling
                    else:
                        self.submenu_labels[index].set_label(label)          
            ## b.- Systems different to Cue-Driven systems
            else:       
                for index in range(8): self.submenu_labels[index].set_label(MainMenu[self.selected_icon][self.room_index][index])
        # (3) Selection and deselection in main menu
        ## -- current icon label selection
        self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))
        self.mainmenu_labels[self.selected_icon].modify_font(pango.FontDescription(medium_font))
        ## -- last icon label deselection
        self.mainmenu_labels[self.current_icons[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        self.mainmenu_labels[self.current_icons[6]].modify_font(pango.FontDescription(medium_font))
        ## -- last event_box background deselection
        STYLE = self.mainmenu_events[self.current_icons[6]].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL] = \
        self.mainmenu_events[self.current_icons[6]].get_colormap().alloc_color(ground)
        self.mainmenu_events[self.current_icons[6]].set_style(STYLE)        
        ## -- current event_box background selection
        STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(blue)
        self.mainmenu_events[self.selected_icon].set_style(STYLE)    
       ## -- different icons from 'Home'
        if self.selected_icon != 0:
            ## a.- commands belong to main menu
            return False
        else: 
            ## b.- commands could belong to general menu
            return True
    
    
    #........... Method 7: EC menu Warning Sign ............
    def EC_WarningSign(self, submenu):
        'Motor Imaginary Movement Preparation'
        
        if submenu: self.Auto_Control()
        # (1) Execution on General Menu
        if not(submenu):            
            # --- event modification              
            STYLE = self.EC_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.EC_event.get_colormap().alloc_color(light_orange)
            self.EC_event.set_style(STYLE)                 
            return 'unknown_task', 'unknown_len'
        # (2) Execution on Main Menu
        else:
            self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(light_orange))                          
            STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(light_orange)
            self.mainmenu_events[self.selected_icon].set_style(STYLE) 
            ## -- length of the current selected submenu
            if self.selected_icon < 2:
                current_len = len([item for item in MainMenu[self.selected_icon] if item != ''])
            else: 
                current_len = len([item for item in MainMenu[self.selected_icon][self.room_index] if item != ''])
            return self.selected_subutton, current_len
    
    
    #........... Method 8: EC menu MI Performance ..........
    def EC_MIPerformance(self, submenu, target):
        'Motor Imaginary Movement Performance - EEG Signal Recording'
        
        # (1) Selection of the appropiate Cue
        if target == 'left':
            self.CUE = self.CueSignals[0]
            self.table.attach(self.CueSignals[0],0, 2, 0, 2)
        elif target == 'right':
            self.CUE = self.CueSignals[1]
            self.table.attach(self.CueSignals[1],0, 2, 0, 2) 
        elif target == 'idle':
            self.CUE = self.CueSignals[2]
            self.table.attach(self.CueSignals[2],0, 2, 0, 2)
        # (2) Execution on General Menu
        if not(submenu):            
            # --- event modification              
            STYLE = self.EC_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.EC_event.get_colormap().alloc_color(orange)
            self.EC_event.set_style(STYLE)                 
        # (3) Execution on Main Menu
        else:
            self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))                          
            STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(orange)
            self.mainmenu_events[self.selected_icon].set_style(STYLE) 
        return


    #........... Method 9: EC menu No Control ..............
    def EC_NoControl(self, submenu, reset):
        'Weak or None Motor Imaginary Movement Performance'
        
        # (1) Execution on General Menu
        if not(submenu):            
            # --- event modification  
            #self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))            
            STYLE = self.EC_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.EC_event.get_colormap().alloc_color(ground)
            self.EC_event.set_style(STYLE)                 
        # (2) Execution on Main Menu
        else:
            ## -- mainmenu labels
            self.mainmenu_labels[self.current_icons[0]].modify_font(pango.FontDescription(medium_font))
            self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))                          
            STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(blue)
            self.mainmenu_events[self.selected_icon].set_style(STYLE) 
            ## -- submenu label
            self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font))
            ## -- reset AutoControl if command != cue
            if reset:
                self.selected_subutton == self.current_subuttons.pop()
                self.current_subuttons.insert(0, self.selected_subutton)
        return 
    

    #............ Method 10: EC menu - Blank  ..............
    def EC_Blank(self, target):
        'Random Inter-trial Inverval'
               
        # (1) Image Removal
        if target == 'left':
            self.table.remove(self.CueSignals[0])
        elif target == 'right':
            self.table.remove(self.CueSignals[1]) 
        elif target == 'idle':
            self.table.remove(self.CueSignals[2])
        # (2) Cue Update
        self.CUE = None

    
    #........... Method 11: EC Gral Icon Reset ..............
    def EC_Reset(self):
        'Resetting before leaving the Current Tab'
        
        # --- event modification              
        STYLE = self.EC_event.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.EC_event.get_colormap().alloc_color(ground)
        self.EC_event.set_style(STYLE)  
    
    
    #.............. Method 12: EC Tab Reset ................
    def EC_ResetALL(self, submenu, tab):
        'Reset of the Whole Tab'

        # (1) Reset of Variables
        self.current_icons = range(8)
        self.current_subuttons = range(8)
        self.selected_subutton = -1 
        # (2) Room-Label
        self.Current_Room.set_text(ROOMS[0])
        # (3) Cue-Removal if any
        if self.CUE != None: self.table.remove(self.CUE)
        # (4) General menu icons modification to indicate ACCESIBLE navigation
        if all([submenu, tab==2]):
            ## -- title colour deselection
            self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))
            # --- image changes ~ general menu     
            self.table.remove(self.GralIconsOFF[0])
            self.table.attach(self.GralIconsON[0], 2, 3, 0, 2)
            self.table.remove(self.GralIconsOFF[1])
            self.table.attach(self.GralIconsON[1], 3, 4, 0, 2)
            children = self.EC_event.get_children()
            self.EC_event.remove(children[0])       
            self.EC_event.add(self.GralIconsON[2])        
            self.table.remove(self.GralIconsOFF[3])
            self.table.attach(self.GralIconsON[3], 5, 6, 0, 2)  
        # (5) MainMenu Deactivation  
        for index in range(len(self.mainmenu_events)):
        ## -- label modifications
            self.mainmenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
            self.mainmenu_labels[index].modify_font(pango.FontDescription(medium_font))
        ## -- image changes
            children = self.mainmenu_events[index].get_children()
            self.mainmenu_events[index].remove(children[0])
            self.mainmenu_events[index].add(self.mainmenu_imagesOFF[index])    
        ## -- event background deselection
            STYLE = self.mainmenu_events[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[index].get_colormap().alloc_color(ground)
            self.mainmenu_events[index].set_style(STYLE)  
        ## -- Sub-menu buttons background desactivation
            STYLE = self.submenu_buttons[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.submenu_buttons[index].get_colormap().alloc_color(lblue)
            self.submenu_buttons[index].set_style(STYLE)            
        ## -- sublabel modifications
            self.submenu_labels[index].set_text('')
            self.submenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
            self.submenu_labels[index].modify_font(pango.FontDescription(medium_font))     
        # (6) History of the Selected Tasks
        for widget in self.History_Labels: widget.set_text('')
        self.History = ['','','','','','','','']


    #............... Method 13: EC menu writer .............
    def EC_Writing(self):
        'GUI~VE control command writer'
        
        # (1) No available submenu~labels
        conditions = [widget.get_text() == '' for widget in self.submenu_labels]
        # (2) Main Menu Update
        ## -- current label
        self.mainmenu_labels[self.selected_icon].modify_font(pango.FontDescription(medium_font)) 
        self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))                          
        STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(blue)
        self.mainmenu_events[self.selected_icon].set_style(STYLE)
        ## -- next label pre-deselection
        self.mainmenu_labels[self.current_icons[0]].modify_font(pango.FontDescription(medium_font))
        # (3) Selecting a task
        ## -- return to the orginal format
        self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font))    
        ## ===== return =====
        if all(conditions): return '_'.join(['2',str(self.selected_icon),'none'])
        ## -- subutton background
        STYLE = self.submenu_buttons[self.selected_subutton].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]=self.submenu_buttons[self.selected_subutton].get_colormap().alloc_color('white')
        self.submenu_buttons[self.selected_subutton].set_style(STYLE)         
        ## -- sublabel selection   
        self.submenu_labels[self.selected_subutton].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))     
        # (4) Updating the History of the selected tasks
        label = self.submenu_labels[self.selected_subutton].get_text() 
        label = label.replace('_', '')
        self.submenu_labels[self.selected_subutton].set_text(label)
        # (5) Updating the History of the selected tasks
        self.History.pop()
        self.History.insert(0, label)   
        for index in range(len(self.History)): self.History_Labels[index].set_text(self.History[index])
        # (6) Number of the current tab (TCP message)
        GUI_VE = []
        GUI_VE.append('2')
        ## -- Number of the current icon
        GUI_VE.append(str(self.selected_icon))
        ## -- Updating the room label
        if self.selected_icon == 1: self.Current_Room.set_text(ROOMS[self.selected_subutton])
        ## -- Number of the current subutton
        GUI_VE.append(str(self.selected_subutton))
        return ''.join(GUI_VE)
        

    #.......Method 14: Automatic Control of the Submenu.....
    def Auto_Control(self):
        'Auto-Selection of the subuttons menu'

        # (1) Button selection in main~menu
        self.mainmenu_labels[self.current_icons[0]].modify_font(pango.FontDescription(font)) 
        self.mainmenu_labels[self.current_icons[-1]].modify_font(pango.FontDescription(medium_font)) 
        ## -- No available submenu~labels
        conditions = [widget.get_text() == '' for widget in self.submenu_labels]
        ## -- Menu == Exit
        condition  = self.mainmenu_labels[self.selected_icon].get_text().lower() == 'exit'
        if any([condition, all(conditions)]): return
        # (2) Subutton & Sublabel selection in sub~menu
        for i in range(8):
            # (3) Updating the current selected subutton
            self.selected_subutton = self.current_subuttons.pop(0)
            self.current_subuttons.append(self.selected_subutton)
            # (4) Button deselection in sub~menu 
            STYLE = self.submenu_buttons[self.current_subuttons[6]].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]=self.submenu_buttons[self.current_subuttons[6]].get_colormap().alloc_color(blue)
            self.submenu_buttons[self.current_subuttons[6]].set_style(STYLE)        
            ## -- sublabel deselection
            self.submenu_labels[self.current_subuttons[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))                  
            self.submenu_labels[self.current_subuttons[6]].modify_font(pango.FontDescription(medium_font)) 
            ## -- current subutton font selection                                         
            self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(font))
            if self.submenu_labels[self.selected_subutton].get_text() != '': break              
                                        