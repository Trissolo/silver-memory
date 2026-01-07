import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MultiChooser(Gtk.Box):
    def __new__(cls, b):
        return super(MultiChooser, cls).__new__(cls)
        # print(f"Creating instance {super(MultiChooser, cls)}")
        #return gag
    def __init__(self, myp):
        super().__init__(homogeneous=False, spacing=2)
        self.set_orientation(1)
        self.lettererichieste = ""