### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### February 4th, 2011

# **********************************
# *   Graphical User Interface:    *
# *   'USER-TUTORIAL SYSTEM'       *
# **********************************

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
# (1) Sound signal
well = 'Sounds\\WellDone.wav'
# (2) Format constants
black = '#213240'
blue = '#466289'
lblue = '#A0AEC1'
orange = '#FA6121'
light_orange = '#FABF8F'
ground = '#DCDCDC'
font = "Century Gothic 24"
medium_font = "Century Gothic 17"
small_font = "Century Gothic 10"
# (3) Main menu list
MainMenu = ['MENU 1','MENU 2','MENU 3','MENU 4', 'MENU 5', 'MENU 6', 'MENU 7', 'EXIT']
# (4) Submenu dictionary (sub-buttons labels)
SubMenu = { 0: ['Task 1.1','Task 1.2','Task 1.3','Task 1.4','Task 1.5','Task 1.6','Task 1.7','Task 1.8'],\
            1: ['Task 2.1','Task 2.2','Task 2.3','Task 2.4','Task 2.5','Task 2.6','Task 2.7','Task 2.8'],\
            2: ['Task 3.1','Task 3.2','Task 3.3','Task 3.4','Task 3.5','Task 3.6','Task 3.7','Task 3.8'],\
            3: ['Task 4.1','Task 4.2','Task 4.3','Task 4.4','Task 4.5','Task 4.6','Task 4.7','Task 4.8'],\
            4: ['Task 5.1','Task 5.2','Task 5.3','Task 5.4','Task 5.5','Task 5.6','Task 5.7','Task 5.8'],\
            5: ['Task 6.1','Task 6.2','Task 6.3','Task 6.4','Task 6.5','Task 6.6','Task 6.7','Task 6.8'],\
            6: ['Task 7.1','Task 7.2','Task 7.3','Task 7.4','Task 7.5','Task 7.6','Task 7.7','Task 7.8'],\
            7: ['','','','','','','','']}


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "cal_menu" CLASS DECLARATION

class UT_menu():
    'Class to control the "User-Tutorial" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "User-Tutorial" menu'
        
        # ============User-Tutorial tab creation==============        
        # (1) TABLE: Widget container
        ## --9 x 8 table creation
        self.table = gtk.Table(9, 8, False)
        self.table.show()
        
        # (2) LABEL: Window title
        titulo = Label('Menu 1', 'Neuropol 33', orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)        
        titulo.hide()
        self.table.attach(titulo, 6, 8, 0, 2) 

        # (3) IMAGES: Icons for cue indication (Tutorial_MI mode)
        CueSignals = [[],[]]
        # -- cue: MI preparation
        url = 'Images\\User_Tutorial\\cue_warning.png'
        image = Image(url)        
        CueSignals[0].append(image)        
        # -- cue: Left MI performance
        url = 'Images\\User_Tutorial\\cue_left.png'
        image = Image(url)
        CueSignals[0].append(image)        
        # -- cue: Right MI performance
        url = 'Images\\User_Tutorial\\cue_right.png'
        image = Image(url)
        CueSignals[0].append(image) 
        # -- cue: Idle MI performance
        url = 'Images\\User_Tutorial\\cue_idle.png'
        image = Image(url)
        CueSignals[0].append(image)      
        
        # (4) IMAGES: Icons for cue indication (Tutorial_CMD mode)     
        # -- cue: Left MI performance
        url = 'Images\\User_Tutorial\\left.png'
        image = Image(url)
        CueSignals[1].append(image)        
        # -- cue: Right MI performance
        url = 'Images\\User_Tutorial\\right.png'
        image = Image(url)
        CueSignals[1].append(image) 
        # -- cue: Idle MI performance
        url = 'Images\\User_Tutorial\\idle.png'
        image = Image(url)
        CueSignals[1].append(image)             
        
        # (5) IMAGES: General menu images
        MiniIconsON, GralEvents = [], []
        for index in range(2,6):
            url = 'Images\\User_Tutorial\\minimenu_on.png'
            event, image = Event_Image(url, ground)
            event.hide()
            MiniIconsON.append(image)
            GralEvents.append(event)
            self.table.attach(event, index, index+1, 0, 2)  
        
        # (6) LABELS: main menu labels
        mainmenu_labels, x, y = [], 0, 1
        Mnum = 'TAB  1'.split()[-1]
        for item in MainMenu:
            if item.lower() != 'exit':
                rename= item.split(' ')
                rename= [rename[0], '\n', Mnum, '.', rename[-1]]
                item  = ''.join(rename)
            label = Label(item, medium_font, lblue, 0.5, 0.9, gtk.JUSTIFY_CENTER)
            label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
            label.hide()
            mainmenu_labels.append(label) 
            self.table.attach(label, x, y, 2, 4)
            x += 1
            y += 1       
                        
        # (7) IMAGES: main menu images
        mainmenu_events, mainmenu_imagesOFF = [], []
        for index in range(7):
            url = 'Images\\User_Tutorial\\option_off.png'
            event, image = Event_Image(url, ground)
            event.hide()
            mainmenu_events.append(event)
            mainmenu_imagesOFF.append(image)
            self.table.attach(event, index, index+1, 4, 6)
        url = 'Images\\User_Tutorial\\Exit_off.png'
        event, image = Event_Image(url, ground)
        event.hide()
        mainmenu_events.append(event)
        mainmenu_imagesOFF.append(image)
        self.table.attach(event, 7, 8, 4, 6)

        # (8) BUTTONS: list of tasks
        submenu_labels, submenu_buttons= [], []
        for x in range(0,8):
            button, label = Button_Label('', lblue, 'white', medium_font)
            label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
            button.hide()
            self.table.attach(button, x, x+1, 6, 8)
            submenu_labels.append(label)
            submenu_buttons.append(button)       
        
        # (9) IMAGES: menu images for OFF or ON states
        MiniIconsOFF, GralIconsON, GralIconsOFF, mainmenu_imagesON, submenu_imagesON = [], [], [], [], []
        for index in range(4):
            MiniIconsOFF.append(Image('Images\\User_Tutorial\\minimenu_off.png')) 
            GralIconsON.append(Image('Images\\User_Tutorial\\menu_on.png')) 
            GralIconsOFF.append(Image('Images\\User_Tutorial\\menu_off.png'))                 
        for index in range(7): mainmenu_imagesON.append(Image('Images\\User_Tutorial\\option_on.png'))
        mainmenu_imagesON.append(Image('Images\\User_Tutorial\\Exit_on.png'))
        for index in range(8): submenu_imagesON.append(Image('Images\\User_Tutorial\\task_on.png'))
               
        # (10) FRAME & LABELS: history of the selected tasks
        self.History_Frame, label = Frame_Label('HISTORY - Recently Selected Tasks', ground, lblue, small_font, 0, 0.5, gtk.JUSTIFY_CENTER)
        self.History_Frame.hide()
        self.table.attach(self.History_Frame, 0, 8, 8, 9)
        History_Labels = []
        History_Labels.append(Label('', small_font, 'black', 0.1, 0.7, gtk.JUSTIFY_LEFT))
        self.table.attach(History_Labels[0], 0, 1, 8, 9)
        for index in range(1,8):
            History_Labels.append(Label('', small_font, lblue, 0.1, 0.7, gtk.JUSTIFY_LEFT))
            self.table.attach(History_Labels[index], index, index+1, 8, 9) 
        for widget in History_Labels: widget.hide()
        
        #(11)Widgets assignation to enable them in the following
        #    methods        
        # -- ImageS
        self.CueSignals = CueSignals
        self.MiniIconsON = MiniIconsON
        self.MiniIconsOFF = MiniIconsOFF 
        self.GralIconsON = GralIconsON
        self.GralIconsOFF = GralIconsOFF
        self.mainmenu_imagesOFF = mainmenu_imagesOFF
        self.mainmenu_imagesON  = mainmenu_imagesON        
        # -- Events        
        self.GralEvents = GralEvents
        self.mainmenu_events = mainmenu_events
        # -- Labels
        self.mainmenu_labels= mainmenu_labels
        self.submenu_labels = submenu_labels
        self.History_Labels = History_Labels
        self.titulo = titulo
        # -- ButtonS
        self.submenu_buttons = submenu_buttons    
        # -- Variable Declaration
        self.History = ['','','','','','','','']   


    #..........Method 2: Returning widgets container........
    def UT_container(self):
        'User_Tutorial table for being appended to the notebook'
        
        return self.table
    
    
    #.. Method 3: System Preconfiguration - CMD Tutorial ...
    def UT_CMDSysConfig(self):
        'Configuration of the Command-Tutorial System: \
         1) Widget Visibility & 2) Variable Declaration'
        
        # (1) Control variable declaration
        self.gralmenu_indexes = range(4)
        self.current_menu = self.gralmenu_indexes.pop(0)
        self.gralmenu_indexes.append(self.current_menu)
        self.Titles = ['TAB  1','TAB  2','TAB  3','TAB  4']
        # --- Current selected button and available message
        self.current_icons = range(8)
        self.current_subuttons = range(8)
        # (2) Table Re-Size
        self.table.set_homogeneous(True)
        # (3) Reset Procedure
        # --- titulo set
        self.titulo.set_text(self.Titles[0])
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))
        # --- image changes        
        children = self.GralEvents[self.current_menu].get_children()
        self.GralEvents[self.current_menu].remove(children[0])
        self.GralEvents[self.current_menu].add(self.GralIconsON[self.current_menu])        
        for index in range(1, len(self.GralEvents)):   
            children = self.GralEvents[index].get_children()
            self.GralEvents[index].remove(children[0])       
            self.GralEvents[index].add(self.MiniIconsON[index])     
        # --- mainmenu-label/image/event modifications
        Mnum = self.Titles[0].split(' ')[-1]
        for index in range(len(self.mainmenu_events)):
            # labels
            label = MainMenu[index]
            if label.lower() != 'exit':
                label = label.split(' ')
                label = [label[0], '\n', Mnum, '.', label[-1]]
                label = ''.join(label)
            self.mainmenu_labels[index].set_text(label)
            self.mainmenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
            self.mainmenu_labels[index].modify_font(pango.FontDescription(medium_font)) 
            # images       
            children = self.mainmenu_events[index].get_children()
            self.mainmenu_events[index].remove(children[0])
            self.mainmenu_events[index].add(self.mainmenu_imagesOFF[index])    
            # events
            STYLE = self.mainmenu_events[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[index].get_colormap().alloc_color(ground)
            self.mainmenu_events[index].set_style(STYLE)                            
        # --- Sub-menu buttons background desactivation
            # labels
            self.submenu_labels[index].set_text('')
            self.submenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
            self.submenu_labels[index].modify_font(pango.FontDescription(medium_font)) 
            # events
            STYLE = self.submenu_buttons[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL] = self.submenu_buttons[index].get_colormap().alloc_color(lblue)
            self.submenu_buttons[index].set_style(STYLE)
        # --- history of the selected tasks
        for widget in self.History_Labels: widget.set_text('')
        self.History = ['','','','','','','','']
        # (4) Widget Visibility
        self.titulo.show()
        for widget in self.GralEvents: widget.show()
        for widget in self.mainmenu_labels: widget.show()
        for widget in self.mainmenu_events: widget.show()
        for widget in self.submenu_buttons: widget.show()
        for widget in self.History_Labels:  widget.show()
        self.History_Frame.show()    
        return False

    #...... Method 4: Warning Sign for the Tutorial_MI .....
    def UT_WarningMI(self):
        'Warning for the MI of the User_Tutorial'

        # (1) Image attachment   
        self.table.attach(self.CueSignals[0][0],2, 6, 2, 6)    
    
    
    #.....Method 5: Warning Sign for the COMMAND Stage......
    def UT_WarningCMD(self, submenu):
        'Warning for the COMMAND part of the User_Tutorial'

        # (1) Automatic Selection Initialization
        if submenu: self.Auto_Control()
        # (2) Event Background Modification 
        # --- Execution on General Menu
        if not(submenu):            
            STYLE = self.GralEvents[self.current_menu].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.GralEvents[self.current_menu].get_colormap().alloc_color(light_orange)
            self.GralEvents[self.current_menu].set_style(STYLE)                  
        # --- Execution on Main Menu
        else:           
            self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(light_orange))                            
            STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(light_orange)
            self.mainmenu_events[self.selected_icon].set_style(STYLE)            
        return
        
    
    #....Method 6: Cue Delivery for the MI Stage......
    def UT_CueMI(self, target):
        'Cue Delivery for the MI part of the User_Tutorial'
    
        # (1) Image Removal        
        self.table.remove(self.CueSignals[0][0])   
        # (2) Selecting the appropriate cue
        if target == 'left':
            self.table.attach(self.CueSignals[0][1],2, 6, 2, 6)            
        elif target == 'right':
            self.table.attach(self.CueSignals[0][2],2, 6, 2, 6)
        elif target == 'idle':
            self.table.attach(self.CueSignals[0][3],2, 6, 2, 6)   
    
    
    #....Method 7: Cue Delivery for the COMMAND Stage......
    def UT_CueCMD(self, submenu, target):
        'Cue Delivery for the COMMAND part of the User_Tutorial'
        
        # (1) Selection of the appropiate Cue
        if target == 'left':
            self.table.attach(self.CueSignals[1][0],0, 2, 0, 2)
        elif target == 'right':
            self.table.attach(self.CueSignals[1][1],0, 2, 0, 2) 
        elif target == 'idle':
            self.table.attach(self.CueSignals[1][2],0, 2, 0, 2) 
        # (2) Event Background Modification        
        # --- Execution on General Menu
        if not(submenu):            
            STYLE = self.GralEvents[self.current_menu].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.GralEvents[self.current_menu].get_colormap().alloc_color(orange)
            self.GralEvents[self.current_menu].set_style(STYLE)                  
        # --- Execution on Main Menu
        else:
            self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))  
            STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(orange)
            self.mainmenu_events[self.selected_icon].set_style(STYLE)         
        return
    

    #...........Method 8: Right MI for COMMAND PART.........
    def UT_NextIcon(self):
        'Navigation through the Gral Menu'
        
        # (1) Previous icon change
        STYLE = self.GralEvents[self.current_menu].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.GralEvents[self.current_menu].get_colormap().alloc_color(ground)
        self.GralEvents[self.current_menu].set_style(STYLE) 
        self.GralEvents[self.current_menu].remove(self.GralIconsON[self.current_menu])
        self.GralEvents[self.current_menu].add(self.MiniIconsON[self.current_menu])
        # (2) Gral menu control update
        self.current_menu = self.gralmenu_indexes.pop(0)
        self.gralmenu_indexes.append(self.current_menu)
        # (3) Previous icon change
        self.GralEvents[self.current_menu].remove(self.MiniIconsON[self.current_menu])
        self.GralEvents[self.current_menu].add(self.GralIconsON[self.current_menu])
        # (4) Title & MainMenu Modifications 
        self.Titles.append(self.Titles.pop(0))
        self.titulo.set_text(self.Titles[0])
        Mnum = self.Titles[0].split(' ')[-1]
        for index in range(len(self.mainmenu_events)):
            label = MainMenu[index]
            if label.lower() != 'exit':
                label = MainMenu[index].split(' ')
                label = [label[0], '\n', Mnum, '.', label[-1]]
                label = ''.join(label)
            self.mainmenu_labels[index].set_text(label)
        
        
        
    #.........Method 9: UT-menu activation - COMMAND........
    def UT_Activation(self):
        '"navigation" and "select" commands switched to UT-menu'

        # =======main menu variables initialization=========      
        self.selected_subutton = 0  
        # (1) GUI~VE control command
        self.GUI_VE = []  
        # ===============UT-menu modifications==============
        # (1) General menu icons modification to indicate INACCESSIBLE navigation    
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))    
        # --- image and background changes        
        self.GralEvents[self.current_menu].remove(self.GralIconsON[self.current_menu])
        self.GralEvents[self.current_menu].add(self.GralIconsOFF[self.current_menu])
        STYLE = self.GralEvents[self.current_menu].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.GralEvents[self.current_menu].get_colormap().alloc_color(ground)
        self.GralEvents[self.current_menu].set_style(STYLE)
        for index in self.gralmenu_indexes[:-1]:           
            children = self.GralEvents[index].get_children()
            self.GralEvents[index].remove(children[0])
            self.GralEvents[index].add(self.MiniIconsOFF[index])        
        # (2) Main Menu Activation        
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        # --- image changes
        for index in range(len(self.mainmenu_events)):
            self.mainmenu_events[index].remove(self.mainmenu_imagesOFF[index])
            self.mainmenu_events[index].add(self.mainmenu_imagesON[index])            
        # (3) Sub-menu buttons Activation
        for item in self.submenu_buttons:
            STYLE = item.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= item.get_colormap().alloc_color(blue)
            item.set_style(STYLE)           
        # (4) Control of Cal menu
        HOME = self.UT_Control()        
        return HOME

    
    #...... Method 10: UT-menu RE-activation - COMMAND......
    def UT_Reactivation(self):
        'Main Menu Reactivation'

        # (1) Resetting the submenu labels
        for item in self.submenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))         
        # (2) Control of N & D menu
        HOME = self.UT_Control()
        return HOME


    #....... Method 11: UT-menu deactivation - COMMAND......
    def UT_Deactivation(self):
        '"navigation" and "select" commands switched to general menu'

        # (1) General menu icons modification to indicate ACCESIBLE navigation   
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))     
        # --- image changes        
        self.GralEvents[self.current_menu].remove(self.GralIconsOFF[self.current_menu])
        self.GralEvents[self.current_menu].add(self.GralIconsON[self.current_menu])        
        for index in self.gralmenu_indexes[:-1]:   
            children = self.GralEvents[index].get_children()
            self.GralEvents[index].remove(children[0])       
            self.GralEvents[index].add(self.MiniIconsON[index])   
        # (2) Main menu Deactivation        
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
        STYLE = self.mainmenu_events[7].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[7].get_colormap().alloc_color(ground)
        self.mainmenu_events[7].set_style(STYLE)            
        # (3) Sub-menu buttons background desactivation
        for item in self.submenu_buttons:
            STYLE = item.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= item.get_colormap().alloc_color(lblue)
            item.set_style(STYLE)
        

    #..........Method 12: UT-menu control - COMMAND.........
    def UT_Control(self):
        'Control of the User_Tutorial menu'
        
        # (1) Updating the current selected button
        self.selected_icon = self.current_icons.pop(0)
        self.current_icons.append(self.selected_icon)   
        # (2) Subutton labels modification
        ## -- current sub-labels
        self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font)) 
        for index in range(8): self.submenu_labels[index].set_label(SubMenu[self.selected_icon][index])      
        ## -- next sublabel pre-deselection
        self.submenu_labels[self.current_subuttons[0]].modify_font(pango.FontDescription(medium_font))         
        # (3) Selection and deselection in main menu   
        ## -- last icon label deselection
        self.mainmenu_labels[self.current_icons[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        self.mainmenu_labels[self.current_icons[6]].modify_font(pango.FontDescription(medium_font))  
        ## -- current icon label selection
        self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))      
        self.mainmenu_labels[self.selected_icon].modify_font(pango.FontDescription(medium_font))     
        ## -- last event_box background deselection
        STYLE = self.mainmenu_events[self.current_icons[6]].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL] = \
        self.mainmenu_events[self.current_icons[6]].get_colormap().alloc_color(ground)
        self.mainmenu_events[self.current_icons[6]].set_style(STYLE)        
        ## -- current event_box background selection
        STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(blue)
        self.mainmenu_events[self.selected_icon].set_style(STYLE) 
        ## -- SubMenu-Text update
        Mnum = self.Titles[0].split(' ')[-1]
        for index in range(len(self.mainmenu_events)):
            if self.mainmenu_labels[self.selected_icon].get_text().lower() == 'exit': break
            label = SubMenu[self.selected_icon][index].split(' ')
            label = [label[0], '\n', Mnum, '.', label[-1]]
            self.submenu_labels[index].set_text(''.join(label))
        ## -- different icons from 'Home'
        if self.selected_icon != 7:
            ## a.- commands belong to main menu
            return False
        else: 
            ## b.- commands could belong to general menu
            return True


    #............ Method 13: UT-menu Blank - MI ............
    def UT_BlankMI(self, target):
        'Rest and Random Intertrial Gap for Tutorial_MI'
               
        # (1) Image Removal
        if target == 'left':
            self.table.remove(self.CueSignals[0][1])
        elif target == 'right':
            self.table.remove(self.CueSignals[0][2]) 
        elif target == 'idle':
            self.table.remove(self.CueSignals[0][3])
        # (2) Return FALSE to avoid calling the idle_function again
        return False


    #............ Method 14: UT-menu Blank - CMD ...........
    def UT_BlankCMD(self, target):
        'Rest and Random Intertrial Gap for Tutorial_CMD'
               
        # (1) Image Removal
        if target == 'left':
            self.table.remove(self.CueSignals[1][0])
        elif target == 'right':
            self.table.remove(self.CueSignals[1][1]) 
        elif target == 'idle':
            self.table.remove(self.CueSignals[1][2])
        # (2) Return FALSE to avoid calling the idle_function again
        return False
    
    
    #.......... Method 15: UT-menu No Control - CMD ........
    def UT_NoControl(self, submenu):
        'No Identified Motor Imaginary Movement'
        
        # (1) Execution on General Menu
        if not(submenu):            
            STYLE = self.GralEvents[self.current_menu].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.GralEvents[self.current_menu].get_colormap().alloc_color(ground)
            self.GralEvents[self.current_menu].set_style(STYLE)              
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
        return 
    
    
    #........... Method 16: UT-Menu writer - CMD ...........
    def UT_Writing(self):
        'GUI~VE control command writer'
        
        self.GUI_VE = []
        # (1) Number of the current tab
        self.GUI_VE.append(0)
        # (2) Number of the current icon
        self.GUI_VE.append(self.selected_icon)
        # (3) Number of the current subutton
        self.GUI_VE.append(self.selected_subutton)
        # (4) Main Menu Update             
        ## -- current label                         
        self.mainmenu_labels[self.selected_icon].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))
        self.mainmenu_labels[self.selected_icon].modify_font(pango.FontDescription(medium_font))   
        STYLE = self.mainmenu_events[self.selected_icon].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_events[self.selected_icon].get_colormap().alloc_color(blue)
        self.mainmenu_events[self.selected_icon].set_style(STYLE)       
        ## -- next label pre-deselection
        self.mainmenu_labels[self.current_icons[0]].modify_font(pango.FontDescription(medium_font))
        # (5) Selecting a task            
        self.submenu_labels[self.selected_subutton].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue)) 
        self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font)) 
        STYLE = self.submenu_buttons[self.selected_subutton].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= \
        self.submenu_buttons[self.selected_subutton].get_colormap().alloc_color('white')
        self.submenu_buttons[self.selected_subutton].set_style(STYLE)                     
        # (6) Updating the History of the selected tasks
        label = self.submenu_labels[self.selected_subutton].get_text()     
        self.History.pop()
        self.History.insert(0, label)   
        for index in range(len(self.History)): self.History_Labels[index].set_text(self.History[index]) 
        return self.GUI_VE
    

    #.......Method 16: Automatic Control of the Submenu.....
    def Auto_Control(self):
        'Auto-Selection of the subuttons menu'

        # (1) Button selection in main~menu
        self.mainmenu_labels[self.current_icons[0]].modify_font(pango.FontDescription(font)) 
        self.mainmenu_labels[self.current_icons[-1]].modify_font(pango.FontDescription(medium_font))   
        if self.mainmenu_labels[self.selected_icon].get_text() != 'EXIT':
            for i in range(8):
                # (2) Updating the current selected subutton
                self.selected_subutton = self.current_subuttons.pop(0)
                self.current_subuttons.append(self.selected_subutton)
                # (3) Button deselection in sub~menu 
                STYLE = self.submenu_buttons[self.current_subuttons[6]].get_style().copy()
                STYLE.bg[gtk.STATE_NORMAL]=self.submenu_buttons[self.current_subuttons[6]].get_colormap().alloc_color(blue)
                self.submenu_buttons[self.current_subuttons[6]].set_style(STYLE)        
                ## -- sublabel deselection
                self.submenu_labels[self.current_subuttons[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))                  
                self.submenu_labels[self.current_subuttons[6]].modify_font(pango.FontDescription(medium_font)) 
                ## -- current subutton font selection                                         
                self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(font))
                if self.submenu_labels[self.selected_subutton].get_text() != '': break                                          

