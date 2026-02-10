import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .MarkupLabel import MarkupLabel

class MainBar:
    def __init__(self):
        self.div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.button_refresh = self.make_refresh_button()
        self.layer_name_label = MarkupLabel("No layer selected")

        self.div.pack_start(self.layer_name_label, False, False, 2)
    def write_layer_name(self, layer):
        self.layer_name_label.write(layer.get_name(), monospace=True, width=20, bgcolor=0x2378bd, align="^")

    def make_refresh_button(self):
        refresh_button = GimpUi.Button.new_from_icon_name(GimpUi.ICON_VIEW_REFRESH, 1)
        refresh_button.show()
        self.div.pack_start(refresh_button, False, False, 2)
        return refresh_button
    
    def refresh_button_action(self, onclick, *args):
        self.button_refresh.connect("clicked", onclick, *args)