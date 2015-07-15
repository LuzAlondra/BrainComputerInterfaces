### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### February 1st, 2010

# ****************************
# * Graphical User Interface:*
# *   'WIDGET CONSTRUCTORS'  *
# ****************************

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
import pygtk
pygtk.require('2.0')
import gtk
import pango
import copy

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATIONS

# .............Function 1: Image constructor................
def Image(IMAGE):
    # 1) Image creation
    image = gtk.Image()
    image.set_from_file(IMAGE)
    image.show()
    return image

# .............Function 2: Label constructor................
def Label(LABEL, FONT, COLOR, XALIGN, YALIGN, JUSTIFICATION):
    # 1) Label creation
    label = gtk.Label()
    label.set_text(LABEL)
    label.show()
    # 2) Label format
    label.modify_font(pango.FontDescription(FONT))
    label.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(COLOR))
    label.set_alignment(xalign = XALIGN, yalign = YALIGN)
    label.set_justify(JUSTIFICATION)    
    return label

# .............Function 3: Frame constructor................
def Frame(LABEL,COLOR):
    # 1) Frame creation
    frame = gtk.Frame()
    frame.set_label(LABEL)
    frame.show()
    # 2) Frame background
    STYLE = frame.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= frame.get_colormap().alloc_color(COLOR)
    frame.set_style(STYLE)
    return frame

# ........Function 4: Button - Label constructor............
def Button_Label(LABEL, COLOR_button, COLOR_label, FONT):
    # 1) Button creation
    button = gtk.Button(LABEL)
    button.show()
    # 2) Button background 
    STYLE = button.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= button.get_colormap().alloc_color(COLOR_button)
    button.set_style(STYLE)
    # 3) Button label font
    if button.get_use_stock():
        label = button.child.get_children()[1]
    elif isinstance(button.child, gtk.Label):
        label = button.child
    else:
        raise ValueError("button does not have a label")
    label.modify_font(pango.FontDescription(FONT))
    label.set_justify(gtk.JUSTIFY_CENTER)
    label.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(COLOR_label))
    return (button, label)

# ...........Function 5: Button - Image constructor.........
def Button_Image(IMAGE, COLOR):
    # 1) Button creation
    button = gtk.Button()
    # 2) Image insertion
    image = gtk.Image()
    image.set_from_file(IMAGE)
    button.add(image)
    image.show()
    button.show()
    # 3) Button background
    STYLE = button.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= button.get_colormap().alloc_color(COLOR)
    button.set_style(STYLE)
    return (button, image)

# ...........Function 6: Event - Image constructor..........
def Event_Image(IMAGE,COLOR):
    # 1) Event creation
    eventbox = gtk.EventBox()
    # 2) Image insertion
    image = gtk.Image()
    image.set_from_file(IMAGE)
    eventbox.add(image)
    image.show()
    eventbox.show()
    # 3) Event background
    STYLE = eventbox.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= eventbox.get_colormap().alloc_color(COLOR)
    eventbox.set_style(STYLE)
    return (eventbox, image)

# ...........Function 7: Event - Label constructor............
def Event_Label(LABEL, FONT, COLOR_font, COLOR_event):
    # 1) Event creation
    eventbox = gtk.EventBox()
    eventbox.show()
    # 2) Label creation
    label = gtk.Label()
    label.set_text(LABEL)
    label.set_justify(gtk.JUSTIFY_CENTER)
    label.modify_fg(gtk.STATE_NORMAL,gtk.gdk.color_parse(COLOR_font))
    label.show()
    # 3) Label font
    label.modify_font(pango.FontDescription(FONT))
    # 4) Event background
    STYLE = eventbox.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= eventbox.get_colormap().alloc_color(COLOR_event)
    eventbox.set_style(STYLE)
    eventbox.add(label)
    return (eventbox, label)


# ...........Function 8: Frame - Image constructor..........
def Frame_Image(IMAGE,COLOR,STYLE):
    # 1) Frame creation
    frame = gtk.Frame()
    # 2) Image insertion
    image = gtk.Image()
    image.set_from_file(IMAGE)
    frame.add(image)
    image.show()
    frame.show()
    # 3) Frame background
    frame.set_shadow_type(STYLE)
    style = frame.get_style().copy()
    style.bg[gtk.STATE_NORMAL]= frame.get_colormap().alloc_color(COLOR)
    frame.set_style(style)
    return (frame, image)


# .........Function 9: Frame - Label constructor............
def Frame_Label(LABEL, COLOR_frame, COLOR_font, FONT, XALIGN, YALIGN, JUSTIFICATION):
    # 1) Frame creation
    frame = gtk.Frame()    
    frame.show()
    # 2) Frame background 
    STYLE = frame.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= frame.get_colormap().alloc_color(COLOR_frame)
    frame.set_style(STYLE)   
    # 3) Label creation
    label = Label(LABEL, FONT, COLOR_font, XALIGN, YALIGN, JUSTIFICATION)    
    # 4) Adding the Label as a Title of the Frame
    frame.set_label_widget(label)
    frame.set_label_align(XALIGN, YALIGN)
    return (frame, label)


# ......... Function 10: Scrolled-Window ~ TextView ........
def Window_TextView(medium_font, blue):
    ## --scrolled window
    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
    ## --textview and buffer
    textview = gtk.TextView()
    textbuffer = textview.get_buffer()
    textview.set_editable(False)
    textview.set_cursor_visible(False)
    textview.set_justification(gtk.JUSTIFY_LEFT)
    textview.set_left_margin(7)
    ## --active text
    tagB = textbuffer.create_tag()
    tagB.set_property("font", medium_font)
    tagB.set_property("foreground", "black")
    ## --non~active text
    tagG = textbuffer.create_tag()
    tagG.set_property("font", medium_font)
    tagG.set_property("foreground", "gray")
    ## --frame 
    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
    STYLE = frame.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL]= frame.get_colormap().alloc_color(blue)
    frame.set_style(STYLE)        
    ## --widgets attachment
    scrolled_window.add(textview)
    frame.add(scrolled_window)
    ## --widget display
    frame.show()
    scrolled_window.show()
    textview.show()
    return frame, textview, textbuffer, tagB, tagG
    
    