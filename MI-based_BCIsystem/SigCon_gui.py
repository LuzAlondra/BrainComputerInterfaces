### VE PROJECT: Brain-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### June 27th, 2011

# ************************************
# * BCI Design - Graphical Interface *
# *      SIGNAL CONDITIONING         *
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
# "SigCon_menu" CLASS DECLARATION

class SigCon_menu():
    'Class to control the "SigCon_interface" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "SigCon_interface" menu'

        # ============== Variable Declaration ==============
        blue = '#466289'
        lblue = '#A0AEC1'
        orange = '#FA6121'
        large_font = 'Trebuchet 16'
        font = "Trebuchet 14"
        sigcon_menu, CheckBoxLabel, RadioLabel = [], [], []
        ##-- Out data from SigCon_menu class
        self.sigcon_output = ['', ['Monopolar', ''], '', 'off', 'off', ['off', 'off']]
        
        # ========= SigCon_interface tab creation ==========        
        # (1) TABLE: Widget container
        ## --14 x 6 table creation
        self.table = gtk.Table(14, 6, True)

        # (2) LABEL: Window title
        titulo = Label(' BCI System - Signal Processing', 'Neuropol 20', blue, 0, 0.5)
        self.table.attach(titulo, 0, 5, 0, 1)
        subtitulo = Label(' A VE Plataform for Simulated BCI-Enabled Independent Living', \
                          'Neuropol 18', orange, 0, 0.5)
        self.table.attach(subtitulo, 0, 5, 1, 2)

        # (3) IMAGES: General menu & EEG layout
        url = 'Images\\minilogo.jpg'
        logo = Image(url)
        logo.set_alignment(xalign=0.5, yalign=0.5)
        self.table.attach(logo, 5, 6, 0, 2)
        url = 'Images\\layout.png'
        eeg = Image(url)
        eeg.set_alignment(xalign=0.8, yalign=0)
        self.table.attach(eeg, 2, 6, 2, 14)

        # (4) LABEL & TEXT-ENTRY: downsampling rate submenu 
        tempo = Label('DOWNSAMPLE RATE', large_font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 2, 3)
        icon = Image('Images\\downsampling.png') 
        icon.set_alignment(xalign=0.2, yalign=0)
        self.table.attach(icon, 2, 3, 2, 4)
        tempo = TextEntry(self.read_text, [0])
        self.table.attach(tempo, 1, 2, 3, 4)
        sigcon_menu.append(tempo)
        
        # (5) LABEL, RADIO BUTTONS & TEXT-ENTRY: spatial filtering submenu
        tempo = Label('SPATIAL FILTERING', large_font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 4, 5)
        icon = Image('Images\\filter.png') 
        icon.set_alignment(xalign=0.2, yalign=0)
        self.table.attach(icon, 2, 3, 4, 6)
        ##-- monopolar referencing
        tempo, label = Radio_Button(None, 'Monopolar', font, 'black')
        RadioLabel.append(label)
        tempo.connect("toggled", self.Monopolar, sigcon_menu, RadioLabel)
        self.table.attach(tempo, 0, 1, 5, 6)
        ##-- bipolar referencing
        tempo, label = Radio_Button(tempo, 'Bipolar', font, lblue)
        RadioLabel.append(label)
        tempo.connect("toggled", self.Bipolar, sigcon_menu, RadioLabel)
        self.table.attach(tempo, 0, 1, 6, 7)
        ##-- small Laplace referencing
        tempo, label = Radio_Button(tempo, 'Small Laplacian', font, lblue)
        RadioLabel.append(label)
        tempo.connect("toggled", self.SLaplace, sigcon_menu, RadioLabel)
        self.table.attach(tempo, 0, 1, 7, 8)
        ##-- large Laplace referencing
        tempo, label = Radio_Button(tempo, 'Large Laplacian', font, lblue)
        RadioLabel.append(label)
        tempo.connect("toggled", self.LLaplace, sigcon_menu, RadioLabel)
        self.table.attach(tempo, 0, 1, 8, 9)
        ##-- CAR referencing
        tempo, label = Radio_Button(tempo, 'Common average', font, lblue)
        RadioLabel.append(label)
        tempo.connect("toggled", self.CAR, sigcon_menu, RadioLabel)
        self.table.attach(tempo, 0, 1, 9, 10)
        ##-- positive electrodes
        tempo = Label('+ Channels', font, 'black', 0.5, 0.5)
        self.table.attach(tempo, 1, 2, 6, 7)
        tempo = TextEntry(self.read_text, [2])
        tempo.set_editable(True)
        self.table.attach(tempo, 1, 2, 7, 8)
        sigcon_menu.append(tempo)
        ##-- negative electrodes
        tempo = Label('- Channels', font, 'black', 0.5, 0.5)
        self.table.attach(tempo, 1, 2, 8, 9)
        tempo = TextEntry(self.read_text, [1,1])
        tempo.set_editable(True)
        self.table.attach(tempo, 1, 2, 9, 10)
        sigcon_menu.append(tempo)


        # (6) LABEL, CHECK BUTTONS & TEXTENTRY: spectral filtering submenu
        tempo = Label('SPECTRAL FILTERING', large_font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 10, 11)
        icon = Image('Images\\filter.png') 
        icon.set_alignment(xalign=0.2, yalign=0)
        self.table.attach(icon, 2, 3, 10, 12)
        ##-- 50Hz rejection
        button, label = Check_Button(' 50Hz-rejection', font, lblue)
        button.connect("toggled", self.Rejection, CheckBoxLabel)
        self.table.attach(button, 0, 1, 11, 12)
        CheckBoxLabel.append(label)
        ##-- DC removal
        button, label = Check_Button(' DC removal', font, lblue)
        button.connect("toggled", self.DCRemoval, CheckBoxLabel)
        self.table.attach(button, 0, 1, 12, 13)
        CheckBoxLabel.append(label)
        ##-- bandwidth
        button, label = Check_Button(' Bandwidth(fH:fL)', font, lblue)
        button.connect("toggled", self.bandwidth, sigcon_menu, CheckBoxLabel)
        self.table.attach(button, 0, 1, 13, 14)
        CheckBoxLabel.append(label)
        tempo = TextEntry(self.read_text, [5,1])
        tempo.set_editable(False)
        self.table.attach(tempo, 1, 2, 13, 14)
        sigcon_menu.append(tempo)

        self.table.show()
        

    #..........Method 2: Returning widgets container........
    def container(self):
        'SigCon table for being appended to the notebook'
        return self.table


    #................Method 3: Monoplar selection...........
    def Monopolar(self, widget, sigcon_menu, RadioLabel):
        'Ear referencing selection'

        if widget.get_active():
            self.sigcon_output[1] = ['Monopolar', '']
            sigcon_menu[2].set_editable(True)
            sigcon_menu[1].set_text('')
            sigcon_menu[2].set_text('')    
            #RadioLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))        
        else:
            self.sigcon_output[1] = ['', '']
            RadioLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 

            
    #...............Method 4: Bipolar selection.............
    def Bipolar(self, widget, sigcon_menu, RadioLabel):
        'Bipolar referencing selection'

        if widget.get_active():
            self.sigcon_output[1] = ['Bipolar', '']
            sigcon_menu[2].set_editable(True)
            sigcon_menu[1].set_text('')
            sigcon_menu[2].set_text('')
            #RadioLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black')) 
        else:
            self.sigcon_output[1] = ['', '']
            RadioLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 


    #............Method 5: Small Laplace selection..........
    def SLaplace(self, widget, sigcon_menu, RadioLabel):
        'Small Laplace referencing selection'

        if widget.get_active():
            self.sigcon_output[1] = ['SmallLaplacian', 'off']
            sigcon_menu[1].set_text('')
            sigcon_menu[2].set_text('')
            sigcon_menu[2].set_editable(False)
            #RadioLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black')) 
        else:
            self.sigcon_output[1]= ['', '']
            RadioLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 


    #............Method 6: Large Laplace selection..........
    def LLaplace(self, widget,sigcon_menu, RadioLabel):
        'Large Laplace referencing selection'

        if widget.get_active():
            self.sigcon_output[1] = ['LargeLaplacian', 'off']
            sigcon_menu[1].set_text('')
            sigcon_menu[2].set_text('')
            sigcon_menu[2].set_editable(False)
            #RadioLabel[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black')) 
        else:
            self.sigcon_output[1] = ['', '']
            RadioLabel[3].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 


    #.................Method 7: CAR selection...............
    def CAR(self, widget, sigcon_menu, RadioLabel):
        'CAR referencing selection'

        if widget.get_active():
            self.sigcon_output[1] = ['CAR', 'off']
            sigcon_menu[1].set_text('')
            sigcon_menu[2].set_text('')
            sigcon_menu[2].set_editable(False)
            #RadioLabel[4].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black')) 
        else:
            self.sigcon_output[1] = ['', '']
            RadioLabel[4].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue)) 


    #................Method 8: 50Hz selection...............
    def Rejection(self, widget, CheckBoxLabel):
        '50Hz Rejection selection'

        if widget.get_active():
            self.sigcon_output[3] = 'on'
            #CheckBoxLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
            self.sigcon_output[3] = 'off'
            CheckBoxLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))


    #.................Method 9: DC Removal..................
    def DCRemoval(self, widget, CheckBoxLabel):
        'DC Removal selection'

        if widget.get_active():
            self.sigcon_output[4] = 'on'
            #CheckBoxLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
            self.sigcon_output[4] = 'off'
            CheckBoxLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))


    #..............Method 10: bandwidth selection............
    def bandwidth(self, widget, sigcon_menu, CheckBoxLabel):
        'BandWidth selection'

        if widget.get_active():
            self.sigcon_output[5] = ['on', '']
            sigcon_menu[3].set_editable(True)
            #CheckBoxLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
            self.sigcon_output[5] = ['off', 'off']
            sigcon_menu[3].set_editable(False)
            CheckBoxLabel[2].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))


    #.......Method 11: Reading from a text entry box .......
    def read_text(self, widget, location):
        'Data Extraction from Text-Entries Boxes'

        new_text = widget.get_text()
        if widget.get_text() != '':
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information check-up and extraction
            ## -- only integer options --> downsampling rate
            if location == [0]:
                if new_text.isdigit():
                    self.sigcon_output[location[0]] = widget.get_text()
                else:
                    MESSAGE = 'Downsampling Rate must be an INTEGER'
                    DialogBox(MESSAGE)
                    widget.set_text('')
                    self.sigcon_output[location[0]] = ''
            ## -- only range selection option --> channels and bandwidth
            else:
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':']
                if location == [4,1]: allow.append(new_text=='.')                
                if any(allow):
                    if len(location) == 1:
                        self.sigcon_output[location[0]] = widget.get_text()
                    else:
                        self.sigcon_output[location[0]][location[1]] = widget.get_text()                   
                else:
                    MESSAGE = 'Only the following characters are allowed in Range Selection:\
                               \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> space'
                    DialogBox(MESSAGE)
                    widget.set_text('')
                    if len(location) == 1:
                        self.sigcon_output[location[0]] = ''
                    else:
                        self.sigcon_output[location[0]][location[1]] = ''
                        

    #....Method 12: Final acquisition from SigCon menu......
    def outcomes(self):
        'SigCon_menu final results'
        
        return self.sigcon_output

        
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# USEFUL NOTES
# (1)
# If you return FALSE in the "delete_event" signal handler,
# GTK will emit the "destroy" signal. Returning TRUE means
# you don't want the window to be destroyed.
# (2)
# If you are using multiple windows, you have to use "destroy_event"
# for the sub-windows for eliminating everything and therefore
# avoiding errors.
# (3)
# - Delete is just for sending a message that the user maybe want to close
# the application (pushing red cross of the window)
# - Destroy is for quitting the application without asking.