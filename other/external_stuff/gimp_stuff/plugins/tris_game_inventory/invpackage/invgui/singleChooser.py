import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class SingleChooser(Gtk.Box):
    def __init__(self, source, var_kind = None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.source = source
        self.connect('destroy', self.destroy_source_ary)
        self.lettererichieste = ""
        search_widget = Gtk.SearchEntry()
        scrolled = Gtk.ScrolledWindow.new(None, None)
        listbox = Gtk.ListBox.new()
        listbox.set_valign(Gtk.Align.FILL)
        if type(var_kind) is int:
            listbox.var_kind = var_kind
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
        return True if self.lettererichieste.lower() in row.get_child().get_text().lower() else False
    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        self.get_salient_widget().invalidate_filter()
    def get_listbox(self):
        return self.get_children()[1].get_child().get_child()
    def get_salient_widget(self):
        return self.get_listbox()
    def get_readable(self, arr, fakeparam=None):
        print("SINGLE", arr)
        return f"{self.source[arr[0]]}"
    def destroy_source_ary(self, widget):
        print("destroy_source_ary!")
        self.source = self.source.clear()
