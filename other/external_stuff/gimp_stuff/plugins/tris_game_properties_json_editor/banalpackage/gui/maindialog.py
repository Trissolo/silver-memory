import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

'''
class MainDialog():
    def __init__(self):
        print("This is the Main Dialog!")

class Altr():
    def conf_a(self, param= "Param di A"):
        print(f"Setting param for Altr Class: {param}")
        self.param = param
'''
from .singlechooser import SingleChooser

class MainDialog(GimpUi.Dialog):
    def __new__(cls):
        print("Creating MainDialog")
        gag = super(MainDialog, cls).__new__(cls)
        return gag
    def __init__(self, *args):
        super().__init__(*args)
        self.add_button("_Done (Close)", Gtk.ResponseType.CANCEL)
        self.connect("destroy", self._on_destroy)
        self.get_content_area().pack_start(SingleChooser(["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei"]), True, True, 2)
        # Test:
        check = self.get_content_area()
        #Gtk.Orientation.HORIZONTAL: 0
        #Gtk.Orientation.VERTICAL: 1
        #check.set_valign(Gtk.Align.FILL)
        print(f"ORIENTATION: {check.get_orientation()}\n get_spacing: {check.get_spacing()}")
        print(f"get_vexpand: {check.get_vexpand()}\nget_hexpand: {check.get_hexpand()}")
        #self.conf_a("qghjqwgqhgwqjhwgqhwgqwhjqgwhqjwgqhjgwqhwgqjwgqhj")
    def _on_destroy(self, widget):
        #a.conf_a("Fare the well!")
        print(f"ON DESTROY CALLED! TEST:{self is widget}\n:)" )
