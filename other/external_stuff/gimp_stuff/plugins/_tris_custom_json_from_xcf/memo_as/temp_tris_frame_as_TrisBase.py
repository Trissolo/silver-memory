import gi
gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrisLabel(Gtk.Label):
    def __init__(self, text = "My TrisLabel"):
        super().__init__()
        self.set_use_markup(True)
        self.set_default_style()
        self.set_name("La TrisLABEL (my extended Gtk.Label -> the click-enabled Widget)")
        #self.raw_text_entered = ""
        
        # temporary use. Remember to delete the following line
        # ...or maybe leave it
        self.write_default(text)
        self.show()
    
    def write_default(self, text, list_params = None):
        self.raw_text_entered = text
        if list_params is None:
            list_params = self.default_style_params
        self.set_markup(type(self).assemble_span(text, *list_params))
        print('raw_text_entered :', self.raw_text_entered, self.raw_text_entered == self.get_text())
        return self
    
    @staticmethod
    def assemble_span(text, color = None, bgcolor = None, size = 100, padAmount = 0, monospace = False):
        color = f'color="#{str(hex(color)).removeprefix("0x").zfill(6)}"' if type(color) == int else ""
        bgcolor = f'bgcolor="#{str(hex(bgcolor)).removeprefix("0x").zfill(6)}"' if type(bgcolor) == int else ""
        size = f'size="{size}%"' if type(size) == int else ""
        pad = " " * padAmount
        return f"<span {color} {bgcolor} {size}>{pad}{text}{pad}</span>"
    
    def set_default_style(self, color = 0x202040, bgcolor = 0x2c2e53, size = 150, pad = 3, monospace = True):
            self.default_style_params = [color, bgcolor, size, pad, monospace]
            return self

class TrisBase(Gtk.Frame):
    def __init__(self):
        super().__init__()
        self.set_name("TrisBase (my Extended FRAME)")
        #immediatly set the content (the Gdk.Label was a placeholder)
        #self.add(Gtk.Label.new("Any content"))
        self.add(Gtk.Grid())
        
        content_grid = TrisLabel("Frame Custom-Label")
        
        eventbox = Gtk.EventBox()
        eventbox.set_name("a standard EventBox ;)")
        eventbox.connect("button-press-event", type(self).on_click_handler)
        eventbox.add(content_grid)
        eventbox.show()
        self.set_label_widget(eventbox)
    
    @staticmethod
    def on_click_handler(evtbox, evtbtn):
        trisFrame = evtbox.get_parent()
        print("The extended Gtk.Frame - now is called TrisBase:", trisFrame)
        clickable_frame_title = evtbox.get_child()
        print("clickable_frame_title:", clickable_frame_title)
        content = trisFrame.get_child()
        print("content -now a Gtk.Grid:", content)
        content.set_visible(not content.get_visible())


trisFrame = TrisBase()
dialogazzo = GimpUi.Dialog.new()
dialogazzo.get_content_area().pack_start(trisFrame, False, False, 11)
dialogazzo.show_all()


# maybe add on over event
'''
def on_pointer_over(evtbox, evtbtn):
    trisFrame = evtbox.get_parent()
    widgetTrisLabel = evtbox.get_child()
    content = trisFrame.get_child()
    widgetTrisLabel.write_default(widgetTrisLabel.raw_text_entered, [0, 0xdadada, 150, 4, True])

def on_pointer_out(evtbox, evtbtn):
    trisFrame = evtbox.get_parent()
    widgetTrisLabel = evtbox.get_child()
    content = trisFrame.get_child()
    widgetTrisLabel.write_default(widgetTrisLabel.raw_text_entered, [0xdadada, 0, 150, 4, True])

eventbox.connect("leave-notify-event", on_pointer_over)
eventbox.connect("enter-notify-event", on_pointer_out)
'''
