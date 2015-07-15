# -*- coding: cp1252 -*-
### VE PROJECT: Brain-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### June 27th, 2011

# ************************************
# * BCI Design - Graphical Interface *
# *          PLOTTING                *
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
     Radio_Button,TextEntry, Check_Button


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL VARIABLES DECLARATION
window = ['Bartlett','Blackman','Boxcar','Flat Top','Gaussian','Hamming','Hanning','Triangular']

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
# "PlotS_menu" CLASS DECLARATION

class PlotS_menu():
    'Class to control the "PlotS_interface" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "PlotS_interface" menu'

        # ============== Variable Declaration ==============
        blue = '#466289'
        lblue = '#A0AEC1'
        orange = '#FA6121'
        large_font = 'Trebuchet 16'
        font = "Trebuchet 14"
        small_font = "Trebuchet 12"
        self.menu_labels, self.Requires_menu, self.menu_checkboxes, CheckBoxLabel = [], [], [], []
        ##-- Out data form PlotS_menu class
        self.plots_output = ['off','off','off','off','off','off','off',['off','off','off','off','off','off','off','off','off','off']]
                
        # ========== PlotS_interface tab creation ==========        
        # (1) TABLE: Widget container
        ## -- 14 x 6 table creation
        self.table = gtk.Table(14, 6, True)

        # (2) LABEL: Window title
        titulo = Label(' BCI System - PlotS', 'Neuropol 20', blue, 0, 0.5)
        self.table.attach(titulo, 0, 5, 0, 1)
        subtitulo = Label(' A VE Plataform for Simulated BCI-Enabled Independent Living', \
                          'Neuropol 18', orange, 0, 0.5)
        self.table.attach(subtitulo, 0, 5, 1, 2)

        # (3) IMAGES: General menu images
        url = 'Images\\minilogo.jpg'
        logo = Image(url)
        logo.set_alignment(xalign=0.5, yalign=0.5)
        self.table.attach(logo, 5, 6, 0, 2)
        
        # (4) LABELS & IMAGES: Titles and Requirements Menu
        ## -- Title 1
        tempo = Label(' OFFLINE ANALYSIS ', large_font, 'black', 0.5, 0.5)
        self.table.attach(tempo, 0, 2, 2, 4)
        ## -- subtitle 1.1
        tempo = Label('1|  Spectral information', font, 'black', 0, 0.5)
        self.table.attach(tempo, 0, 2, 4, 5)
        icon = Image('Images\\spectro.png') 
        icon.set_alignment(xalign=0.1, yalign=0.5)
        self.table.attach(icon, 2, 3, 4, 6)
        ## -- subtitle 1.2
        tempo = Label('2|  Feature distribution', font, 'black', 0, 0.5)
        self.table.attach(tempo, 0, 2, 6, 7)
        icon = Image('Images\\histo.png') 
        icon.set_alignment(xalign=0.1, yalign=1)
        self.table.attach(icon, 2, 3, 6, 8)
        ## -- subtitle 1.3
        tempo = Label('3|  Time-course of motor imagery', font, 'black', 0, 0.5)
        self.table.attach(tempo, 0, 3, 8, 9) 
        icon = Image('Images\\erds.png') 
        icon.set_alignment(xalign=0.1, yalign=0)
        self.table.attach(icon, 2, 3, 9, 11)       
        ## -- Title 2
        tempo = Label(' ONLINE ANALYSIS ', large_font, 'black', 0.5, 0.5)
        self.table.attach(tempo, 0, 2, 11, 13)        
        icon = Image('Images\\xy.png') 
        icon.set_alignment(xalign=0.1, yalign=1)
        self.table.attach(icon, 2, 3, 12, 14)
        ## -- Title 3
        tempo = Label('REQUIREMENTS', large_font, 'black', 0.5, 0.5)
        self.table.attach(tempo, 4, 6, 2, 4)        
        ## -- Feature Plotting Menu
        tempo = Label('Left / right / idle: ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 4, 5) 
        self.menu_labels.append(tempo)
        tempo = Label('+ Channels: ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 5, 6)   
        self.menu_labels.append(tempo)     
        tempo = Label('Trials (BS1;BS2;...): ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 6, 7)
        self.menu_labels.append(tempo)
        tempo = Label('Samples (BS1;BS2;...): ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 7, 8)
        self.menu_labels.append(tempo)
        tempo = Label('Time window [s]: ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 8, 9)
        self.menu_labels.append(tempo)         
        tempo = Label('Window type: ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 9, 10) 
        self.menu_labels.append(tempo) 
        tempo = Label('Overlapping rate [%]: ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 10, 11)  
        self.menu_labels.append(tempo) 
        tempo = Label('Overlapping brain states? (psd/histo/both/none): ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 11, 12)
        self.menu_labels.append(tempo) 
        tempo = Label('Overlapping channels in PSD? (y/n): ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 12, 13)
        self.menu_labels.append(tempo) 
        tempo = Label('Reference intervals: ', font, lblue, 1, 0.5)
        self.table.attach(tempo, 2, 5, 13, 14)
        self.menu_labels.append(tempo)    
        
        # (5) TEXT-ENTRY:  Plot Requirements Menu
        tempo = TextEntry(self.read_Requirements, [7,0])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 4, 5)
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,1])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 5, 6)
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,2])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 6, 7)
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,3])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 7, 8)
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,4])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 8, 9)
        self.Requires_menu.append(tempo) #just for compatibility
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,6])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 10, 11)
        self.Requires_menu.append(tempo)   
        tempo = TextEntry(self.read_Requirements, [7,7])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 11, 12)
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,8])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 12, 13)
        self.Requires_menu.append(tempo)
        tempo = TextEntry(self.read_Requirements, [7,9])
        tempo.set_editable(False)
        self.table.attach(tempo, 5, 6, 13, 14)
        self.Requires_menu.append(tempo)
                
        # (6) CHECK BUTTONS: offline/online analysis selection
        button, label = Check_Button(' Spectrogram', font, lblue)
        button.connect("toggled", self.Plots, 0, CheckBoxLabel)
        self.table.attach(button, 0, 1, 5, 6) 
        self.menu_checkboxes.append(button)      
        CheckBoxLabel.append(label)  
        button, label = Check_Button(' PSD', font, lblue)
        button.connect("toggled", self.Plots, 1, CheckBoxLabel)
        self.table.attach(button, 1, 2, 5, 6) 
        self.menu_checkboxes.append(button)        
        CheckBoxLabel.append(label)
        button, label = Check_Button(' Boxplot', font, lblue)
        button.connect("toggled", self.Plots, 2, CheckBoxLabel)
        self.table.attach(button, 0, 1, 7, 8)
        self.menu_checkboxes.append(button)
        CheckBoxLabel.append(label)
        button, label = Check_Button(' Histogram', font, lblue)
        button.connect("toggled", self.Plots, 3, CheckBoxLabel)
        self.table.attach(button, 1, 3, 7, 8)
        self.menu_checkboxes.append(button)
        CheckBoxLabel.append(label)
        button, label = Check_Button(' 2D ERD/ERS\n map', font, lblue)
        button.connect("toggled", self.Plots, 4, CheckBoxLabel)
        self.table.attach(button, 0, 1, 9, 11)
        self.menu_checkboxes.append(button)
        CheckBoxLabel.append(label)
        button, label = Check_Button(' 3D ERD/ERS\n map', font, lblue)
        button.connect("toggled", self.Plots, 5, CheckBoxLabel)
        self.table.attach(button, 1, 3, 9, 11)
        self.menu_checkboxes.append(button)
        CheckBoxLabel.append(label)
        button, label = Check_Button(' XY-plot of features', font, lblue)
        button.connect("toggled", self.Plots, 6, CheckBoxLabel)
        self.table.attach(button, 0, 3, 13, 14)
        self.menu_checkboxes.append(button)
        CheckBoxLabel.append(label)
        
        # (7) COMBOBOXENTRY: window type selection
        self.combobox = gtk.combo_box_new_text()
        for item in window: self.combobox.append_text(item)
        self.combobox.connect('changed', self.selwin)
        self.table.attach(self.combobox, 5, 6, 9, 10)
        self.combobox.show()        

        self.table.show()
        

    #..........Method 2: Returning widgets container........

    def container(self):
        'Class table for being appended to the notebook'
        return self.table


    #.........Method 3: ComboTextEntry selection............
    def selwin(self, widget):
        'Reading from the ComboTextEntry'
        
        location = widget.get_active()
        self.plots_output[7][5] = window[location]


    #......... Method 4: Plots CheckBoxes menu .............
    def Plots(self, widget, current_checkbox, CheckBoxLabel):
        'Spectrogram/PDS/BoxPlot/Histogram/ERSD/XYPlot Menu'
        
        lblue = '#A0AEC1'        
        # (1) Only Spectrogram/PSD selection or deselection
        #      WINDOW TYPE & OVERLAPING
        tempo = []
        for item in self.menu_checkboxes[:2]: tempo.append(item.get_active())
        if any(tempo):
            for item in self.menu_labels[5:7]: item.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            for item in self.Requires_menu[5:7]: item.set_editable(True) 
            for index in [5,6]: 
                if self.plots_output[7][index] == 'off': self.plots_output[7][index] = ''                      
        else:
            for item in self.menu_labels[5:7]: item.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            for item in self.Requires_menu[5:7]:
                item.set_text('')
                item.set_editable(False)
                self.combobox.set_active(-1)
            self.plots_output[7][5:7] = ['off','off']
        # (2) Only Spectrogram/PDS/ERDS selection or deselection
        #     SAMPLES & TIME WINDOW
        tempo = []
        for index in [0,1,4,5]: tempo.append(self.menu_checkboxes[index].get_active())
        if any(tempo):
            for item in self.menu_labels[3:5]: item.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            for item in self.Requires_menu[3:5]: item.set_editable(True) 
            for index in [3,4]:
                if self.plots_output[7][index] == 'off':  self.plots_output[7][index] = ''                 
        else:
            for item in self.menu_labels[3:5]: item.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            for item in self.Requires_menu[3:5]: 
                item.set_text('') 
                item.set_editable(False) 
            self.plots_output[7][3:5] = ['off', 'off']
        # (3) Only Spectrogram/PDS/ERDS selection or deselection
        #     BRAIN STATE & TRIALS
        tempo = []
        for index in [0,1,4,5]: tempo.append(self.menu_checkboxes[index].get_active())
        if any(tempo):
            for index in [0,2]:
                self.menu_labels[index].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
                self.Requires_menu[index].set_editable(True)  
                if self.plots_output[7][index] == 'off':  self.plots_output[7][index] = ''       
        else:
            for index in [0,2]:            
                self.menu_labels[index].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
                self.Requires_menu[index].set_text('') 
                self.Requires_menu[index].set_editable(False) 
                self.plots_output[7][index] = 'off'         
        # (4) Only PSD/Histogram selection or deselection
        #     OVERLAPPING
        tempo = []
        for index in [1,3]: tempo.append(self.menu_checkboxes[index].get_active())
        if any(tempo):
            self.menu_labels[7].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            self.Requires_menu[7].set_editable(True)
            if self.plots_output[7][7] == 'off': self.plots_output[7][7] = ''
        else:
            self.menu_labels[7].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            self.Requires_menu[7].set_text('') 
            self.Requires_menu[7].set_editable(False) 
            self.plots_output[7][7] = 'off'
        # (5) Only Spectrogram/PSD/ERDSmaps selection or deselection
        #     CHANNELS
        tempo = []
        for index in [0,1,4,5]: tempo.append(self.menu_checkboxes[index].get_active())
        if any(tempo):  
            self.menu_labels[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            self.Requires_menu[1].set_editable(True)
            if self.plots_output[7][1] == 'off': self.plots_output[7][1] = ''
        else:
            self.menu_labels[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            self.Requires_menu[1].set_text('') 
            self.Requires_menu[1].set_editable(False) 
            self.plots_output[7][1] = 'off'        
        # (6) Only ERDSmaps selection or deselection
        #     ERDS ESTIMATES
        tempo = []
        for index in [4,5]: tempo.append(self.menu_checkboxes[index].get_active())
        if any(tempo):  
            self.menu_labels[9].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            self.Requires_menu[9].set_editable(True)
            if self.plots_output[7][9] == 'off': self.plots_output[7][9] = ''
        else:
            self.menu_labels[9].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            self.Requires_menu[9].set_text('') 
            self.Requires_menu[9].set_editable(False) 
            self.plots_output[7][9] = 'off'        
        # (7) Only PSD selection or deselection
        #     CHANNELS & OVERLAPPING
        if self.menu_checkboxes[1].get_active():  
            self.menu_labels[8].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            self.Requires_menu[8].set_editable(True)
            if self.plots_output[7][8] == 'off': self.plots_output[7][8] = ''
        else:
            self.menu_labels[8].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            self.Requires_menu[8].set_text('') 
            self.Requires_menu[8].set_editable(False) 
            self.plots_output[7][8] = 'off'
        # (8) Only XY-plot selection or deselection
        if self.menu_checkboxes[6].get_active():                                
            for item in self.menu_checkboxes[:6]: item.set_active(False)          
        # (9) Turn ON tha appropriated checkbox
        if widget.get_active():
            self.plots_output[current_checkbox] = 'on'
            #CheckBoxLabel[current_checkbox].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:            
            self.plots_output[current_checkbox] = 'off'       
            CheckBoxLabel[current_checkbox].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
               
    
    #....... Method 8: Reading from a text entry box .......
    def read_Requirements(self, widget, location):
        'Data Extraction from Text-Entries Boxes'

        new_text = widget.get_text()
        if widget.get_text() != '':
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information check-up and extraction
            loc  = [location == [7,1], location == [7,10]]
            locA = [location == [7,2], location == [7,3]]
            locB = [location == [7,4], location == [7,6]]
            locC = [location == [7,7], location == [7,8], location == [7,9]]
            ## -- only group of integers -> MENTAL STATUS
            if location == [7, 0]:
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',']
                if any(allow):
                    self.plots_output[location[0]][location[1]] = widget.get_text()                     
                else:
                    MESSAGE = 'Only the following characters are allowed in this box:\
                               \n-> digits (0-9)\n-> comma (,)\n-> space'
                    DialogBox(MESSAGE)
                    widget.set_text('')
                    self.plots_output[location[0]][location[1]] = ''                     
            ## -- only range selection option -> CHANNELS, ERDS ESTIMATES
            elif any(loc):
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':']
                if any(allow):
                    self.plots_output[location[0]][location[1]] = widget.get_text() 
                else:                      
                    MESSAGE = 'Only the following characters are allowed in Range Selection:\
                               \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> space'
                    DialogBox(MESSAGE)
                    widget.set_text('')
                    self.plots_output[location[0]][location[1]] = ''         
            ## -- only combined range selection option -> TRIALS AND SAMPLES
            elif any(locA):
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':',new_text==';']
                if any(allow):
                    self.plots_output[location[0]][location[1]] = widget.get_text()                     
                else:
                    MESSAGE = 'Only the following characters are allowed in Combined Range Selection:\
                               \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> semicolon (;)\n-> dot(.)\n-> space'
                    DialogBox(MESSAGE)
                    widget.set_text('')
                    self.plots_output[location[0]][location[1]] = ''                    
            ## -- only float option -> WINDOW LENGTH AND OVERLAPPING
            elif any(locB):
                allow = [new_text.isdigit(),new_text=='.']
                if any(allow):
                    self.plots_output[location[0]][location[1]] = widget.get_text()
                else:
                    MESSAGE = 'Window Length and Overlapping selection must be a FLOAT or an INTEGER'
                    DialogBox (MESSAGE)
                    widget.set_text('')
                    self.plots_output[location[0]][location[1]] = ''  
            ## -- only string option -> BRAIN STATES/CHANNELS OVERLAPPING/SCALED FEATURES            
            elif any(locC):
                self.plots_output[location[0]][location[1]] = widget.get_text()
                        
    
    #........Method 9: Final acquisition from SVM menu........
    def outcomes(self):
        'Class_menu final results'
        
        return self.plots_output


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