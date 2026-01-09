import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class VersatileBox(Gtk.Box):
    def __new__(cls):
        return super(VersatileBox, cls).__new__(cls)
    def __init__(self):
        super().__init__(homogeneous=False, spacing=2)
        #self.set_orientation(1)
    def make_kind_selector(self, dictionary):
        self.set_orientation(1)
        for key, value in dictionary.items():
            button = Gtk.Button.new_with_label(key)
            button.val = value
            button.set_halign(1)
            button.set_valign(1)
            #print("BUTTON HEXP", button.set_hexpand(True))
            self.pack_start(button, True, True, 2)
        self.show_all()
        #[print(elem.val) for elem in self.get_children()]
        return self