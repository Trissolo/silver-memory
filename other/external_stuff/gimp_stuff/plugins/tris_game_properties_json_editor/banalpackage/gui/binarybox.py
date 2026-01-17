import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

#gi.require_version("GimpUi", "3.0")
#from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class BinaryBox(Gtk.Box):
    def __new__(cls):
        return super(BinaryBox, cls).__new__(cls)
    def __init__(self):
        super().__init__(homogeneous=False, spacing=2)
        #self.set_orientation(1)
        button = Gtk.Button.new_with_label("Set existence")
        button.set_halign(1)
        button.set_valign(1)
        button.key = 1
        #button.connect('clicked', self.gag)
        #print("BUTTON HEXP", button.set_hexpand(True))
        self.pack_start(button, False, False, 2)
        self.show_all()
    def get_readable(self, arr, fakeparam=None): 
        return "Exists" if arr[0] == 1 else "Not set"
    def get_default_button(self):
        return self.get_children()[0]