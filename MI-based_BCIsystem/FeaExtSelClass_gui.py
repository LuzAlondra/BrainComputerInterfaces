# -*- coding: cp1252 -*-
### VE PROJECT: Brain-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### June 27th, 2011

# ************************************
# * BCI Design - Graphical Interface *
# *  FEATURE EXT + SEL, CLASSIFIER   *
# ************************************

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject
import scipy as sp
from scipy import io
import numpy as np

# ...................GUI Design Libraries...................
from Constructors_gui import Image,Label,Frame,Button_Label,\
     Radio_Button,TextEntry, Check_Button, Event_Label


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL VARIABLES DECLARATION
window = ['Bartlett','Blackman','Boxcar','Flat Top','Gaussian','Hamming','Hanning','Triangular']
lblue = '#A0AEC1'

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION
# F1. Dialog Box design to send a warning
def DialogBox(MESSAGE):
    'Warning Information Delivery'

    message = Label(MESSAGE,'Trebuchet 14', 'black', 0, 0)
    dialog = gtk.Dialog('Typing Error!',None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,("OK", True))
    STYLE = dialog.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = dialog.get_colormap().alloc_color('#DCDCDC')
    dialog.set_style(STYLE)
    dialog.vbox.pack_start(message)
    dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    dialog.show_all()
    result = dialog.run()
    if result: dialog.destroy()
    dialog.destroy()  

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "FeaExtSelClass_menu" CLASS DECLARATION

class FeaExtSelClass_menu():
    'Class to control the "FeaExtClass_interface" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "FeaExt_interface" menu'

        # ============== Variable Declaration ==============
        blue = '#466289'
        lblue = '#A0AEC1'
        tab_bg = '#DCDCDC'
        orange = '#FA6121'
        large_font = 'Trebuchet 16'
        font = "Trebuchet 14"
        small_font = "Trebuchet 12"
        BP_menu, FeaSel_menu, CheckBoxLabel, RadioLabel = [], [], [], []
        ##-- Out data from FeaExt_menu class
        self.feaext_output = ['absolute_bb', 'off', ['off', 'off'], ['off', 'off'], ['off', 'off'], ['off', 'off'], \
                             ['off', 'off'], ['off', 'off'], ['off', 'off'], ['off', 'off'], ['off', 'off'], ['off', 'off']]
        self.location = [0, 0, 0, 0, 0]
        ##-- Out data from FeaSel_menu class
        self.feasel_output = ['off', ['off', 'FDA'], ['off', 'off'], ['off', 'off']]
        ##-- Out data from Class_menu class
        self.class_output = ['FDA', '', 'off','off']
        
        # ========== Feature Extractor Interface ===========        
        # (1) TABLE: Widget container
        ## --14 x 6 table creation
        self.table = gtk.Table(14, 6, True)
        self.table.show()

        # (2) LABEL: Window title
        titulo = Label(' BCI System - Feature Extractor, Selector & Classifier', 'Neuropol 20', blue, 0, 0.5)
        self.table.attach(titulo, 0, 5, 0, 1)
        subtitulo = Label(' A VE Plataform for Simulated BCI-Enabled Independent Living', \
                          'Neuropol 18', orange, 0, 0.5)
        self.table.attach(subtitulo, 0, 5, 1, 2)

        # (3) IMAGES: General menu images
        url = 'Images\\minilogo.jpg'
        logo = Image(url)
        logo.set_alignment(xalign=0.5, yalign=0.5)
        self.table.attach(logo, 5, 6, 0, 2)
 
        # (4) LABEL & RADIO BUTTONS: Type of BP Selection
        ## -- Title
        tempo = Label('FEATURE\nEXTRACTOR ', large_font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 1, 2, 4)
        icon = Image('Images\\features.png') 
        icon.set_alignment(xalign=0.2, yalign=0.5)
        self.table.attach(icon, 1, 2, 2, 4)      
        ## -- label
        tempo = Label('1|  Power measurement', font, 'black', 0.1, 0.5)
        self.table.attach(tempo, 0, 2, 4, 5) 
        ## -- BP selection
        option1, label = Radio_Button(None, ' Band power including broadband', font, 'black')
        RadioLabel.append(label)
        option1.connect("toggled", self.BP_opt1, BP_menu, RadioLabel, 1)
        self.table.attach(option1, 0, 2, 5, 6)        
        option2, label = Radio_Button(option1, ' Band power', font, lblue)
        RadioLabel.append(label)
        option2.connect("toggled", self.BP_opt1, BP_menu, RadioLabel, 2)
        self.table.attach(option2, 0, 2, 6, 7)       
        option3, label = Radio_Button(option1, ' Relative power', font, lblue)
        RadioLabel.append(label)
        option3.connect("toggled", self.BP_opt2, BP_menu, RadioLabel)
        self.table.attach(option3, 0, 2, 7, 8)
        option4, label = Radio_Button(option1, ' ERD-ERS values:', font, lblue)
        RadioLabel.append(label)
        option4.connect("toggled", self.BP_opt3, BP_menu, RadioLabel)
        self.table.attach(option4, 0, 1, 8, 9)

        # (5) EventBoxes & LABEL: bandwidth submenu selection
        ## -- label
        tempo = Label('2|  Frequency band selection', font, 'black', 0.1, 0.5)
        self.table.attach(tempo, 0, 2, 9, 10)
        ##-- theta band
        event, label = Event_Label('theta: ', font, lblue, 1, 0.5, tab_bg)
        event.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        event.connect("button_press_event", self.BP_Theta, BP_menu)
        self.table.attach(event, 0, 1, 10, 11)
        BP_menu.append(label)
        ##-- alpha band
        event, label = Event_Label('alpha: ', font, lblue, 1, 0.5, tab_bg)
        event.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        event.connect("button_press_event", self.BP_Alpha, BP_menu)
        self.table.attach(event, 0, 1, 11, 12)
        BP_menu.append(label)        
        ##-- beta band
        event, label = Event_Label('beta: ', font, lblue, 1, 0.5, tab_bg)
        event.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        event.connect("button_press_event", self.BP_Beta, BP_menu)
        self.table.attach(event, 0, 1, 12, 13)
        BP_menu.append(label)        
        ##-- gamma band
        event, label = Event_Label('gamma: ', font, lblue, 1, 0.5, tab_bg)
        event.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        event.connect("button_press_event", self.BP_Gamma, BP_menu)
        self.table.attach(event, 0, 1, 13, 14)
        BP_menu.append(label)
        
        # (6) TEXT-ENTRIES: BP submenu selection 
        ## -- ERD/ERS power       
        tempo = TextEntry(self.read_BP, 0)
        tempo.set_editable(False)
        self.table.attach(tempo, 1, 2, 8, 9)
        BP_menu.append(tempo)
        ## -- theta band
        tempo = TextEntry(self.read_BP, 1)
        tempo.set_editable(False)
        self.table.attach(tempo, 1, 2, 10, 11)
        BP_menu.append(tempo)
        ##-- alpha band
        tempo = TextEntry(self.read_BP, 2)
        tempo.set_editable(False)
        self.table.attach(tempo, 1, 2, 11, 12)
        BP_menu.append(tempo)        
        ## -- beta band
        tempo = TextEntry(self.read_BP, 3)
        tempo.set_editable(False)
        self.table.attach(tempo, 1, 2, 12, 13)
        BP_menu.append(tempo)        
        ## -- gamma band
        tempo = TextEntry(self.read_BP, 4)
        tempo.set_editable(False)
        self.table.attach(tempo, 1, 2, 13, 14)
        BP_menu.append(tempo)       
        
        
        # =========== Feature Selector Interface ===========
        # (1) LABELS: classifier menu selection
        ## -- Title 
        tempo = Label('FEATURE\nSELECTOR', large_font, 'black', 1, 0.5)
        self.table.attach(tempo, 2, 3, 2, 4)
        icon = Image('Images\\selection.png') 
        icon.set_alignment(xalign=0.2, yalign=0.5)
        self.table.attach(icon, 3, 4, 2, 4)
        
        # (2) CHECK BUTTON & LABEL: DBI menu
        ## -- label
        tempo = Label('1|  Cluster validity techniques', font, 'black', 0.1, 0.5)
        self.table.attach(tempo, 2, 4, 4, 5)
        ## -- check button
        button, label = Check_Button(' DBI', font, lblue)
        button.connect("toggled", self.DBI, CheckBoxLabel)
        self.table.attach(button, 2, 4, 5, 6)
        CheckBoxLabel.append(label)
                
        # (3) CHECK BUTTON & RADIO BUTTONS: RFE menu
        ## -- label
        tempo = Label('2|  Feature ranking (offline system)', font, 'black', 0.1, 0.5)
        self.table.attach(tempo, 2, 4, 6, 7)
        ## -- check button
        button, label = Check_Button(' RFE', font, lblue)
        button.connect("toggled", self.RFE, FeaSel_menu, CheckBoxLabel)
        self.table.attach(button, 2, 4, 7, 8)
        CheckBoxLabel.append(label)
        ## -- radio buttons
        option1, label = Radio_Button(None, ' FDA', font, 'black')
        RadioLabel.append(label)
        option1.connect('toggled', self.Classifier, 'FDA', 'selection', RadioLabel, 2)
        self.table.attach(option1, 2, 4, 8, 9)
        FeaSel_menu.append(option1)
        option2, label = Radio_Button(option1, ' Linear SVM', font, lblue)
        RadioLabel.append(label)
        option2.connect('toggled', self.Classifier, 'Linear_SVM', 'selection', RadioLabel, 3)
        self.table.attach(option2, 2, 3, 9, 10)    
        FeaSel_menu.append(option2)    
        option3, label = Radio_Button(option2, ' Gaussian SVM', font, lblue)
        RadioLabel.append(label)
        option3.connect('toggled', self.Classifier, 'RBF_SVM', 'selection', RadioLabel, 4)
        self.table.attach(option3, 3, 4, 9, 10)
        FeaSel_menu.append(option3)
        for item in FeaSel_menu[:3]: item.hide()
        
        # (4) CHECK BUTTON, LABEL & TEXT-ENTRY: Feature Selection
        ## -- label
        tempo = Label('3|  Feature selection', font, 'black', 0.1, 0.5)
        self.table.attach(tempo, 2, 4, 10, 11)
        ## -- check button
        button, label = Check_Button(' Feature indexes', font, lblue)
        button.connect("toggled", self.IndexRange, FeaSel_menu, CheckBoxLabel)
        self.table.attach(button, 2, 4, 11, 12)
        CheckBoxLabel.append(label)        
        ##-- radio button 1
        option4, label = Radio_Button(None, ' DBI features: ', font, 'black')
        RadioLabel.append(label)
        option4.connect("toggled", self.DBIFeatures, FeaSel_menu, RadioLabel)
        self.table.attach(option4, 2, 3, 12, 13)
        FeaSel_menu.append(option4)           
        ##-- radio button 2
        option5, label = Radio_Button(option4, ' RFE features: ', font, lblue)
        RadioLabel.append(label)
        option5.connect("toggled", self.RFEFeatures, FeaSel_menu, RadioLabel)
        self.table.attach(option5, 2, 3, 13, 14)
        FeaSel_menu.append(option5)     
        ## -- text-entry 1
        tempo = TextEntry(self.read_FeaSel, [2, 1])
        tempo.set_editable(False)
        self.table.attach(tempo, 3, 4, 12, 13)
        FeaSel_menu.append(tempo)  
        ## -- text-entry 2
        tempo = TextEntry(self.read_FeaSel, [3, 1])
        tempo.set_editable(False)
        self.table.attach(tempo, 3, 4, 13, 14)
        FeaSel_menu.append(tempo)
        for item in FeaSel_menu[3:]: item.hide()
        
               
        # ========== Feature Classifier Interface ==========
        # (1) LABELS: classifier menu selection
        ## -- Title 
        tempo = Label('CLASSIFIER', large_font, 'black', 1, 0.5)
        self.table.attach(tempo, 4, 5, 2, 4)
        icon = Image('Images\\classifier.png') 
        icon.set_alignment(xalign=0.2, yalign=0.5)
        self.table.attach(icon, 5, 6, 2, 4)
        ## -- SubTitle 1
        tempo = Label('1|  Class labels ', font, 'black', 0, 0.5)
        self.table.attach(tempo, 4, 6, 4, 5) 
        ## -- Left/Right/NonControl commands
        tempo = Label('Left / right / idle: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 4, 5, 5, 6) 
        ## -- SubTitle 2
        tempo = Label('2|  Feature vector scaling', font, 'black', 0, 0.5)
        self.table.attach(tempo, 4, 6, 6, 7)
        ## -- SubTitle 3
        tempo = Label('3|  Classifier type', font, 'black', 0, 0.5)
        self.table.attach(tempo, 4, 6, 8, 9)        
        ## -- SubTitle 4
        tempo = Label('4|  Classifier calibration (online system)', font, 'black', 0, 0.5)
        self.table.attach(tempo, 4, 6, 12, 13)        
        
         # (2) RADIO BUTTONS: classifier selection
        option1, label = Radio_Button(None, ' FDA', font, 'black')
        RadioLabel.append(label)
        option1.connect('toggled', self.Classifier, 'FDA', 'classification', RadioLabel, 7)
        self.table.attach(option1, 4, 6, 9, 10)
        option2, label = Radio_Button(option1, ' Linear SVM', font, lblue)
        RadioLabel.append(label)
        option2.connect('toggled', self.Classifier, 'Linear_SVM', 'classification', RadioLabel, 8)
        self.table.attach(option2, 4, 6, 10, 11)        
        option3, label = Radio_Button(option2, ' Radial basis function SVM', font, lblue)
        RadioLabel.append(label)
        option3.connect('toggled', self.Classifier, 'RBF_SVM', 'classification', RadioLabel, 9)
        self.table.attach(option3, 4, 6, 11, 12)         
        
        # (3) LABEL: Classifier Calibration
        class_label = Label('Trials per class: ', font, 'black', 1, 0.5)
        self.table.attach(class_label, 4, 5, 13, 14)        
        
        # (4) TEXT-ENTRY:  Class labels and calibration
        ## -- Class Labels
        tempo = TextEntry(self.read_Class, [1])
        tempo.set_editable(True)
        self.table.attach(tempo, 5, 6, 5, 6)
        ## -- Classifier Calibration
        tempo = TextEntry(self.read_Class, [2])
        tempo.set_editable(True)
        self.table.attach(tempo, 5, 6, 13, 14)
        
        ## (5) CHECKBOX: Feature Vector Scaling
        button, label = Check_Button(' Standardization', font, lblue)
        button.connect("toggled", self.StandardScore, CheckBoxLabel)
        self.table.attach(button, 4, 6, 7, 8)
        CheckBoxLabel.append(label)
        

    #..........Method 2: Returning widgets container........
    def container(self):
        'FeaExtSelClass table for being appended to the notebook'
        return self.table


    #..............Method 3: BP Analysis sub-menu...........
    def BP_opt1(self, widget, BP_menu, RadioLabel, suboption):
        'Absolute Power Analysis Menu'

        if widget.get_active(): 
            if suboption == 1:
                self.feaext_output[0] = 'absolute_bb'            
                #RadioLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            elif suboption == 2:
                self.feaext_output[0] = 'absolute'            
                #RadioLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))                
            self.feaext_output[1] = 'off'
        else:    
            if suboption == 1:
                RadioLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            elif suboption == 2:
                RadioLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
             
                
    #..............Method 4: BP Analysis sub-menu...........
    def BP_opt2(self, widget, BP_menu, RadioLabel):
        'Relative Power Analysis Menu'

        if widget.get_active(): 
            self.feaext_output[0] = 'relative'
            self.feaext_output[1] = 'off'
            #RadioLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black')) 
        else:
            RadioLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))        


#..............Method 5: BP Analysis sub-menu...........
    def BP_opt3(self, widget, BP_menu, RadioLabel):
        'ERD/ERS Analysis Menu'

        if widget.get_active(): 
            self.feaext_output[0] = 'ERD/ERS'
            self.feaext_output[1] = ''
            BP_menu[4].set_editable(True)   
            #RadioLabel[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black')) 
            self.location[0] = [1]
        else:
            BP_menu[4].set_text('')
            BP_menu[4].set_editable(False)
            RadioLabel[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))        


    #............Method 6: Theta Band Selection.............
    def BP_Theta(self, widget, event, BP_menu):
        'theta band selection'

        current_label = BP_menu[0].get_text()
        on_off = current_label.count('*')
        # ON State (Broad Band)
        if on_off == 0:
            BP_menu[0].set_text('Broad theta*: ')
            BP_menu[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            BP_menu[5].set_editable(True)
            self.feaext_output[2] = ['on', '']  
            self.location[1] = [2, 1]   
        # ON State (Upper/Lower Band)
        elif on_off == 1:
            BP_menu[0].set_text('Narrow theta**: ')            
            BP_menu[5].set_text('')
            self.feaext_output[2] = ['off', 'off']
            self.feaext_output[3] = ['on', '']  
            self.feaext_output[4] = ['on', '']  
            self.location[1] = [3, 4, 1]                    
        # OFF State
        else:
            BP_menu[0].set_text('Theta: ')
            BP_menu[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            BP_menu[5].set_text('')
            BP_menu[5].set_editable(False)
            self.feaext_output[2] = ['off', 'off']
            self.feaext_output[3] = ['off', 'off']
            self.feaext_output[4] = ['off', 'off']
            self.location[1] = 0


    #............Method 7: Alpha Band Selection.............
    def BP_Alpha(self, widget, event, BP_menu):
        'alpha band selection'

        current_label = BP_menu[1].get_text()
        on_off = current_label.count('*')
        # ON State (Broad Band)
        if on_off == 0:
            BP_menu[1].set_text('Broad alpha*: ')
            BP_menu[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            BP_menu[6].set_editable(True)
            self.feaext_output[5] = ['on', '']  
            self.location[2] = [5, 1]   
        # ON State (Upper/Lower Band)
        elif on_off == 1:
            BP_menu[1].set_text('Narrow alpha**: ')            
            BP_menu[6].set_text('')
            self.feaext_output[5] = ['off', 'off']
            self.feaext_output[6] = ['on', '']  
            self.feaext_output[7] = ['on', '']  
            self.location[2] = [6, 7, 1]                    
        # OFF State
        else:
            BP_menu[1].set_text('Alpha: ')
            BP_menu[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            BP_menu[6].set_text('')
            BP_menu[6].set_editable(False)
            self.feaext_output[5] = ['off', 'off']
            self.feaext_output[6] = ['off', 'off']
            self.feaext_output[7] = ['off', 'off']
            self.location[2] = 0
        

   #.............Method 8: Beta Band Selection..............
    def BP_Beta(self, widget, event, BP_menu):
        'beta band selection'

        current_label = BP_menu[2].get_text()
        on_off = current_label.count('*')
        # ON State (Broad Band)
        if on_off == 0:
            BP_menu[2].set_text('Broad beta*: ')
            BP_menu[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            BP_menu[7].set_editable(True)
            self.feaext_output[8] = ['on', '']  
            self.location[3] = [8, 1]   
        # ON State (Upper/Lower Band)
        elif on_off == 1:
            BP_menu[2].set_text('Narrow beta**: ')            
            BP_menu[7].set_text('')
            self.feaext_output[8] = ['off', 'off']
            self.feaext_output[9] = ['on', '']  
            self.feaext_output[10] = ['on', '']  
            self.location[3] = [9, 10, 1]                    
        # OFF State
        else:
            BP_menu[2].set_text('Beta: ')
            BP_menu[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            BP_menu[7].set_text('')
            BP_menu[7].set_editable(False)
            self.feaext_output[8]  = ['off', 'off']
            self.feaext_output[9]  = ['off', 'off']
            self.feaext_output[10] = ['off', 'off']
            self.location[3] = 0
        

   #.............Method 9:  Gamma Band Selection...........
    def BP_Gamma(self, widget, event, BP_menu):
        'gamma band selection'

        current_label = BP_menu[3].get_text()
        on_off = current_label.count('*')
        # ON State
        if on_off == 0:
            BP_menu[3].set_text('Gamma*: ')
            BP_menu[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            BP_menu[8].set_editable(True)
            self.feaext_output[11] = ['on', ''] 
            self.location[4] = [11, 1]           
        # OFF State
        else:
            BP_menu[3].set_text('Gamma: ')
            BP_menu[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            BP_menu[8].set_text('')
            BP_menu[8].set_editable(False)
            self.feaext_output[11] = ['off', 'off']
            self.location[4] = 0
        
 
    #.......Method 10: Reading from a text entry box ........
    def read_BP(self, widget, current):
        'Data Extraction from Text-Entries Boxes (BP_menu)'
        
        location = self.location[current]
        new_text = widget.get_text()
        if widget.get_text() != '':            
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information extraction
            allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':',new_text=='.',new_text==';']
            if any(allow):
                if len(location) == 2:
                    self.feaext_output[location[0]][location[1]] = widget.get_text()
                elif len(location) == 3:
                    self.feaext_output[location[0]][location[2]] = widget.get_text() 
                else:
                    self.feaext_output[location[0]] = widget.get_text()                                       
            else:
            # (2) Information error               
                MESSAGE = 'Only the following characters are allowed in Range Selection:\
                           \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> semicolon (;)\
                           \n-> dot (.)\n-> space'
                DialogBox(MESSAGE)                    
                widget.set_text('')
                if len(location) == 2:
                    self.feaext_output[location[0]][location[1]] = '' 
                elif len(location) == 3:
                    self.feaext_output[location[0]][location[2]] = ''
                else:
                    self.feaext_output[location[0]] = ''
    
    
    #.................Method 11: DBI Menu...................
    def DBI(self, widget, CheckBoxLabel):
        'Davis-Bouldin Index Check-Button'

        if widget.get_active():
            self.feasel_output[0] = 'on'
            #CheckBoxLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
            self.feasel_output[0] = 'off'
            CheckBoxLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))


    #.................Method 12: RFE Menu...................
    def RFE(self, widget, FeaSel_menu, CheckBoxLabel):
        'Recursive Feature Elimination Menu'

        if widget.get_active():
            self.feasel_output[1][0] = 'on'
            self.feasel_output[1][1] = 'FDA'
            FeaSel_menu[0].set_active(True)
            FeaSel_menu[1].set_active(False)
            FeaSel_menu[2].set_active(False)
            #CheckBoxLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            for item in FeaSel_menu[:3]: item.show()
        else:
            self.feasel_output[1][0] = 'off'
            CheckBoxLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            for item in FeaSel_menu[:3]: item.hide()


    #..............Method 13: Index Range Menu...............
    def IndexRange(self, widget, FeaSel_menu, CheckBoxLabel):
        'Index Range Insertion Menu'

        if widget.get_active():
            self.feasel_output[2][0] = 'on'
            self.feasel_output[2][1] = ''
            FeaSel_menu[3].set_active(True)
            FeaSel_menu[4].set_active(False)
            FeaSel_menu[-2].set_editable(True)
            FeaSel_menu[-1].set_editable(False)
            for item in FeaSel_menu[3:]: item.show()
        else:
            self.feasel_output[2][0] = 'off'
            self.feasel_output[2][1] = 'off'
            self.feasel_output[3][0] = 'off'
            self.feasel_output[3][1] = 'off'
            FeaSel_menu[-2].set_text('')
            FeaSel_menu[-2].set_editable(True)
            FeaSel_menu[-1].set_text('')
            FeaSel_menu[-1].set_editable(False)
            CheckBoxLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            for item in FeaSel_menu[3:]: item.hide()


    #..............Method 14: DBI-Features Menu...............
    def DBIFeatures(self, widget, FeaSel_menu, RadioLabel):
        'DBI-Feature Selection Menu'

        if widget.get_active():            
            self.feasel_output[2][0] = 'on'
            self.feasel_output[2][1] = ''                
            FeaSel_menu[-2].set_editable(True)           
        else:
            self.feasel_output[2][0] = 'off'
            self.feasel_output[2][1] = 'off'
            FeaSel_menu[-2].set_text('')
            FeaSel_menu[-2].set_editable(False)
            RadioLabel[5].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))            


    #..............Method 15: RFE-Features Menu...............
    def RFEFeatures(self, widget, FeaSel_menu, RadioLabel):
        'RFE-Feature Selection Menu'
        
        if widget.get_active():
            self.feasel_output[3][0] = 'on'
            self.feasel_output[3][1] = ''
            FeaSel_menu[-1].set_editable(True)             
        else:
            self.feasel_output[3][0] = 'off'
            self.feasel_output[3][1] = 'off'
            FeaSel_menu[-1].set_text('')
            FeaSel_menu[-1].set_editable(False)
            RadioLabel[6].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))           


    #....... Method 16: Reading from a text entry box ......
    def read_FeaSel(self, widget, location):
        'Data Extraction from Text-Entries Boxes'

        new_text = widget.get_text()
        if widget.get_text() != '':
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information check-up and extraction
            ## -- only group of integer/float numbers
            allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':',new_text==';']
            if any(allow):
                self.feasel_output[location[0]][location[1]] = widget.get_text()
            else:
                MESSAGE = 'Only the following characters are allowed in this box:\
                           \n-> digits (0-9)\n-> comma (,)\n-> semicolon (;)\n-> space'
                DialogBox(MESSAGE)
                widget.set_text('')
                self.feasel_output[location[0]][location[1]] = ''

        
    #..............Method 17: Classifier Menu...............
    def Classifier(self, widget, data, Sel_Class, RadioLabel, loc):
        'Classifier Menu'

        if widget.get_active():
            if Sel_Class == 'selection':
                self.feasel_output[1][1] = data
            else:
                self.class_output[0] = data
            #RadioLabel[loc].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
            if Sel_Class == 'selection':
                self.feasel_output[1][1] = ''
            else:
                self.class_output[0] = ''
            RadioLabel[loc].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            
            
    #...............Method 18: Standard Score...............
    def StandardScore(self, widget, CheckBoxLabel):
        'Standardization of the Feature Vectors based on Idle States'

        if widget.get_active():
            self.class_output[3] = 'on'
            #CheckBoxLabel[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
            CheckBoxLabel[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            self.class_output[3] = 'off'
      

    #....... Method 19: Reading from a text entry box ......
    def read_Class(self, widget, location):
        'Data Extraction from Text-Entries Boxes'

        new_text = widget.get_text()
        if widget.get_text() != '':
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information check-up and extraction
            ## -- only group of integer/float numbers
            allow = [new_text.isdigit(),new_text.isspace(),new_text==',']
            if any(allow):
                self.class_output[location[0]] = widget.get_text() 
            else:
                MESSAGE = 'Only the following characters are allowed in this box:\
                           \n-> digits (0-9)\n-> comma (,)\n-> space'
                DialogBox(MESSAGE)
                widget.set_text('')
                self.class_output[location[0]] = ''


    #.....Method 20: Final acquisition from FeaExt menu......
    def outcomes(self):
        'FeaExtClass_menu final results'

        # theta band splitting
        if self.feaext_output[3][0]  == 'on':            
            bands = self.feaext_output[3][1].split(';')
            self.feaext_output[3][1] = bands[0]
            self.feaext_output[4][1] = bands[1]
        # alpha band spliting
        if self.feaext_output[6][0]  == 'on':            
            bands = self.feaext_output[6][1].split(';')
            self.feaext_output[6][1] = bands[0]
            self.feaext_output[7][1] = bands[1]
        if self.feaext_output[9][0]  == 'on':            
            bands = self.feaext_output[9][1].split(';')
            self.feaext_output[9][1]  = bands[0]
            self.feaext_output[10][1] = bands[1] 
        return self.feaext_output, self.feasel_output, self.class_output


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# USEFUL NOTES
# (1)
# If you return FALSE in the "delete_event" signal handler,
# GTK will emit the "destroy" signal. Returning TRUE means
# you don’t want the window to be destroyed.
# (2)
# If you are using multiple windows, you have to use "destroy_event"
# for the sub-windows for eliminating everything and therefore
# avoiding errors.
# (3)
# - Delete is just for sending a message that the user maybe want to close
# the application (pushing red cross of the window)
# - Destroy is for quitting the application without asking.
