import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .MarkupLabel import MarkupLabel

class LeftSummary():
    def __init__(self, property):
        self.div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        self.label_a = MarkupLabel(f"{property}: ")
        self.label_a.write(monospace=True)
        self.label_b = MarkupLabel("- - - -")
        self.div.pack_start(self.label_a, False, False, 0)
        self.div.pack_start(self.label_b, False, False, 0)
        #self.div.show_all()


        