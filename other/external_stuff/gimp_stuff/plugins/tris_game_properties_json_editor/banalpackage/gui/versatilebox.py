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
            button = Gtk.Button.new_with_label(value)
            button.key = key
            button.set_halign(1)
            button.set_valign(1)
            #button.connect('clicked', self.gag)
            #print("BUTTON HEXP", button.set_hexpand(True))
            self.pack_start(button, True, True, 2)
        self.show_all()
        #[print(elem.val) for elem in self.get_children()]
        #print("​✔️​", self.get_readable([-5]))
        return self
    def make_main_bar(self):
        self.set_name("Mainbar Box")
        refresh_button = GimpUi.Button.new_from_icon_name(GimpUi.ICON_VIEW_REFRESH, 1)
        refresh_button.set_name("Btn_refresh_layer")
        #refresh_button.set_halign(1)
        #refresh_button.set_valign(1)
        #refresh_button.show()
        self.pack_start(refresh_button, False, False, 2)
        l = Gtk.Label.new(f"Layer name here")
        self.pack_start(l, True, True, 2)
        for a, b in zip((GimpUi.ICON_TOOL_CAGE, GimpUi.ICON_DOCUMENT_SAVE), ("Btn_extract_paths", "Btn_generate_json")):
            button = GimpUi.Button.new_from_icon_name(a, 1)
            button.set_name(b)
            self.pack_end(button, False, False, 2)
        #button_generate_json = GimpUi.Button.new_from_icon_name(GimpUi.ICON_DOCUMENT_SAVE, 1)
        #button_generate_json.set_name("Btn_generate_json")
        #GimpUi.ICON_TOOL_CAGE

        #button_generate_json.set_halign(1)
        #button_generate_json.set_valign(1)
        #self.pack_end(button_generate_json, False, False, 2)
        self.show_all()
        return self
    def gag(self, button):
        #print(*self.source.items())
        print(f"Selected {button.key} (Corresp: {self.source.get(button.key)})")
    def make_preview_bar(self):
        self.set_name("Preview Box")
        #refresh_button = GimpUi.Button.new_from_icon_name(GimpUi.ICON_VIEW_REFRESH, 1)
        #refresh_button.set_name("Btn_refresh_layer")
        #refresh_button.set_halign(1)
        #refresh_button.set_valign(1)
        #refresh_button.show()
        button_remove_existing_parasite = Gtk.Button.new_with_label("Remove Existing Parasite")
        button_remove_existing_parasite.set_name("remove_parasite")
        self.pack_start(button_remove_existing_parasite, False, False, 2)
        label = Gtk.Label.new(f"Parasite info")
        self.pack_start(label, True, False, 2)
        self.show_all()
        return self
    def get_readable(self, arr, fakeparam=None): 
        return f"{self.source[arr[0]]} ({arr[0]})"
    