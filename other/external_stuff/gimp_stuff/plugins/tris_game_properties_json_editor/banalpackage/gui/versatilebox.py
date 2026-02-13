import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class VersatileBox(Gtk.Box):
    def __new__(cls):
        return super(VersatileBox, cls).__new__(cls)
    def __init__(self):
        super().__init__(homogeneous=False, spacing=2)
        #self.set_orientation(1)
    def make_kind_selector(self, dictionary):
        self.source = dictionary
        self.set_orientation(1)
        self.set_name("kindselectorbox")
        for key, value in dictionary.items():
            button = Gtk.Button.new_with_label(f"{value} ({key})")
            button.key = key
            button.set_halign(1)
            button.set_valign(1)
            self.pack_start(button, True, True, 2)
        self.show_all()
        self.connect("destroy", self.on_kind_selector_destroy)
        return self
    def gag(self, button):
        print(f"Selected {button.key} (Corresp: {self.source.get(button.key)})")
    def make_preview_bar(self):
        self.set_name("Preview Box")
        button_remove_existing_parasite = Gtk.Button.new_with_label("Remove Existing Parasite")
        button_remove_existing_parasite.set_name("remove_parasite")
        self.pack_start(button_remove_existing_parasite, False, False, 2)
        label = Gtk.Label.new(f"Parasite info")
        self.pack_start(label, True, False, 2)
        self.show_all()
        return self
    def get_readable(self, arr, fakeparam=None): 
        return f"{self.source[arr[0]]} ({arr[0]})"
    def on_kind_selector_destroy(self, other):
        self.source = None
        #print("🥚 Versatile kind_selector_destroy called")

#alternative
# class MyCustomBox(Gtk.Box):
#     def __init__(self):
#         # Initialize the parent Gtk.Box
#         # We set orientation to vertical and spacing to 10 pixels
#         super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
#         # Add a Label
#         self.label = Gtk.Label(label="This is a subclassed Box")
#         self.pack_start(self.label, True, True, 0)
        
#         # Add a Button
#         self.button = Gtk.Button(label="Click Me")
#         self.button.connect("clicked", self.on_button_clicked)
#         self.pack_start(self.button, True, True, 0)
#         self.show_all()
    
#     def on_button_clicked(self, widget):
#         print("Button inside the custom box was clicked!")
