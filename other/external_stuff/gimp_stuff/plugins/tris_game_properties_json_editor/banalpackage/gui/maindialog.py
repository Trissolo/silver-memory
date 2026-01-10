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
from ..modules.datagrabber import DataGrabber
from .singlechooser import SingleChooser
from .versatilebox import VersatileBox
from .multichooser import MultiChooser

class MainDialog(GimpUi.Dialog, DataGrabber):
    def __new__(cls):
        print("Creating MainDialog")
        gag = super(MainDialog, cls).__new__(cls)
        return gag
    def __init__(self, *args):
        super().__init__(*args)
        self.set_title("Tris JSON generator")
        self.set_name("az")
        self.add_button("_Done (Close)", Gtk.ResponseType.CANCEL)
        self.connect("destroy", self._on_destroy)
        self.initialize_internal_stuff()
        #MAINBAR:
        self.get_content_area().pack_start(VersatileBox().make_main_bar(), True, True, 0)
        #TESTING Multi:
        m = MultiChooser(self.raw_vars, self.ntr_vars_kinds)
        self.get_content_area().pack_start(m, True, True, 2)
        #Building GUI:
        self.get_content_area().pack_start(VersatileBox().make_kind_selector(self.ntr_depth), False, False, 2)
        #self.get_content_area().pack_start(SingleChooser(["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei"]), True, True, 2)
        self.get_content_area().pack_start(SingleChooser(self.raw_hovernames), True, True, 2)
        # Test:
        check = self.get_content_area()
        #Gtk.Orientation.HORIZONTAL: 0
        #Gtk.Orientation.VERTICAL: 1
        #check.set_valign(Gtk.Align.FILL)
        print(f"ORIENTATION: {check.get_orientation()}\n get_spacing: {check.get_spacing()}")
        print(f"get_vexpand: {check.get_vexpand()}\nget_hexpand: {check.get_hexpand()}")
    def _on_destroy(self, widget):
        #a.conf_a("Fare the well!")
        print(f"ON DESTROY CALLED! TEST:{self is widget}\n:)" )
    def greet(self):
        print(f"Hi from {self.get_name()} 😎!")
