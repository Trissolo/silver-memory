import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class SingleChooser(Gtk.Box):
    def __new__(cls, b):
        #print(f"Creating instance {super(SingleChooser, cls)}")
        gag = super(SingleChooser, cls).__new__(cls)
        return gag
    def __init__(self, source):
        super().__init__(homogeneous=False, spacing=2)
        self.set_orientation(1)
        self.source = source
        self.lettererichieste = ""
        search_widget = Gtk.SearchEntry()
        scrolled = Gtk.ScrolledWindow.new(None, None)
        #scrolled.set_valign(Gtk.Align.FILL)
        #self.set_vexpand(True)
        #scrolled.set_valign(Gtk.Align.FILL)
        #print(f"SCROOOOOLLLED! Hexpand: {scrolled.get_hexpand()}, valign: {scrolled.get_valign()}") #Gtk.Align)}")
        listbox = Gtk.ListBox.new()
        listbox.set_valign(Gtk.Align.FILL)
        for idx, item in enumerate(source):
            element = Gtk.ListBoxRow.new()
            element.idx = idx
            element.add(Gtk.Label.new(f"{item} ({idx})"))
            listbox.add(element)
            listbox.set_sort_func(self.sort_func, None, False)
            listbox.set_filter_func(self.tris_filter_func, False)
        search_widget.connect("search-changed", self.on_search_activated)
        scrolled.add(listbox)
        self.pack_start(search_widget, False, False, 1)
        self.pack_end(scrolled, True, True, 1)
        self.show_all()
    def sort_func(self, row_1, row_2, data, notify_destroy):
        return row_1.get_child().get_text().lower() > row_2.get_child().get_text().lower()
    def tris_filter_func(self, row, notify_destroy):
        #print("Filter and ROW", row.get_children()[0].get_text(), type(row))
        return True if self.lettererichieste.lower() in row.get_child().get_text().lower() else False
    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        self.get_listbox().invalidate_filter()
    def get_listbox(self):
        return self.get_children()[1].get_child().get_child()
    def get_readable(self, arr, fakeparam=None):
        return f"{self.source[arr[0]]}"
        #return res
        