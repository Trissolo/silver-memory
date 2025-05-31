import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .LayerManager import LayerManager
from ..misc.MarkupLabel import MarkupLabel

class BaseWidget(LayerManager):       
    def make_left_gui(self, prop):
        self.div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        div.show()
        self.right_div = div
        self.div.pack_end(div, True, True, 0)

        div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        self.left_div = div
        div.show()
        self.div.pack_start(div, False, False, 0)

        for num in range(97, 99):
            label = MarkupLabel(prop if num == 97 else "----")
            #label.set_default_text()
            div.pack_start(label, False, False, 2)
            setattr(self, f"label_{chr(num)}", label)

        for num, name in enumerate([GimpUi.ICON_MENU_RIGHT, GimpUi.ICON_DIALOG_ERROR, GimpUi.ICON_GO_PREVIOUS], start=97):
            button = GimpUi.Button.new_from_icon_name(name, 1)
            button.show()
            div.pack_end(button, False, False, 2)
            setattr(self, f"button_{chr(num)}", button)
        #self.left_div = div
        self.div.show()
        
