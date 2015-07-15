### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### August 24th, 2010

# ****************************
# * Graphical User Interface:*
# *      'MOBILITY MENU'     *
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
from Constructors import Image,Label,Frame,Frame_Image,Event_Image,Frame_Label


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL VARIABLES DECLARATION
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
# (2) Room-Labels
room_labels = ['Entrance', 'Kitchen', 'My Bedroom', 'Bathroom', 'Carer-Room', 'Living-Room']
room_len    = {'Entrance':2, 'Kitchen':5, 'My Bedroom':11, 'Bathroom':13, 'Carer-Room':16, 'Living-Room':20}


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "mob_menu" CLASS DECLARATION

class mob_menu():
    'Class to control the "Mobility" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "Mobility" menu'
        
        # =============Mobility tab creation===============        
        # (1) TABLE: Widget container
        ## --9 x 8 table creation
        self.table = gtk.Table(9, 8, True)
        self.table.show()
        
        # (2) LABEL: Window title
        titulo = Label('Mobility', 'Neuropol 31', orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
        self.table.attach(titulo, 6, 8, 0, 2)
        
        # (3) FRAMES & IMAGES: General menu images
        GralIconsON = []
        ## --'Necessities and Desires' option
        url = 'Images\\Necessity&Desire\\SNecessities_on.png'
        GralIconsON.append(Image(url))
        self.table.attach(GralIconsON[0], 2, 3, 0, 2)
        ## --'Mobility' option
        url = 'Images\\Mobility\\LMobility_on.png'
        mob_event, mob_image = Event_Image(url, ground)
        mob_event.set_border_width(10)
        GralIconsON.append(mob_image)
        self.table.attach(mob_event, 3, 4, 0, 2)
        ## --'Environmental Control' option
        url = 'Images\\EnvControl\\SHomeControl_on.png'
        GralIconsON.append(Image(url))
        self.table.attach(GralIconsON[2], 4, 5, 0, 2)
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

        # (5) EVENTS & IMAGES: Room Selection
        mainmenu_icons, mainmenu_imagesOFF = [], []
        # --- exit
        eventbox, image = Event_Image('Images\\Mobility\\Exit_off.png', ground)
        eventbox.set_size_request(95, 95)
        self.table.attach(eventbox, 0, 1, 3, 5)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)        
        # --- caregiver's room
        eventbox, image = Event_Image('Images\\Mobility\\BedRoom2_off.png', ground)
        eventbox.set_size_request(250, 95)
        self.table.attach(eventbox, 1, 3, 3, 5)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)        
        # --- bathroom
        eventbox, image = Event_Image('Images\\Mobility\\BathRoom_off.png', ground)
        eventbox.set_size_request(250, 95)
        self.table.attach(eventbox, 3, 5, 3, 5)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)        
        # ---my bedroom
        eventbox, image = Event_Image('Images\\Mobility\\BedRoom1_off.png', ground)
        eventbox.set_size_request(250, 95)
        self.table.attach(eventbox, 5, 7, 3, 5)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)     
        # --- exit
        eventbox, image = Event_Image('Images\\Mobility\\Exit_off.png', ground)
        eventbox.set_size_request(95, 95)
        self.table.attach(eventbox, 7, 8, 3, 5)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image) 
        # --- living room
        eventbox, image = Event_Image('Images\\Mobility\\LivingRoom_off.png', ground)
        eventbox.set_size_request(250, 95)
        self.table.attach(eventbox, 1, 3, 5, 7)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)    
        # --- entrance
        eventbox, image = Event_Image('Images\\Mobility\\Entrance_off.png', ground)
        eventbox.set_size_request(250, 95)
        self.table.attach(eventbox, 3, 5, 5, 7)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)   
        # --- kitchen
        eventbox, image = Event_Image('Images\\Mobility\\Kitchen_off.png', ground)
        eventbox.set_size_request(250, 95)
        self.table.attach(eventbox, 5, 7, 5, 7)
        mainmenu_icons.append(eventbox)
        mainmenu_imagesOFF.append(image)         
                
        # (6) LABELS: Icon labels for main menu
        mainmenu_labels = []
        # --- exit
        label = Label('Exit', medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
        label.set_size_request(95, 20)
        self.table.attach(label, 0, 1, 2, 3)
        mainmenu_labels.append(label)          
        # --- caregiver's room
        label = Label('Carer-Room', medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
        label.set_size_request(250, 20)
        self.table.attach(label, 1, 3, 2, 3)
        mainmenu_labels.append(label)          
        # --- bathroom
        label = Label('Bathroom', medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
        label.set_size_request(250, 20)
        self.table.attach(label, 3, 5, 2, 3)
        mainmenu_labels.append(label)       
        # ---my bedroom
        label = Label('My Bedroom', medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
        label.set_size_request(250, 20)
        mainmenu_labels.append(label)        
        self.table.attach(label, 5, 7, 2, 3)
        # --- exit        
        label = Label('Exit', medium_font, lblue, 0.5, 0.8, gtk.JUSTIFY_CENTER)
        eventbox.set_size_request(95, 20)
        mainmenu_labels.append(label)
        self.table.attach(label, 7, 8, 2, 3)        
        # --- living room
        label = Label('Living-Room', medium_font, lblue, 0.5, 0.2, gtk.JUSTIFY_CENTER)
        label.set_size_request(250, 20)
        mainmenu_labels.append(label)        
        self.table.attach(label, 1, 3, 7, 8)    
        # --- entrance
        label = Label('Entrance', medium_font, lblue, 0.5, 0.2, gtk.JUSTIFY_CENTER)
        label.set_size_request(250, 20)
        mainmenu_labels.append(label)        
        self.table.attach(label, 3, 5, 7, 8)
        # --- kitchen
        label = Label('Kitchen', medium_font, lblue, 0.5, 0.2, gtk.JUSTIFY_CENTER)
        label.set_size_request(250, 20)
        mainmenu_labels.append(label)        
        self.table.attach(label, 5, 7, 7, 8)
        
        
        # (7) IMAGES: general menu images for OFF state
        GralIconsOFF = []
        GralIconsOFF.append(Image('Images\\Necessity&Desire\\SNecessities_off.png'))
        GralIconsOFF.append(Image('Images\\Mobility\\LMobility_off.png'))
        GralIconsOFF.append(Image('Images\\EnvControl\\SHomeControl_off.png'))
        GralIconsOFF.append(Image('Images\\Messenger\\SChat_off.png'))         
        
        # (8) IMAGES: main menu images for ON state
        mainmenu_imagesON = []
        mainmenu_imagesON.append(Image('Images\\Mobility\\Exit_on.png'))
        mainmenu_imagesON.append(Image('Images\\Mobility\\BedRoom2_on.png'))
        mainmenu_imagesON.append(Image('Images\\Mobility\\BathRoom_on.png'))        
        mainmenu_imagesON.append(Image('Images\\Mobility\\BedRoom1_on.png'))
        mainmenu_imagesON.append(Image('Images\\Mobility\\Exit_on.png'))
        mainmenu_imagesON.append(Image('Images\\Mobility\\LivingRoom_on.png'))
        mainmenu_imagesON.append(Image('Images\\Mobility\\Entrance_on.png'))
        mainmenu_imagesON.append(Image('Images\\Mobility\\Kitchen_on.png'))
        mainmenu_selection = []
        mainmenu_selection.append(Image('Images\\Mobility\\Exit.png'))
        mainmenu_selection.append(Image('Images\\Mobility\\BedRoom2.png'))
        mainmenu_selection.append(Image('Images\\Mobility\\BathRoom.png'))        
        mainmenu_selection.append(Image('Images\\Mobility\\BedRoom1.png'))
        mainmenu_selection.append(Image('Images\\Mobility\\Exit.png'))
        mainmenu_selection.append(Image('Images\\Mobility\\LivingRoom.png'))
        mainmenu_selection.append(Image('Images\\Mobility\\Entrance.png'))
        mainmenu_selection.append(Image('Images\\Mobility\\Kitchen.png'))         
        
        # (9) IMAGE: general menu image for MI state
        self.mob_MI = Image('Images\\Mobility\\LMobility_MI.png')         
        
        # (10) FRAME & LABELS: history of the selected tasks
        frame, label = Frame_Label('HISTORY - Recently Selected Places', ground, lblue, small_font, 0, 0.5, gtk.JUSTIFY_CENTER)
        self.table.attach(frame, 0, 8, 8, 9)
        History_Labels = []
        History_Labels.append(Label('', small_font, 'black', 0.1, 0.6, gtk.JUSTIFY_LEFT))
        self.table.attach(History_Labels[0], 0, 1, 8, 9)
        for index in range(1,8):
            History_Labels.append(Label('', small_font, lblue, 0.1, 0.6, gtk.JUSTIFY_LEFT))
            self.table.attach(History_Labels[index], index, index+1, 8, 9)      
 
        #(11) Widgets assignation to enable them in following
        #     methods
        ## -- ContainerS      
        self.mainmenu_icons = mainmenu_icons
        self.mob_event = mob_event
        ## -- ImageS
        self.CueSignals = CueSignals
        self.GralIconsON  = GralIconsON
        self.GralIconsOFF = GralIconsOFF
        self.mainmenu_imagesON  = mainmenu_imagesON
        self.mainmenu_imagesOFF = mainmenu_imagesOFF
        self.mainmenu_selection = mainmenu_selection
        ## -- LabelS
        self.mainmenu_labels = mainmenu_labels
        self.titulo = titulo
        self.History_Labels = History_Labels
        ## -- Variable Declaration
        self.History, self.CUE = ['','','','','','','',''], None


    #..........Method 2: Returning widgets container........

    def mob_container(self):
        'Mobility table for being appended to the notebook'
        return self.table


    #............Method 3: Mobility menu activation.........
    def mob_Activation(self):
        '"navigation" and "select" commands switched to Mobility menu'

        # =======main menu variables initialization=========
        # (1) Current selected button and available message
        self.current_labels = range(8)

        # ============Mobility menu modifications===========
        # (1) General menu icons modification to indicate INACCESSIBLE navigation
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
        # --- image changes ~ general menu     
        self.table.remove(self.GralIconsON[0])
        self.table.attach(self.GralIconsOFF[0], 2, 3, 0, 2)
        children = self.mob_event.get_children()
        self.mob_event.remove(children[0])       
        self.mob_event.add(self.GralIconsOFF[1])
        STYLE = self.mob_event.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mob_event.get_colormap().alloc_color(ground)
        self.mob_event.set_style(STYLE)
        self.table.remove(self.GralIconsON[2])
        self.table.attach(self.GralIconsOFF[2], 4, 5, 0, 2)
        self.table.remove(self.GralIconsON[3])
        self.table.attach(self.GralIconsOFF[3], 5, 6, 0, 2)                    
        # (2) Main Menu Activation
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        # --- image changes
        for index in range(len(self.mainmenu_icons)):
            self.mainmenu_icons[index].remove(self.mainmenu_imagesOFF[index])
            self.mainmenu_icons[index].add(self.mainmenu_imagesON[index])
        if self.History[0] != '': 
            labels = []
            for widget in self.mainmenu_labels: labels.append(widget.get_text())
            index = labels.index(self.History[0])
            self.mainmenu_icons[index].remove(self.mainmenu_imagesON[index])
            self.mainmenu_icons[index].add(self.mainmenu_selection[index])
        # (3) Control of Mobility menu
        HOME = self.mob_Control()
        return HOME
    
        
    #..........Method 4: Mobility menu RE-activation........
    def mob_Reactivation(self):
        'Main Menu Reactivation'

        # (1) Control of Mobility menu
        HOME = self.mob_Control()
        return HOME


    #..........Method 5: Mobility menu deactivation.........
    def mob_Deactivation(self):
        '"navigation" and "select" commands switched to general menu'

        # (1) General menu icons modification to indicate ACCESIBLE navigation 
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))
        # --- image changes
        self.table.remove(self.GralIconsOFF[0])
        self.table.attach(self.GralIconsON[0], 2, 3, 0, 2)
        self.mob_event.remove(self.GralIconsOFF[1])
        self.mob_event.add(self.GralIconsON[1])
        self.table.remove(self.GralIconsOFF[2])
        self.table.attach(self.GralIconsON[2], 4, 5, 0, 2)
        self.table.remove(self.GralIconsOFF[3])
        self.table.attach(self.GralIconsON[3], 5, 6, 0, 2)        
        # (2) Main menu labels Deactivation
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
        self.mainmenu_labels[self.current_labels[0]].modify_font(pango.FontDescription(medium_font))
        # --- image changes
        for index in range(len(self.mainmenu_icons)):
            children = self.mainmenu_icons[index].get_children()
            self.mainmenu_icons[index].remove(children[0])            
            self.mainmenu_icons[index].add(self.mainmenu_imagesOFF[index]) 
        # --- event background deselection        
        self.mainmenu_labels[0].modify_font(pango.FontDescription(medium_font)) 
        STYLE = self.mainmenu_icons[0].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[0].get_colormap().alloc_color(ground)
        self.mainmenu_icons[0].set_style(STYLE)       
        self.mainmenu_labels[4].modify_font(pango.FontDescription(medium_font))
        STYLE = self.mainmenu_icons[4].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[0].get_colormap().alloc_color(ground)
        self.mainmenu_icons[4].set_style(STYLE)
 
 
    #.............Method 6: Mobility menu control...........
    def mob_Control(self):
        'Control of the Mobility menu'
        
        # (1) Updating the current selected label
        self.selected_label = self.current_labels.pop(0)
        self.current_labels.append(self.selected_label)
        # (2) Selection and deselection in main menu
        # -- deselection of the previous label
        self.mainmenu_labels[self.current_labels[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        self.mainmenu_labels[self.current_labels[6]].modify_font(pango.FontDescription(medium_font))
        # -- deselection of the previous button
        STYLE = self.mainmenu_icons[self.current_labels[6]].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[self.current_labels[6]].get_colormap().alloc_color(ground)
        self.mainmenu_icons[self.current_labels[6]].set_style(STYLE)
        # -- selection of the current label & background
        self.mainmenu_labels[self.selected_label].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))
        self.mainmenu_labels[self.selected_label].modify_font(pango.FontDescription(medium_font))  
        STYLE = self.mainmenu_icons[self.selected_label].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[self.selected_label].get_colormap().alloc_color(blue)
        self.mainmenu_icons[self.selected_label].set_style(STYLE)
        # -- different icons from 'Home'
        if (self.selected_label != 0) and (self.selected_label != 4):
            ## a.- commands belong to main menu
            return False
        else:
            ## b.- commands could belong to general menu
            return True
    
    
    #.........Method 7: Mobility menu Warning Sign...........
    def mob_WarningSign(self, submenu):
        'Motor Imaginary Movement Preparation'
        
        # (1) Execution on General Menu
        if not(submenu):    
            # --- frame modification        
            STYLE = self.mob_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mob_event.get_colormap().alloc_color(light_orange)
            self.mob_event.set_style(STYLE) 
            return 'unknown_task', 'unknown_len'                            
        # (2) Execution on Main Menu
        else:
            # --- current selection
            self.mainmenu_labels[self.selected_label].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(light_orange))  
            STYLE = self.mainmenu_icons[self.selected_label].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[self.selected_label].get_colormap().alloc_color(light_orange)
            self.mainmenu_icons[self.selected_label].set_style(STYLE)         
            # --- pre~selection of the next label
            self.mainmenu_labels[self.current_labels[0]].modify_font(pango.FontDescription(font))          
            return 'unknown_task', 'unknown_len'
    
    
    #.........Method 8: Mobility menu MI Performance........
    def mob_MIPerformance(self, submenu, target):
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
            # --- frame modification        
            STYLE = self.mob_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mob_event.get_colormap().alloc_color(orange)
            self.mob_event.set_style(STYLE)                             
        # (3) Execution on Main Menu
        else:
            self.mainmenu_labels[self.selected_label].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange)) 
            STYLE = self.mainmenu_icons[self.selected_label].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[self.selected_label].get_colormap().alloc_color(orange)
            self.mainmenu_icons[self.selected_label].set_style(STYLE)                        
        return


    #......... Method 9: Mobility menu No Control ..........
    def mob_NoControl(self, submenu):
        'Weak or None Motor Imaginary Movement Performance'
        
        # (1) Execution on General Menu
        if not(submenu):            
            # --- frame modification        
            STYLE = self.mob_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mob_event.get_colormap().alloc_color(ground)
            self.mob_event.set_style(STYLE)                
        # (2) Execution on Main Menu
        else:
            self.mainmenu_labels[self.current_labels[0]].modify_font(pango.FontDescription(medium_font))
            self.mainmenu_labels[self.selected_label].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue)) 
            STYLE = self.mainmenu_icons[self.selected_label].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[self.selected_label].get_colormap().alloc_color(blue)
            self.mainmenu_icons[self.selected_label].set_style(STYLE)            
        return 

    
    #.......... Method 10: Mobility menu - Blank  ..........
    def mob_Blank(self, target):
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
    
    
    #.........Method 11: Mobility Gral Icon Reset............
    def mob_Reset(self):
        'Resetting before leaving the Current Tab'
        
        # --- frame modification        
        STYLE = self.mob_event.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mob_event.get_colormap().alloc_color(ground)
        self.mob_event.set_style(STYLE)
    
    
    #............Method 12: Mobility Tab Reset..............
    def mob_ResetALL(self, submenu, tab):
        'Reset of the Whole Tab'

        # (1) Reset of Variables
        self.current_labels = range(8)
        self.selected_label = 0     
        # (2) Cue-Removal if any
        if self.CUE != None: self.table.remove(self.CUE)
        # (3) General menu icons modification to indicate ACCESIBLE navigation
        if all([submenu, tab==1]):
            ## -- title colour deselection
            self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))
            ## -- image changes
            # --- image changes
            self.table.remove(self.GralIconsOFF[0])
            self.table.attach(self.GralIconsON[0], 2, 3, 0, 2)
            self.mob_event.remove(self.GralIconsOFF[1])
            self.mob_event.add(self.GralIconsON[1])
            self.table.remove(self.GralIconsOFF[2])
            self.table.attach(self.GralIconsON[2], 4, 5, 0, 2)
            self.table.remove(self.GralIconsOFF[3])
            self.table.attach(self.GralIconsON[3], 5, 6, 0, 2)  
        # (4) MainMenu Deactivation  
        for index in range(len(self.mainmenu_icons)):
        ## -- label modifications
            self.mainmenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
            self.mainmenu_labels[index].modify_font(pango.FontDescription(medium_font))
        ## -- image changes
            children = self.mainmenu_icons[index].get_children()
            self.mainmenu_icons[index].remove(children[0])
            self.mainmenu_icons[index].add(self.mainmenu_imagesOFF[index])    
        ## -- event background deselection
            STYLE = self.mainmenu_icons[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[index].get_colormap().alloc_color(ground)
            self.mainmenu_icons[index].set_style(STYLE)    
        # (5) History of the Selected Tasks
        for widget in self.History_Labels: widget.set_text('')
        self.History = ['','','','','','','','']
        

    #.............Method 13: Mobility menu writer...........
    def mob_Writing(self):
        'GUI~VE control command writer'
        
        # (1) Variable Declaration
        ## -- Number of the current tab
        GUI_VE = []
        GUI_VE.append('1')
        ## -- Number of the current button
        GUI_VE.append(str(self.selected_label))
        ## -- Previous and Current Room_Labels         
        prelabel = self.History[0]
        label = self.mainmenu_labels[self.selected_label].get_text()
        ## -- Visual Feedback Variables
        if prelabel == '': prelabel = 'Entrance'
        # video length
        video_len = 0
        if prelabel != label:
            while prelabel != room_labels[0]: room_labels.append(room_labels.pop(0))
            label_idx = room_labels.index(label)
            for index in range(1, label_idx+1): video_len += room_len[room_labels[index]]
        # (2) Main Menu Update
        ## -- current label
        self.mainmenu_labels[self.selected_label].modify_font(pango.FontDescription(medium_font))
        self.mainmenu_labels[self.selected_label].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))                          
        STYLE = self.mainmenu_icons[self.selected_label].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_icons[self.selected_label].get_colormap().alloc_color(blue)
        self.mainmenu_icons[self.selected_label].set_style(STYLE) 
        ## -- next label pre-deselection
        self.mainmenu_labels[self.current_labels[0]].modify_font(pango.FontDescription(medium_font))
        # (3) Selection of the appropriate Room & Video-Duration calculation       
        prelabel, labels = self.History[0], [] 
        if prelabel != label:
            ## -- room selection
            self.mainmenu_icons[self.selected_label].remove(self.mainmenu_imagesON[self.selected_label])
            self.mainmenu_icons[self.selected_label].add(self.mainmenu_selection[self.selected_label])            
        # (4) Removing previous selection
            if prelabel != '':
                for widget in self.mainmenu_labels: labels.append(widget.get_text())
                prelabel_idx = labels.index(prelabel)
                self.mainmenu_icons[prelabel_idx].remove(self.mainmenu_selection[prelabel_idx])
                self.mainmenu_icons[prelabel_idx].add(self.mainmenu_imagesON[prelabel_idx])                                
        # (5) Updating the History of the selected tasks
            self.History.pop()
            self.History.insert(0, label)   
            for index in range(len(self.History)): self.History_Labels[index].set_text(self.History[index])                       
        return ''.join(GUI_VE), video_len




