import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class DictChooser(Gtk.Box):
    def __init__(self, isMonoChooser=False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        tempnames = None
        if isMonoChooser:
            self.set_name("MonoChooser")
            self.source = {1: "<- is set"}
            tempnames = {1: "Add prop."}
        else:
            self.set_name("kindselectorbox")
            self.source = tempnames = self.kind_dictionary()
        for key, value in tempnames.items():
            button = Gtk.Button.new_with_label(f"{value} ({key})")
            button.key = key
            button.set_halign(1)
            button.set_valign(1)
            self.pack_start(button, True, True, 2)
        self.show_all()
        self.connect("destroy", self.on_kind_chooser_destroy)
    def get_readable(self, ary, size = None):
        return f"{self.source.get(ary[0])}"
    def get_salient_widgets(self):
        return (button for button in self.get_children())
    @staticmethod
    def kind_dictionary():
        kind_dictionary = {
            -6: 'Hoverable',
            -5: 'Background',
            0: 'Ridiculously Faraway',
            1: 'Trigger Area',
            2: 'Covered',
            3: 'Always Back',
            4: 'Depth Sorted Bottom (0.5, 1)',
            5: 'Depth Sorted Center (0.5, 0.5)',
            800: 'Foreground'
            }
        return kind_dictionary
    def on_kind_chooser_destroy(self, widget):
        self.source = self.source.clear()