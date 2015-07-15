### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### February 2nd, 2011

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
def Label(LABEL, FONT, COLOR, X, Y):
    # 1) Label creation
    label = gtk.Label()
    label.set_text(LABEL)
    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(COLOR))
    label.modify_font(pango.FontDescription(FONT))
    label.set_alignment(xalign=X, yalign=Y)
    label.show()    
    return label

# .............Function 3: Frame constructor................
def Frame(LABEL, COLOR):
    # 1) Frame creation
    frame = gtk.Frame()
    frame.set_label(LABEL)
    frame.show()
    # 2) Frame background
    STYLE = frame.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = frame.get_colormap().alloc_color(COLOR)
    frame.set_style(STYLE)
    return frame

# ........Function 4: Button - Label constructor............
def Button_Label(LABEL, COLOR, FONT):
    # 1) Button creation
    button = gtk.Button(LABEL)
    button.show()
    # 2) Button background 
    STYLE = button.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = button.get_colormap().alloc_color(COLOR)
    button.set_style(STYLE)
    # 3) Button label font
    if button.get_use_stock():
        label = button.child.get_children()[1]
    elif isinstance(button.child, gtk.Label):
        label = button.child
    else:
        raise ValueError("button does not have a label")
    label.modify_font(pango.FontDescription(FONT))
    return (button, label)

# .............Function 5: Radio Button constructor.........
def Radio_Button(GROUP, LABEL, FONT, COLOUR):
    # 1) Button creation
    radio_button = gtk.RadioButton(GROUP, LABEL)
    radio_button.show()
    # 2) Button label font
    if radio_button.get_use_stock():
        label = radio_button.child.get_children()[1]
    elif isinstance(radio_button.child, gtk.Label):
        label = radio_button.child
    else:
        raise ValueError("radio_button does not have a label")
    label.modify_font(pango.FontDescription(FONT))
    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(COLOUR))
    return radio_button, label

# .............Function 6: Text Entry constructor...........
def TextEntry(FUNCTION, LOCATION):
    # 1) Entry properties
    entry = gtk.Entry()
    entry.set_property('xalign', 0.5)
    entry.modify_font(pango.FontDescription('Tahoma 14'))
    entry.show()
    # 2) Entry signals connection
    entry.connect('changed', FUNCTION, LOCATION)
    return entry

# .............Function 7: Check Button constructor.........
def Check_Button(LABEL, FONT, COLOUR):
    # 1) Button creation
    check_button = gtk.CheckButton(LABEL)
    check_button.show()
    # 2) Button label font
    if check_button.get_use_stock():
        label = check_button.child.get_children()[1]
    elif isinstance(check_button.child, gtk.Label):
        label = check_button.child
    else:
        raise ValueError("check_button does not have a label")
    label.modify_font(pango.FontDescription(FONT))
    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(COLOUR))
    return check_button, label


# ........Function 9: Button - Label constructor............
def Toggle_Button(LABEL, COLOR, FONT):
    # 1) Button creation
    toggle_button = gtk.ToggleButton(LABEL)
    toggle_button.show()
    # 2) Button background 
    STYLE = toggle_button.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = toggle_button.get_colormap().alloc_color(COLOR)
    toggle_button.set_style(STYLE)
    # 3) Button label font
    if toggle_button.get_use_stock():
        label = toggle_button.child.get_children()[1]
    elif isinstance(toggle_button.child, gtk.Label):
        label = toggle_button.child
    else:
        raise ValueError("button does not have a label")
    label.modify_font(pango.FontDescription(FONT))
    return toggle_button


# .........Function 10: Event - Label constructor............
def Event_Label(LABEL, FONT, COLOR, X, Y, BACKGND):
    # 1) EventBox creation
    event_box = gtk.EventBox()
    event_box.show()
    # 2) EventBox
    STYLE = event_box.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = event_box.get_colormap().alloc_color(BACKGND)
    event_box.set_style(STYLE)
    # 3) Label creation
    label = gtk.Label()
    label.set_text(LABEL)
    label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(COLOR))
    label.modify_font(pango.FontDescription(FONT))
    label.set_alignment(xalign=X, yalign=Y)
    label.show()
    event_box.add(label)    
    return event_box, label


# .........Function 11: Event - Image constructor...........
def Event_Image(IMAGE, X, Y, BACKGND):
    # 1) Image creation
    image = gtk.Image()
    image.set_from_file(IMAGE)
    image.show()
    # 2) EventBox creation
    event_box = gtk.EventBox()
    event_box.show()
    # 3) EventBox
    STYLE = event_box.get_style().copy()
    STYLE.bg[gtk.STATE_NORMAL] = event_box.get_colormap().alloc_color(BACKGND)
    event_box.set_style(STYLE)
    # 4) Image format & attachment
    image.set_alignment(xalign = X, yalign = Y)
    event_box.add(image)    
    return event_box, image


