### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### August 24th, 2010

# ****************************
# * Graphical User Interface:*
# *    'MESSENGER MENU'      *
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
from Constructors import Image,Label,Button_Label,Button_Image,Frame_Image,\
                         Event_Image,Frame_Label,Window_TextView
import WordPrediction

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL CONSTANTS DECLARATION
# (1) Format constants
black = '#213240'
blue = '#466289'
lblue = '#A0AEC1'
orange = '#FA6121'
light_orange = '#FABF8F'
ground = '#DCDCDC'
large_font = "Century Gothic 30"
font = "Century Gothic 25"
medium_font = "Century Gothic 17"
small_font = "Century Gothic 10"

# (2) Main menu dictionary (main buttons labels)
MainMenu = {0: ['a','b','c','d','e','delete','space','send'],
            1: ['f','g','h','i','j','delete','space','send'],
            2: ['k','l','m','n','o','delete','space','send'],
            3: ['p','q','r','s','t','delete','space','send'],
            4: ['u','v','w','x','y','z','delete','space'],
            5: ['','','','','','','',''],                  
            6: ['Images\\Messenger\\joy.png','Images\\Messenger\\sadness.png','Images\\Messenger\\trust.png',
                'Images\\Messenger\\disgust.png','Images\\Messenger\\fear.png','Images\\Messenger\\anger.png',
                'Images\\Messenger\\surprise.png','Images\\Messenger\\anticipation.png'],
            7: 'Exit'}
# (3) List of emotions cartoon
for index in range(8): MainMenu[6][index] = Image(MainMenu[6][index])


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "msg_menu" CLASS DECLARATION

class msg_menu():
    'Class to control the "Messenger" tab'

    #............Method 1: Initialization Process...........
    def __init__(self):        
        'Initial method to generate the "Messenger" menu'

        # =============Messenger tab creation===============        
        # (1) TABLE: Widget container
        ## --9 x 8 table creation
        self.table = gtk.Table(9, 8, True)
        self.table.show()
        
        # (2) LABEL: Window title
        titulo = Label('Messenger', 'Neuropol 31', orange, 0.5, 0.5, gtk.JUSTIFY_CENTER)
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
        url = 'Images\\EnvControl\\SHomeControl_on.png'
        GralIconsON.append(Image(url))
        self.table.attach(GralIconsON[2], 4, 5, 0, 2)
        ## --'Messenger' option
        url = 'Images\\Messenger\\LChat_on.png'
        msg_event, msg_image = Event_Image(url, ground)
        msg_event.set_border_width(10)
        GralIconsON.append(msg_image)
        self.table.attach(msg_event, 5, 6, 0, 2)
        
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

        # (5) TEXT ENTRY
        ## -- text entry
        entry = gtk.Entry(False)
        entry.modify_font(pango.FontDescription(small_font))
        entry.show()
        self.table.attach(entry, 1, 8, 2, 3)
        ## -- text- image
        url = 'Images\\Messenger\\Text_off.png'
        writeOFF = Image(url)
        self.table.attach(writeOFF, 0, 1, 2, 3)

        # (6) BUTTONS: Messenger main menu
        mainmenu_labels, mainmenu_buttons = [], []
        labels = ['a b c d e', 'f g h i j', 'k l m n o',\
                  'p q r s t', 'uv wx yz', 'Options', 'Emotions', 'E X I T']
        for index in range(8):
            button, label = Button_Label(labels[index], lblue, lblue, medium_font)     
            label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)       
            self.table.attach(button, index, index+1, 3, 4)
            mainmenu_labels.append(label)
            mainmenu_buttons.append(button)        

        # (7) BUTTONS: Messenger sub - menu
        submenu_buttons, submenu_labels = [], []
        for x in range(8):
            subutton, sublabel = Button_Label('', lblue, 'white', medium_font)
            sublabel.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
            self.table.attach(subutton, x, x+1, 4, 5)
            submenu_buttons.append(subutton)
            submenu_labels.append(sublabel)        

        # (8) TEXT DISPLAY
        frame_win, textview, textbuffer, tagB, tagG = Window_TextView(medium_font, blue) 
        self.table.attach(frame_win, 0, 8, 5, 8)

        # (9) FRAME & LABEL: Available options
        ## --frame creation        
        frame, label = Frame_Label('AVAILABLE OPTIONS', ground, lblue, small_font, 0, 0.5, gtk.JUSTIFY_CENTER)
        self.table.attach(frame, 0, 8, 8, 9) 
        ## --menu of options
        options_menu = []
        for index in range(8):
            option = Label('', medium_font, 'black', 0.5, 0.5, gtk.JUSTIFY_CENTER)
            self.table.attach(option, index, index+1, 8, 9)
            options_menu.append(option)       
        
        # (10) IMAGES: general menu images 
        GralIconsOFF = []
        GralIconsOFF.append(Image('Images\\Necessity&Desire\\SNecessities_off.png'))
        GralIconsOFF.append(Image('Images\\Mobility\\SMobility_off.png'))
        GralIconsOFF.append(Image('Images\\EnvControl\\SHomeControl_off.png'))        
        GralIconsOFF.append(Image('Images\\Messenger\\LChat_off.png'))
        writeON = Image('Images\\Messenger\\Text_on.png')
        self.msg_MI = Image('Images\\Messenger\\LChat_MI.png') 
        
        #(11) IMAGES: emotion submenu 
        SelectedEmotion = []
        SelectedEmotion.append(Image('Images\\Messenger\\joy_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\sadness_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\trust_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\disgust_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\fear_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\anger_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\surprise_selection.png'))
        SelectedEmotion.append(Image('Images\\Messenger\\anticipation_selection.png'))     
        
        #(12) Widgets assignation to enable them in the following
        #     methods
        ## -- ButtonS
        self.mainmenu_buttons = mainmenu_buttons
        self.submenu_buttons = submenu_buttons
        ## -- ImageS
        self.msg_image = msg_image
        self.writeOFF = writeOFF
        self.writeON  = writeON
        self.GralIconsOFF = GralIconsOFF
        self.GralIconsON  = GralIconsON
        self.SelectedEmotion = SelectedEmotion
        ## -- FrameS
        self.msg_event = msg_event
        self.frame_win = frame_win
        ## -- LabelS
        self.CueSignals = CueSignals
        self.titulo = titulo
        self.mainmenu_labels = mainmenu_labels
        self.submenu_labels = submenu_labels
        self.options_menu = options_menu
        ## -- TextEntrY
        self.entry = entry
        ## -- TextDiplaY
        self.textview = textview
        self.textbuffer = textbuffer
        self.tagB, self.tagG = tagB, tagG
        ## -- Variable Declaration
        self.CUE = None
        #     Messages variables
        self.text, self.OPTIONS, self.num_space = '', ['','','','','','','',''], 0
    

    #..........Method 2: Returning widgets container........
    def msg_container(self):
        'Messenger table for being appended to the notebook'
        return self.table

    
    #..........Method 3: Messenger menu activation..........
    def msg_Activation(self):
        '"navigation" and "select" commands switched to Messenger menu'

        # =======main menu variables initialization=========
        # (1) Current selected button and available message
        self.current_buttons = range(8)
        self.current_subuttons = range(8)
        # (2) Submenu default value
        self.selected_subutton = 0
        
        # ============Messenger menu modifications==========
        # (1) General menu icons modification to indicate INACCESIBLE navigation 
        # --- title colour deselection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
        # --- image changes
        self.table.remove(self.GralIconsON[0])
        self.table.attach(self.GralIconsOFF[0], 2, 3, 0, 2)
        self.table.remove(self.GralIconsON[1])
        self.table.attach(self.GralIconsOFF[1], 3, 4, 0, 2)
        self.table.remove(self.GralIconsON[2])
        self.table.attach(self.GralIconsOFF[2], 4, 5, 0, 2) 
        children = self.msg_event.get_children()
        self.msg_event.remove(children[0])        
        self.msg_event.add(self.GralIconsOFF[3])      
        STYLE = self.msg_event.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.msg_event.get_colormap().alloc_color(ground)
        self.msg_event.set_style(STYLE)     
        # (2) Main Menu Activation
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        # --- image changes
        self.table.remove(self.writeOFF)
        self.table.attach(self.writeON, 0, 1, 2, 3)        
        # (3) Sub-menu buttons activation
        for item in self.submenu_buttons:
            STYLE = item.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= item.get_colormap().alloc_color(blue)
            item.set_style(STYLE)
        # (4) Control of messenger menu
        HOME = self.msg_Control()     
        return HOME
    

    #.........Method 4: Messenger menu RE-activation........
    def msg_Reactivation(self):
        'Main Menu Reactivation'
        
        # (1) Resetting the submenu labels
        for item in self.submenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
        # (2) Control of messenger menu
        HOME = self.msg_Control()
        return HOME


    #..........Method 5: Messenger menu deactivation........
    def msg_Deactivation(self):
        '"navigation" and "select" commands switched to general menu'

        # (1) General menu icons modification to indicate ACCESIBLE navigation 
        # --- title colour selection
        self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))
        # --- image changes
        self.table.remove(self.GralIconsOFF[0])
        self.table.attach(self.GralIconsON[0], 2, 3, 0, 2)
        self.table.remove(self.GralIconsOFF[1])
        self.table.attach(self.GralIconsON[1], 3, 4, 0, 2)
        self.table.remove(self.GralIconsOFF[2])
        self.table.attach(self.GralIconsON[2], 4, 5, 0, 2) 
        self.msg_event.remove(self.GralIconsOFF[3])
        self.msg_event.add(self.GralIconsON[3])           
        # (2) Main menu labels Deactivation
        # --- label modifications
        for item in self.mainmenu_labels: item.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
        self.mainmenu_labels[self.current_buttons[0]].modify_font(pango.FontDescription(medium_font))
        # --- button\label modifications
        STYLE = self.mainmenu_buttons[7].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[7].get_colormap().alloc_color(lblue)
        self.mainmenu_buttons[7].set_style(STYLE)
        self.mainmenu_labels[7].modify_font(pango.FontDescription(medium_font))
        # --- image changes
        self.table.remove(self.writeON)
        self.table.attach(self.writeOFF, 0, 1, 2, 3)          
        # (3) Sub-menu buttons background desactivation
        for item in self.submenu_buttons:
            STYLE = item.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= item.get_colormap().alloc_color(lblue)
            item.set_style(STYLE)  


    #............Method 6: Messenger menu control...........
    def msg_Control(self):
        'Control of the Messenger menu'

        # (1) Updating the current selected button
        self.selected_button = self.current_buttons.pop(0)
        self.current_buttons.append(self.selected_button)
        # (2) Subutton labels modification
        ## -- current sublabel
        self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font))
        ## -- next sublabel pre-deselection
        self.submenu_labels[self.current_subuttons[0]].modify_font(pango.FontDescription(medium_font))  
        # (3) Button selection and deselection in main menu
        ## -- current button background and label selection
        STYLE = self.mainmenu_buttons[self.selected_button].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[self.selected_button].get_colormap().alloc_color(blue)
        self.mainmenu_buttons[self.selected_button].set_style(STYLE)
        self.mainmenu_labels[self.selected_button].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
        self.mainmenu_labels[self.selected_button].modify_font(pango.FontDescription(medium_font))
        ## -- last button background and label deselection
        STYLE = self.mainmenu_buttons[self.current_buttons[6]].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[self.current_buttons[6]].get_colormap().alloc_color(lblue)
        self.mainmenu_buttons[self.current_buttons[6]].set_style(STYLE)
        self.mainmenu_labels[self.current_buttons[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('black'))
        self.mainmenu_labels[self.current_buttons[6]].modify_font(pango.FontDescription(medium_font))
        # (4) Main buttons control
        # a.- 'HOME' button
        if self.selected_button == 7:
            # -- unselecting all subuttons, removing images and labels
            for index in range(8):
                children = self.submenu_buttons[index].get_children()
                self.submenu_buttons[index].remove(children[0])
                self.submenu_buttons[index].add(self.submenu_labels[index])
                self.submenu_labels[index].set_label(MainMenu[5][index])
                STYLE = self.submenu_buttons[index].get_style().copy()
                STYLE.bg[gtk.STATE_NORMAL]= self.submenu_buttons[index].get_colormap().alloc_color(blue)
                self.submenu_buttons[index].set_style(STYLE)
                self.submenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
                self.submenu_labels[index].modify_font(pango.FontDescription(medium_font))   
            # -- commands could belong to general menu
            return True
        # b.- 'EMOTIONS' button
        elif self.selected_button == 6:
            for index in range(8):
                self.submenu_buttons[index].remove(self.submenu_labels[index])
                self.submenu_buttons[index].add(MainMenu[self.selected_button][index])
            return False
        # c.- Letters and 'OPTIONS' buttons
        else:
            if self.selected_button != 5:
            ## -- row subutton labels modification
                for index in range(8):
                    self.submenu_labels[index].set_label(MainMenu[self.selected_button][index])
            else:
                for index in range(8):
                    self.submenu_labels[index].set_text(self.options_menu[index].get_text())                    
            ## -- commands belong to main menu
            return False


    #.........Method 7: Messenger menu Warning Sign.......
    def msg_WarningSign(self, submenu):
        'Motor Imaginary Movement Preparation'
        
        if submenu: self.Auto_Control()
        # (1) Execution on General Menu
        if not(submenu):            
            # --- event modification        
            STYLE = self.msg_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.msg_event.get_colormap().alloc_color(light_orange)
            self.msg_event.set_style(STYLE)   
            return 'unknown_task', 'unknown_len'
        # (2) Execution on Main Menu
        else:
            self.mainmenu_buttons[self.selected_button].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))                          
            STYLE = self.mainmenu_buttons[self.selected_button].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[self.selected_button].get_colormap().alloc_color(light_orange)
            self.mainmenu_buttons[self.selected_button].set_style(STYLE)
            ## -- length of the current selected submenu
            current_len = len([item for item in MainMenu[self.selected_button] if item != '']) 
            return self.selected_subutton, current_len


    #.........Method 8: Messenger menu MI Performance.......
    def msg_MIPerformance(self, submenu, target):
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
            STYLE = self.msg_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.msg_event.get_colormap().alloc_color(orange)
            self.msg_event.set_style(STYLE)                  
        # (3) Execution on Main Menu
        else:
            self.mainmenu_buttons[self.selected_button].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))                          
            STYLE = self.mainmenu_buttons[self.selected_button].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[self.selected_button].get_colormap().alloc_color(orange)
            self.mainmenu_buttons[self.selected_button].set_style(STYLE) 
        return


    #......... Method 9: Messenger menu No Control .........
    def msg_NoControl(self, submenu, reset):
        'Weak or None Motor Imaginary Movement Performance'
        
        # (1) Execution on General Menu
        if not(submenu):            
            # --- event modification        
            STYLE = self.msg_event.get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.msg_event.get_colormap().alloc_color(ground)
            self.msg_event.set_style(STYLE)                 
        # (2) Execution on Main Menu
        else:                              
            ## -- mainmenu labels
            self.mainmenu_labels[self.current_buttons[0]].modify_font(pango.FontDescription(medium_font))
            STYLE = self.mainmenu_buttons[self.selected_button].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[self.selected_button].get_colormap().alloc_color(blue)
            self.mainmenu_buttons[self.selected_button].set_style(STYLE) 
            ## -- submenu label
            if self.selected_button != 6:
                self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font))  
            ## -- emotion button
            else: 
                children = self.submenu_buttons[self.current_subuttons[-1]].get_children()
                self.submenu_buttons[self.current_subuttons[-1]].remove(children[0])
                self.submenu_buttons[self.current_subuttons[-1]].add(MainMenu[6][self.current_subuttons[-1]]) 
            ## -- reset AutoControl if command != cue
            if reset:
                self.selected_subutton == self.current_subuttons.pop()
                self.current_subuttons.insert(0, self.selected_subutton)                   
    
    
    #........ Method 10: Messenger menu - Blank  .......
    def msg_Blank(self, target):
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
    
    
    #..........Method 11: Messenger Gral Icon Reset..........
    def msg_Reset(self):
        'Resetting before leaving the Current Tab'
        
        # --- event modification        
        STYLE = self.msg_event.get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.msg_event.get_colormap().alloc_color(ground)
        self.msg_event.set_style(STYLE)  
    
    
    #............Method 12: Messenger Tab Reset.............
    def msg_ResetALL(self, submenu, tab):
        'Reset of the Whole Tab'

        # (1) Reset of Variables
        self.current_buttons = range(8)
        self.current_subuttons = range(8)
        self.text, self.OPTIONS, self.num_space, self.selected_subutton = '', ['','','','','','','',''], 0, -1
        # (2) Cue-Removal if any
        if self.CUE != None: self.table.remove(self.CUE)
        # (3) General menu icons modification to indicate ACCESIBLE navigation
        if all([submenu, tab==3]):
            # --- title colour selection
            self.titulo.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(orange))
            # --- image changes
            self.table.remove(self.GralIconsOFF[0])
            self.table.attach(self.GralIconsON[0], 2, 3, 0, 2)
            self.table.remove(self.GralIconsOFF[1])
            self.table.attach(self.GralIconsON[1], 3, 4, 0, 2)
            self.table.remove(self.GralIconsOFF[2])
            self.table.attach(self.GralIconsON[2], 4, 5, 0, 2) 
            self.msg_event.remove(self.GralIconsOFF[3])
            self.msg_event.add(self.GralIconsON[3])   
            # --- image changes
            self.table.remove(self.writeON)
            self.table.attach(self.writeOFF, 0, 1, 2, 3)    
        # (4) MainMenu Deactivation  
        for index in range(len(self.mainmenu_buttons)):
        ## -- label modifications
            self.mainmenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(lblue))
            self.mainmenu_labels[index].modify_font(pango.FontDescription(medium_font))
        ## -- event background deselection
            STYLE = self.mainmenu_buttons[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[index].get_colormap().alloc_color(lblue)
            self.mainmenu_buttons[index].set_style(STYLE)  
        ## -- Sub-menu buttons background desactivation
            STYLE = self.submenu_buttons[index].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= self.submenu_buttons[index].get_colormap().alloc_color(lblue)
            self.submenu_buttons[index].set_style(STYLE)            
        ## -- sublabel modifications
            self.submenu_labels[index].set_text('')
            self.submenu_labels[index].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))
            self.submenu_labels[index].modify_font(pango.FontDescription(medium_font))     
        # (5) Available Options Reset
        for widget in self.options_menu: widget.set_text('')
        # (6) TextView Widgets (labels and/or cartoons) Removal
        self.table.remove(self.frame_win)
        self.frame_win, self.textview, self.textbuffer, self.tagB, self.tagG = Window_TextView(medium_font, blue) 
        self.table.attach(self.frame_win, 0, 8, 5, 8)
        # (7) TextEntry clearance
        self.entry.set_text('')
            

    #............Method 13: Messenger menu writer...........
    def msg_Writing(self):
        'Desired letter catcher and writer'
        
        # (1) No available submenu~labels (just return the original format to mainlabels and sublabels)
        conditions = [widget.get_text() == '' for widget in self.submenu_labels]
        conditions.append(self.selected_button == 5)
        # (2) Main Menu Update
        ## -- current label
        self.mainmenu_labels[self.selected_button].modify_font(pango.FontDescription(medium_font))
        self.mainmenu_labels[self.selected_button].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))                          
        STYLE = self.mainmenu_buttons[self.selected_button].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]= self.mainmenu_buttons[self.selected_button].get_colormap().alloc_color(blue)
        self.mainmenu_buttons[self.selected_button].set_style(STYLE) 
        ## -- next label pre-deselection
        self.mainmenu_labels[self.current_buttons[0]].modify_font(pango.FontDescription(medium_font))
        # (3) Selecting a task         
        ## -- sublabel update to medium_font
        self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(medium_font)) 
        ## ===== return =====
        if all(conditions): return '_'.join(['3',str(self.selected_button),'none'])
        ## -- selection of a task
        self.submenu_labels[self.selected_subutton].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(blue))  
        STYLE = self.submenu_buttons[self.selected_subutton].get_style().copy()
        STYLE.bg[gtk.STATE_NORMAL]=self.submenu_buttons[self.selected_subutton].get_colormap().alloc_color('white')
        self.submenu_buttons[self.selected_subutton].set_style(STYLE) 
        # (4) 'EMOTIONS' selection
        if self.selected_button == 6:
            PIXBUF = self.SelectedEmotion[self.selected_subutton].get_pixbuf()
            location = self.textbuffer.get_end_iter()
            self.textbuffer.insert_pixbuf(location, PIXBUF)
            self.textbuffer.insert_at_cursor('\n')
            # -- updating the vertical window scroll automatically
            mark = self.textbuffer.create_mark("end", self.textbuffer.get_end_iter(), False)
            self.textview.scroll_to_mark(mark, 0.05, True, 0.0, 0.0)
            # -- variable to stop BCI-protocol in Exp2 (option 2: sent message)   
            #    (force the system to sent always the first SEND to avoid unnecessary future comparison             
            return '307'
        # (5) Writing on the TextVIEW and TextEntry
        else:
            ## -- 'space' command
            if self.submenu_labels[self.selected_subutton].get_text() == 'space':
                if self.text != '':
                    # a.- writing one gap
                    if self.text[-1] != '_': self.text += '_'
                    # b.- resetting optional words
                    for item in self.options_menu: item.set_text('')
            ## -- 'send' command
            elif self.submenu_labels[self.selected_subutton].get_text() == 'send':
                if self.text != '':
                    # a.- writing on TextView only if there is data
                    self.text = self.text.replace('_', ' ')
                    self.textbuffer.insert_at_cursor(self.text)
                    iterG1, iterB2 = self.textbuffer.get_bounds()
                    line_number = self.textbuffer.get_line_count()
                    iterB1 = self.textbuffer.get_iter_at_line(line_number)
                    self.textbuffer.apply_tag(self.tagG, iterG1, iterB2)
                    self.textbuffer.remove_tag(self.tagG, iterB1, iterB2)
                    self.textbuffer.apply_tag(self.tagB, iterB1, iterB2)
                    self.textbuffer.insert_at_cursor('\n')
                    # b.- updating the vertical window scroll automatically
                    mark = self.textbuffer.create_mark("end", self.textbuffer.get_end_iter(), False)
                    self.textview.scroll_to_mark(mark, 0.05, True, 0.0, 0.0)
                    # c.- resetting used variables
                    self.text, self.OPTIONS, self.num_space = '', ['','','','','','','',''], 0
                    for item in self.options_menu: item.set_text('')
                    # -- variable to stop BCI-protocol in Exp2 (option 2: sent message)   
                    #    (force the system to sent always the first SEND to avoid unnecessary future comparison             
                    return '307'
            ## -- letters and available options
            else:
                # a.- no 'OPTIONS' button
                if self.selected_button != 5:
                    # deleting process
                    if self.submenu_labels[self.selected_subutton].get_text() == 'delete':
                        if self.text != '':
                            if self.text[-1] == '_':
                                self.text = self.text[:-1]
                                space = self.text.find('_')
                                if space == -1:
                                    self.num_space = 0
                                else:
                                    while space != -1:
                                        self.num_space = space + 1
                                        space = self.text.find('_', self.num_space, len(self.text))                        
                            else:
                                self.text = self.text[:-1]
                    # writing process
                    else:                   
                        self.text += MainMenu[self.selected_button][self.selected_subutton]
                # b.- 'OPTIONS' button
                else:
                    if self.OPTIONS[self.selected_subutton] != '':                
                        self.text = self.text[:self.num_space] + self.OPTIONS[self.selected_subutton] + '_'
                # c.- updating the self.text according to the available options and number of written spaces
                space = self.text.find('_', self.num_space, len(self.text))
                if space == -1:
                    if len(self.text) == 1: self.OPTIONS = ['','','','','','','','']
                else:
                    self.num_space = space + 1
                word = self.text[self.num_space:]
                self.OPTIONS = WordPrediction.Options(word, self.OPTIONS)
                while len(self.OPTIONS) < 8:
                    self.OPTIONS.append('')
                for index in range(8):
                    self.options_menu[index].set_text(self.OPTIONS[index])                
            ## -- 'write' on the entry line
            self.entry.set_text(self.text)
            if self.entry.get_text() == '':
                for index in range(8):
                    self.options_menu[index].set_text('')
            ## -- return empty string till the SEND button is pushed
            ##    (variable to stop BCI-protocol in Exp2)
            return '_'.join(['3',str(self.selected_button),'writing'])

      
    #.......Method 14: Automatic Control of the Submenu.....
    def Auto_Control(self):
        'Auto-Selection of the subuttons menu'

        # (1) Button selection in main~menu
        self.mainmenu_labels[self.current_buttons[0]].modify_font(pango.FontDescription(font)) 
        self.mainmenu_labels[self.selected_button].modify_font(pango.FontDescription(medium_font))   
        ## -- No available submenu~labels
        conditions = [widget.get_text() == '' for widget in self.submenu_labels]
        conditions.append(self.selected_button == 5) 
        if all(conditions): return
        # (2) Emotions
        if self.mainmenu_labels[self.selected_button].get_text().lower() == 'emotions':
            # (2.1) Updating the current selected subutton
            self.selected_subutton = self.current_subuttons.pop(0)
            self.current_subuttons.append(self.selected_subutton)     
            # (2.2) Button selection in menu/submenu
            self.mainmenu_labels[self.current_buttons[0]].modify_font(pango.FontDescription(font))
            ## -- current subutton background selection
            children = self.submenu_buttons[self.selected_subutton].get_children()
            self.submenu_buttons[self.selected_subutton].remove(children[0])
            self.submenu_buttons[self.selected_subutton].add(self.SelectedEmotion[self.selected_subutton])                                      
            ## -- previous subutton background deselection
            STYLE = self.submenu_buttons[self.current_subuttons[6]].get_style().copy()
            STYLE.bg[gtk.STATE_NORMAL]= \
            self.submenu_buttons[self.current_subuttons[6]].get_colormap().alloc_color(blue)
            self.submenu_buttons[self.current_subuttons[6]].set_style(STYLE) 
            children = self.submenu_buttons[self.current_subuttons[6]].get_children()
            self.submenu_buttons[self.current_subuttons[6]].remove(children[0])
            self.submenu_buttons[self.current_subuttons[6]].add(MainMenu[6][self.current_subuttons[6]])                                  
        # (3) Text-Entry
        elif self.mainmenu_labels[self.selected_button].get_text().lower().strip() != 'exit':
            for i in range(8):
                # (3.1) Updating the current selected subutton
                self.selected_subutton = self.current_subuttons.pop(0)
                self.current_subuttons.append(self.selected_subutton)
                # (3.2) Button deselection in sub~menu 
                STYLE = self.submenu_buttons[self.current_subuttons[6]].get_style().copy()
                STYLE.bg[gtk.STATE_NORMAL]=self.submenu_buttons[self.current_subuttons[6]].get_colormap().alloc_color(blue)
                self.submenu_buttons[self.current_subuttons[6]].set_style(STYLE)        
                ## -- sublabel deselection
                self.submenu_labels[self.current_subuttons[6]].modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse('white'))                  
                self.submenu_labels[self.current_subuttons[6]].modify_font(pango.FontDescription(medium_font)) 
                ## -- current subutton font selection         
                text = self.submenu_labels[self.selected_subutton].get_text()
                if len(text) == 1:
                    self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(large_font))
                else:
                    self.submenu_labels[self.selected_subutton].modify_font(pango.FontDescription(font))
                if text != '': break