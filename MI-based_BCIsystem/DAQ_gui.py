### VE PROJECT: Brain-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### June 27th, 2011

# ************************************
# * BCI Design - Graphical Interface *
# *        DATA ACQUISITION          *
# ************************************



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
from __future__ import division
import audiere
import pygtk
pygtk.require('2.0')
import cPickle
import gtk
import pango
import gobject
import time
import scipy as sp
from scipy import io
import numpy as np
from socket import *
import matplotlib
import matplotlib.pyplot as plt
# .................. GUI Design Libraries ..................
from Constructors_gui import Image,Label,Frame,Button_Label,Radio_Button,TextEntry,Event_Image
# ................. DAQ and DSP processing .................
from DSP_Functions import spectral_filter,bits_float, SiGCoN



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL VARIABLES DECLARATION
lblue  = '#A0AEC1'
blue   = '#466289'
orange = '#FA6121'
root = 'C:\\Documents and Settings\\lmalon\\Desktop\\'
# ---- 64 electrodes matrix according to BioSemi Layout ----
layout = np.array([[ 0,  0,  0,  1, 33, 34,  0,  0,  0],
                   [ 2,  0,  3,  0, 37,  0, 36,  0, 35],
                   [ 7,  6,  5,  4, 38, 39, 40, 41, 42],
                   [ 8,  9, 10, 11, 47, 46, 45, 44, 43],
                   [15, 14, 13, 12, 48, 49, 50, 51, 52],
                   [16, 17, 18, 19, 32, 56, 55, 54, 53],
                   [23, 22, 21, 20, 31, 57, 58, 59, 60],
                   [25,  0, 26,  0, 30,  0, 63,  0, 62],
                   [ 0,  0,  0, 27, 29, 64,  0,  0,  0]], dtype = int)



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION
# F1. Dialog Box design to send a warning
def DialogBox(MESSAGE, TITLE):
    'Warning Information Delivery'

    message = Label(MESSAGE,'Trebuchet 14', 'black', 0, 0)
    dialog = gtk.Dialog(TITLE,None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,("OK", True))
    STYLE = dialog.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = dialog.get_colormap().alloc_color('#DCDCDC')
    dialog.set_style(STYLE)
    dialog.vbox.pack_start(message)
    dialog.show_all()
    dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    result = dialog.run()
    if result: dialog.destroy()
    dialog.destroy()  



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# "DAQ_menu" CLASS DECLARATION

class DAQ_menu():
    'Class to control the "DAQ_interface" tab'

    #.............Method 1: Initialization Process..........
    def __init__(self):        
        'Initial method to generate the "DAQ_interface" menu'

        # ============== Variable Declaration ==============
        tab_bg = '#DCDCDC'
        small_font = "Trebuchet 12"
        large_font = 'Trebuchet 16'
        font = "Trebuchet 14"
        OffLine_menu, OnLine_menu, RadioLabel = [], [], []
        ##-- Out data from DAQ_menu class
        self.daq_output = ['offline', [], '', 'off', '', '', '', '', '', '', '']
        
        # ========== DAQ_interface tab creation ============        
        # (1) TABLE: Widget container
        ## --14 x 6 table creation
        self.table = gtk.Table(14, 6, True)

        # (2) LABEL: Window title
        titulo = Label(' BCI System - Data Acquisition', 'Neuropol 20', blue, 0, 0.5)
        self.table.attach(titulo, 0, 5, 0, 1)
        subtitulo = Label(' A VE Plataform for Simulated BCI-Enabled Independent Living', \
                          'Neuropol 18', orange, 0, 0.5)
        self.table.attach(subtitulo, 0, 5, 1, 2)

        # (3) IMAGES: General menu images
        url = 'Images\\minilogo.jpg'
        logo = Image(url)
        logo.set_alignment(xalign=0.5, yalign=0.5)
        self.table.attach(logo, 5, 6, 0, 2)
 
        # (4) RADIO-BUTTONS: Offline & Online Selection
        ## -- Offline selection
        option1, label = Radio_Button(None, ' OFFLINE BCI SYSTEM', large_font, 'black')
        RadioLabel.append(label)
        self.mnum = 0
        option1.connect("toggled", self.OffLine, OffLine_menu, RadioLabel)
        self.table.attach(option1, 0, 2, 2, 4)
        icon = Image('Images\\offline.png') 
        icon.set_alignment(xalign = 0.75, yalign = 0.5)
        self.table.attach(icon, 1, 2, 2, 4)
        

        # (5) LABELS: offline & online submenu selection
        ## -- OffLine selection
        tempo = Label('', font, lblue, 0.5, 0.5)
        self.table.attach(tempo, 0, 1, 4, 5)
        OffLine_menu.append(tempo)
        tempo = Label('', font, lblue, 0.5, 0.5)
        self.table.attach(tempo, 1, 2, 4, 5)
        OffLine_menu.append(tempo)
        tempo = Label('Biosemi cap electrodes: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 5, 6)
        OffLine_menu.append(tempo)
        tempo = Label('External electrodes: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 6, 7)
        OffLine_menu.append(tempo)        
        tempo = Label('Bad electrodes: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 7, 8)
        OffLine_menu.append(tempo)        
        tempo = Label('Training trials (BS1;BS2;...): ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 8, 9)
        OffLine_menu.append(tempo)
        tempo = Label('Testing trials (BS1;BS2;...): ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 9, 10)
        OffLine_menu.append(tempo)
        tempo = Label('Samples per trial (BS1;BS2;...): ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 10, 11)
        OffLine_menu.append(tempo)
        tempo = Label('Segmentation length (BS1;BS2;...): ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 11, 12)
        OffLine_menu.append(tempo)
        tempo = Label('Overlapping rate [%]: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 12, 13)
        OffLine_menu.append(tempo)
        tempo = Label('Sample rate [Hz]: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 0, 2, 13, 14)
        OffLine_menu.append(tempo)
        ## -- OnLine selection
        tempo = Label('ActiveTwo hostname: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 4, 5)
        OnLine_menu.append(tempo)
        tempo = Label('Assistive-software hostname: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 5, 6)
        OnLine_menu.append(tempo)
        tempo = Label('Bytes in TCP array: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 6, 7)
        OnLine_menu.append(tempo)
        tempo = Label('Biosemi cap electrodes: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 7, 8)
        OnLine_menu.append(tempo)        
        tempo = Label('External electrodes: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 8, 9)
        OnLine_menu.append(tempo)        
        tempo = Label('Samples for controlling: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 9, 10)
        OnLine_menu.append(tempo)
        tempo = Label('Samples for referencing: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 10, 11)
        OnLine_menu.append(tempo)        
        tempo = Label('Segmentation length [s]: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 11, 12)
        OnLine_menu.append(tempo)
        tempo = Label('Overlapping rate [%]: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 12, 13)
        OnLine_menu.append(tempo)
        tempo = Label('Sample rate [Hz]: ', font, 'black', 1, 0.5)
        self.table.attach(tempo, 3, 5, 13, 14)
        OnLine_menu.append(tempo)

        # (6) TEXT-ENTRY BOXES: selection panel for previous submenus
        ## -- OffLine selection
        tempo = TextEntry( self.read_offline, 2)
        self.table.attach(tempo, 2, 3, 5, 6)
        OffLine_menu.append(tempo)        
        tempo = TextEntry( self.read_offline, 3)
        self.table.attach(tempo, 2, 3, 6, 7)
        OffLine_menu.append(tempo)        
        tempo = TextEntry( self.read_offline, 10)
        self.table.attach(tempo, 2, 3, 7, 8)
        OffLine_menu.append(tempo)        
        tempo = TextEntry( self.read_offline, 5)
        self.table.attach(tempo, 2, 3, 8, 9)
        OffLine_menu.append(tempo)        
        tempo = TextEntry( self.read_offline, 6)
        self.table.attach(tempo, 2, 3, 9, 10)
        OffLine_menu.append(tempo)        
        tempo = TextEntry( self.read_offline, 4)
        self.table.attach(tempo, 2, 3, 10, 11)
        OffLine_menu.append(tempo)
        tempo = TextEntry( self.read_offline, 8)
        self.table.attach(tempo, 2, 3, 11, 12)
        OffLine_menu.append(tempo)
        tempo = TextEntry( self.read_offline, 9)
        self.table.attach(tempo, 2, 3, 12, 13)
        OffLine_menu.append(tempo)
        tempo = TextEntry( self.read_offline, 7)
        self.table.attach(tempo, 2, 3, 13, 14)
        OffLine_menu.append(tempo)
        ## -- OnLine selection
        tempo = TextEntry( self.read_online, 1)
        self.table.attach(tempo, 5, 6, 4, 5)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 10)
        self.table.attach(tempo, 5, 6, 5, 6)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 2)
        self.table.attach(tempo, 5, 6, 6, 7)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 3)
        self.table.attach(tempo, 5, 6, 7, 8)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 4)
        self.table.attach(tempo, 5, 6, 8, 9)
        OnLine_menu.append(tempo)        
        tempo = TextEntry( self.read_online, 8)
        self.table.attach(tempo, 5, 6, 9, 10)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 9)
        self.table.attach(tempo, 5, 6, 10, 11)
        OnLine_menu.append(tempo)        
        tempo = TextEntry( self.read_online, 6)
        self.table.attach(tempo, 5, 6, 11, 12)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 7)
        self.table.attach(tempo, 5, 6, 12, 13)
        OnLine_menu.append(tempo)
        tempo = TextEntry( self.read_online, 5)
        self.table.attach(tempo, 5, 6, 13, 14)
        OnLine_menu.append(tempo)
        
        # (7) EVENT-IMAGE: IAF Online selection
        ## -- online radio button
        option2, label = Radio_Button(option1, ' ONLINE BCI SYSTEM', large_font, lblue)
        RadioLabel.append(label)
        option2.connect("toggled", self.OnLine, OnLine_menu, RadioLabel)
        self.table.attach(option2, 3, 5, 2, 4)
        ## -- online image
        icon = Image('Images\\online.png') 
        icon.set_alignment(xalign = 0.75, yalign = 0.5)
        self.table.attach(icon, 4, 5, 2, 4)
        ## -- IAF eventbox
        IAF, img_IAF = Event_Image('Images\\IAF.png', 1, 0.5, tab_bg)
        IAF.connect("button_press_event", self.AlphaPeak)
        self.table.attach(IAF, 5, 6, 2, 4)
        OnLine_menu.append(IAF)

        # (8) BUTTONS: tools to load a matrix
        browse, label = Button_Label('LOAD', blue, font)
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
        label.modify_font(pango.FontDescription('Neuropol 14'))
        self.table.attach(browse, 2, 3, 4, 5)
        browse.connect('clicked', self.Load, OffLine_menu)
      
        self.table.show()
        
        # (9) Preset Interface
        OffLine_menu.append(browse)
        ## -- OffLine is "ON"
        for item in OnLine_menu: item.hide()
        ## -- OnLine is "OFF"
        for item in OffLine_menu: item.show()


    #..........Method 2: Returning widgets container........

    def container(self):
        'DAQ table for being appended to the notebook'
        return self.table


    #..........Method 3: OffLine Analysis sub-menu..........
    def OffLine(self, widget, OffLine_menu, RadioLabel):
        'OffLine Analysis Menu'

        if widget.get_active():
        # (1) Visible tools for submenu
            for item in OffLine_menu: item.show()
            self.daq_output[0] = 'offline'
            self.daq_output[1] = []
            #RadioLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
        # (2) Unvisible tools for submenu
            for item in OffLine_menu: item.hide()
            for item in OffLine_menu[11:-1]: item.set_text('')
            for item in self.daq_output[2:]: item = ''
            RadioLabel[0].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))
            self.daq_output[1] = []
            OffLine_menu[0].set_text('')
            OffLine_menu[1].set_text('')
            self.mnum = 0

     
    #...........Method 4: OnLine Analysis sub-menu..........
    def OnLine(self, widget, OnLine_menu, RadioLabel):
        'OnLine Analysis Menu'
        
        if widget.get_active():
        # (1) Visible tools for submenu
            for item in OnLine_menu: item.show()
            self.daq_output[0] = 'online'
            #RadioLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
        else:
        # (2) Unvisible tools for submenu
            for item in OnLine_menu: item.hide() 
            for item in OnLine_menu[10:-1]: item.set_text('')
            for item in self.daq_output[1:-1]: item = ''
            RadioLabel[1].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(lblue))

    #............Method 5: 'Load' Button pressing...........
    def Load(self, widget, OffLine_menu):
        'Searching matrixes to upload for processing'

        # (1) FileSelection
        self.FileSel = gtk.FileSelection('List of Numerical Arrays Selection')
        self.FileSel.connect('destroy_event', self.destroy_FileSel, OffLine_menu)
        self.FileSel.ok_button.connect('clicked', self.file_ok_sel, OffLine_menu)
        self.FileSel.cancel_button.connect('clicked', lambda w: self.FileSel.destroy())
        self.FileSel.show()


    #.........Method 6: OK button of 'Load' Button..........
    def file_ok_sel(self, widget, OffLine_menu):
        'A copy of the url selected matrix file'

        url = self.FileSel.get_filename()
        # (1) decoding the filename for display
        tempo = url.split('\0')
        tempo = tempo[0].split('\\')
        tempo = tempo[-1]
        # (2) checking if the file has mat extension
        ext = tempo.split('.')
        ext[0] = tempo
        if ext[1] == 'mat':            
            while len(ext[0]) > 13: ext[0] = ext[0][:-1]
            self.mnum += 1
            TexT = str(self.mnum) + '.- ' + ext[0]            
            OffLine_menu[0].set_text(TexT)
            self.FileSel.cancel_button.emit('clicked')
        # (3) selected matrix as the first output
            tempo = sp.io.loadmat(url)
            keys = tempo.keys()
            keys.sort()
            for key in keys:
                if key.find('_') == -1:
                    self.daq_output[1].append(tempo[key])
            # -- mental state label update & matrix dimension label update
            label = str(np.shape(self.daq_output[1][-1]))
            OffLine_menu[1].set_text(label)
        else:
            dialog = gtk.Dialog('File Extension Error!',None,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,("OK", True))
            message = Label('The file extension must be .mat', small_font, 'black', 0, 0)
            dialog.vbox.pack_start(message)
            dialog.show_all()
            result = dialog.run()
            if result: dialog.destroy()
            dialog.destroy()  
            

    #.......Method 7: CANCEL button of 'Load' Button .......
    def destroy_FileSel(self, widget, event, OffLine_menu):
        'Closure of FileSelection window'

        # (1) daq_out resetting
        self.daq_output = ['offline', [], '', 'off', '', '', '', '', '', '', '']
        # (2) cleanning of the filename
        OffLine_menu[0].set_text('')
        OffLine_menu[1].set_text('')
        self.mnum = 0
        # (3) closing window
        gtk.main_quit()


    #.......Method 8: Reading from a text entry box ........
    def read_offline(self, widget, location):
        'Data Extraction from Text-Entries Boxes (OffLine_menu)'

        new_text = widget.get_text()
        if widget.get_text() != '':
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information check-up and extraction
            ## -- only range selection option --> electrodes (default, external & bad)
            locA = [location == 2, location == 3, location == 10]
            locB = [location == 4, location == 5, location == 6]
            if any(locA):
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':']
                if any(allow):
                    self.daq_output[location] = widget.get_text()                    
                else:
                    MESSAGE = 'Only the following characters are allowed in Range Selection:\
                               \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> space'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- only combined range selection option --> trials and samples
            elif any(locB):
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':',new_text==';']
                if any(allow):
                    self.daq_output[location] = widget.get_text()                    
                else:
                    MESSAGE = 'Only the following characters are allowed in Combined Range Selection:\
                               \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> semicolon (;)\n-> space'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''                                    
            ## -- only integer options --> sample rate
            elif location == 7:
                if new_text.isdigit():
                    self.daq_output[location] = widget.get_text()
                else:
                    MESSAGE = 'Sample Rate Information must be an INTEGER'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- only float options --> time window
            elif location == 8:
                allow = [new_text.isdigit(),new_text=='.',new_text==';']
                if any(allow):
                    self.daq_output[location] = widget.get_text()
                else:
                    MESSAGE = 'Time Window Information must be a FLOAT'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- only integer options --> overlap rate
            elif location == 9:
                if new_text.isdigit():
                    self.daq_output[location] = widget.get_text()
                else:
                    MESSAGE = 'Overlap Rate Information must be an INTEGER'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''

                    
    #.......Method 9: Reading from a text entry box ........
    def read_online(self, widget, location):
        'Data Extraction from Text-Entries Boxes (OnLine_menu)'

        new_text = widget.get_text()
        if widget.get_text() != '':
            new_text = list(widget.get_text())
            new_text = new_text.pop(len(new_text)-1)
            # (1) Information check-up and extraction
            locA = [location == 3, location == 4]  
            locB = [location == 6, location == 7]          
            locC = [location == 8, location == 9]
            ## -- only integer options --> TCP array
            if location == 2:
                if new_text.isdigit():
                    self.daq_output[location] = widget.get_text()
                else:
                    MESSAGE = 'TCP Information must be an INTEGER'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- only range selection option --> channels
            elif any(locA):
                allow = [new_text.isdigit(),new_text.isspace(),new_text==',',new_text==':']
                if any(allow):
                    self.daq_output[location] = widget.get_text()                    
                else:
                    MESSAGE = 'Only the following characters are allowed in Range Selection:\
                               \n-> digits (0-9)\n-> comma (,)\n-> colon (:)\n-> space'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- only integer options --> sample rate
            elif location == 5:
                if new_text.isdigit():
                    self.daq_output[location] = widget.get_text()
                else:
                    MESSAGE = 'Sample Rate Information must be an INTEGER'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- only float option --> time window & overlap rate
            elif any(locB):
                allow = [new_text.isdigit(),new_text=='.']
                if any(allow):
                    self.daq_output[location] = widget.get_text()                    
                else:
                    MESSAGE = 'Time information must be a FLOAT or an INTEGER'
                    DialogBox (MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''    
            ## -- only integer options --> number of samples for controlling and referencing
            elif any(locC):  
                if new_text.isdigit():
                    self.daq_output[location] = widget.get_text()                    
                else:
                    MESSAGE = 'Sammple Information must be an INTEGER'
                    DialogBox(MESSAGE, 'Typing Error!')
                    widget.set_text('')
                    self.daq_output[location] = ''
            ## -- none        
            else:
                self.daq_output[location] = widget.get_text()
            


    #.....Method 10: Final acquisition from DAQ menu........
    def outcomes(self):
        'DAQ_menu final results'
        
        return self.daq_output
    
    
    #.........Method 11: Individual Alpha Frequency.........
    def AlphaPeak(self, widget, event):
        'Method to calculate the individual alpha frequency'
        
        # ==================================================
        # Data Acquisition
        # ==================================================
        print '\n\n***** INDIVIDUAL ALPHA FREQUENCY (IAF) *****'
        # ***** Data Storage *****
        EEG_EPOCHS = []
        device     = audiere.open_device()
        start      = device.open_file('Sounds\\iaf_start.wav')
        stop       = device.open_file('Sounds\\iaf_stop.wav')
        # ***** Recording EC&EO Condition *****
        for msg in ['Start recording the eyes close condition?', 'Start recording the eyes open condition?']:
            DialogBox(msg, 'Individual Alpha Frequency')   
            start.play()
            # (a) Local Variables Declaration
            TCP_ch, TCP_array, time_record, Fs = 72, 432, 180, 128
            current_samples, data, TCP_samples, daq_samples = 0, '', TCP_array//TCP_ch//3, time_record*Fs 
            eeg_epoch = np.zeros((TCP_ch, 1))             
            # (b) BioSemi TCP Communication Start
            Client_T11 = socket(AF_INET, SOCK_STREAM)
            Client_T11.connect(('localhost', 778))
            # ...........Data Acquisition per epoch.............
            while current_samples < daq_samples:        
            # (c) Default Variables into the Loop
                tempo = np.zeros((TCP_ch, TCP_samples))            
            # (d) Sample Collection per TCP_array
                # --- loop to ensure a complete TCP_array collection
                while len(data) < TCP_array: data += Client_T11.recv(TCP_array)
                # --- saving data till to get the require length (i.e., daq_samples)
                BYTES = data[:TCP_array]
                data =  data[TCP_array:]
            # (e) Conversion from 24bits to Voltage 
                BYTES = bits_float(BYTES)                
                # --- Converting in microvolts
                BYTES = BYTES * 31.25e-3
            # (f) Data Re-Organization into Channels               
                new_ch_idx = 0
                for ch in range(TCP_ch): tempo[new_ch_idx, :], new_ch_idx = BYTES[ch::TCP_ch], new_ch_idx+1
                eeg_epoch = np.append(eeg_epoch, tempo, axis = 1)
                current_samples += TCP_samples
            # (g) delete the first column of eeg_epoch created by default         
            eeg_epoch = np.delete(eeg_epoch, 0, axis = 1)
            print '==> Raw_Data: ', np.shape(eeg_epoch)
            EEG_EPOCHS.append(eeg_epoch)
            # (h) BioSemi TCP client closure
            Client_T11.close()
            stop.play()
        # (i) Data storage
        cPickle.dump(EEG_EPOCHS, open(root + 'IAF.p', 'wb'))       
        # ==================================================
        # Signal Conditioning
        # ==================================================    
        EEG_DSP = []
        for eeg_epoch in EEG_EPOCHS:   
            # (a) Variable Declaration
            sigcon_samples = 128 * 180
            eeg_tempo = np.zeros((64, daq_samples))
            eeg_dsp = np.zeros((64, sigcon_samples))     
            ref, BW, bandrej, DC = ['LargeLaplacian',[]], ['on',[0,0], [0,0]], ['off',(0,0)], ['off',(0,0)]   
            ## -- filter design
            BW[1][0], BW[1][1] = spectral_filter(128, 7,  0, 4, 'highpass')   
            BW[2][0], BW[2][1] = spectral_filter(128, 0, 14, 7, 'lowpass')
            # (b) Spectral Filtering
            for ch in range(64):eeg_tempo[ch,:] = SiGCoN(ch,eeg_epoch,layout,ref,BW,bandrej,DC,1,'spectral',[])
            # (c) Spatial Filtering + Downsampling
            for ch in range(64):  eeg_dsp[ch,:] = SiGCoN(ch,eeg_tempo,layout,ref,BW,bandrej,DC,1,'spatial', [])
            # (d) Data storage
            EEG_DSP.append(eeg_dsp)    
            print '==> Conditioned_Data: ', np.shape(eeg_dsp)
        # ==================================================
        # Power Spectral Density
        # ==================================================          
        FIG = plt.figure(num = 1, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')
        FIG.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.05, top = 0.925, hspace = 0.3)
        # (a) Eyes Closed (EC) Condition
        ## -- axis 1 configuration
        ax1 = FIG.add_subplot(3, 1, 1)
        ax1.tick_params(labelsize = 9) 
        ax1.grid(True)
        ax1.set_xlabel('F r e q u e n c y [Hz]', fontsize = 10, fontname='Byington')
        ax1.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 10, fontname='Byington')
        ax1.set_title('EYES CLOSE CONDITION', color = 'black', fontsize = 11, fontname='Byington')
        ## -- plot of EC condition
        signal = np.mean(EEG_DSP[0], axis = 0)
        print '==> ECspectrum_Data: ', np.shape(signal)
        Pxx1, freqs1 = ax1.psd(signal, NFFT=512, Fs=128, noverlap=50, color=blue, linewidth=1.75)
        ## -- maximum values
        max_values = np.max(Pxx1)
        max_idxs   = np.where(Pxx1 == max_values)[0]
        for idxs in max_idxs: ax1.text(freqs1[idxs],10*np.log10(Pxx1[idxs]),str(freqs1[idxs]),color=blue,fontsize=11,fontname='Byington')
        # (b) Eyes Open (EO) Condition
        ## -- axis 2 configuration
        ax2 = FIG.add_subplot(3, 1, 2)
        ax2.tick_params(labelsize = 9) 
        ax2.grid(True)
        ax2.set_xlabel('F r e q u e n c y [Hz]', fontsize = 10, fontname='Byington')
        ax2.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 10, fontname='Byington')
        ax2.set_title('EYES OPEN CONDITION', color = 'black', fontsize = 11, fontname='Byington')
        ## -- plot of EO condition
        signal = np.mean(EEG_DSP[-1], axis = 0)
        print '==> EOspectrum_Data: ', np.shape(signal)
        Pxx2, freqs2 = ax2.psd(signal, NFFT=512, Fs=128, noverlap=50, color=orange, linewidth=1.75)
        ## -- maximum values
        max_values = np.max(Pxx2)
        max_idxs   = np.where(Pxx2 == max_values)[0]
        for idxs in max_idxs: ax2.text(freqs2[idxs],10*np.log10(Pxx2[idxs]),str(freqs2[idxs]),color=orange,fontsize=11,fontname='Byington')
        # (c) Comparison between EC and EO Conditions
        ## -- axis 3 configuration
        ax3 = FIG.add_subplot(3, 1, 3)
        ax3.tick_params(labelsize = 9) 
        ax3.grid(True)
        ax3.set_xlabel('F r e q u e n c y [Hz]', fontsize = 10, fontname='Byington')
        ax3.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 10, fontname='Byington')
        ax3.set_title('DIFFERENCE BETWEEN EC & EO CONDITIONS', color = 'black', fontsize = 11, fontname='Byington')
        ## -- plot of ECvsEO condition
        signal = 10*np.log10(Pxx1) - 10*np.log10(Pxx2)
        print '==> ECvsEOspectrum_Data: ', np.shape(signal)
        ax3.plot(freqs1, signal, color = '#AD0066', linewidth = 1.75)
        ## -- maximum values
        max_values = np.max(signal)
        max_idxs   = np.where(signal == max_values)[0]
        for idxs in max_idxs: ax3.text(freqs1[idxs],signal[idxs],str(freqs1[idxs]),color='#AD0066',fontsize=11,fontname='Byington')
        ## -- display & storage
        url = root + 'IAF.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white')
        plt.show()
        print '********************************************\n'
        
        
           


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
