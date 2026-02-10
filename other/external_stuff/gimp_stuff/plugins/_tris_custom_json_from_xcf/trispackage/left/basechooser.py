import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

'''
class BaseChooser:
    def set_array(self, source_array):
        self.source_array = source_array
        
    def pseudo_init(self, source_array):
        self.source_array = source_array
        self.lettererichieste = "e"
        self.user_selected = None
        
        '''
'''
                ┌─...
                ├─GtkListBoxRow
                ├─GtkListBoxRow
                ├─GtkListBoxRow
                ├─GtkListBoxRow
                ├─GtkListBoxRow
            ┌─GtkListBox
            ┌─(GtkViewport)
        ┌─GtkScrolledWindow
        ├─GtkSearchEntry
        GtkBox
        '''
'''

        div = self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        search_widget = Gtk.SearchEntry()
        scrolled = Gtk.ScrolledWindow.new(None, None)
        listbox = self.listbox = Gtk.ListBox.new()
        
        scrolled.add(listbox)
        div.pack_start(search_widget, False, False, 1)
        div.pack_end(scrolled, True, True, 1)
        
        self._populate_listbox(source_array, listbox)
        search_widget.connect("search-changed", self.on_search_activated)
        div.show()
    
    def _populate_listbox(self, ary, listbox):
        for idx, item in enumerate(ary):
            element = Gtk.ListBoxRow.new()
            #element.data = item
            element.idx = idx
            element.add(Gtk.Label.new(f"{item} ({idx})"))
            listbox.add(element)
            listbox.set_sort_func(self.sort_func, None, False)
            listbox.set_filter_func(self.tris_filter_func, False)
            #listbox.connect("row-activated", self.on_row_activated_grid, self)
   
    def build_lb(self, ary):
        listbox = self.listbox = Gtk.ListBox()
        scrolled = self.scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        # populate the ListBox
        self._populate_listbox(ary, listbox)
        
    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        self.listbox.invalidate_filter()
    
    def sort_func(self, row_1, row_2, data, notify_destroy):
        #print("Sort_Func", row_1, row_2, self.source_array[row_1.idx],self.source_array[row_2.idx],  sep="\n")
        return self.source_array[row_1.idx].lower() > self.source_array[row_2.idx].lower()
        #return row_1.data.lower() > row_2.data.lower()
            
    def tris_filter_func(self, row, notify_destroy):
        #print(f"tris_filter_func <--------- ORCUS row text: {row.get_children()[0].get_text()}", self.lettererichieste, row.idx, notify_destroy, self.source_array[row.idx])
        return True if self.lettererichieste.lower() in self.source_array[row.idx].lower() else False
'''    

class SimpleChooser:
    def pseudo_init(self, source_array, kind = None):
        self.lettererichieste = ""
        div = self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
        search_widget = Gtk.SearchEntry()
        scrolled = Gtk.ScrolledWindow.new(None, None)
        listbox = self.listbox = Gtk.ListBox.new()
        
        scrolled.add(listbox)
        div.pack_start(search_widget, False, False, 1)
        div.pack_end(scrolled, True, True, 1)
        
        self._populate_listbox(source_array, listbox)
        search_widget.connect("search-changed", self.on_search_activated)
        div.show()
    
    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        self.listbox.invalidate_filter()
    
    def tris_filter_func(self, row, notify_destroy):
        print("Filter", row.get_children()[0].get_text())
        return True if self.lettererichieste.lower() in row.get_children()[0].get_text().lower() else False
    
    def _populate_listbox(self, ary, listbox):
        for idx, item in enumerate(ary):
            element = Gtk.ListBoxRow.new()
            element.idx = idx
            element.add(Gtk.Label.new(f"{item} ({idx})"))
            listbox.add(element)
            listbox.set_sort_func(self.sort_func, None, False)
            listbox.set_filter_func(self.tris_filter_func, False)
    
    def sort_func(self, row_1, row_2, data, notify_destroy):
        return row_1.get_children()[0].get_text().lower() > row_2.get_children()[0].get_text().lower()
    def test_row_chicked(self, listbox, row):
        print(f"Clicked: {row.idx}")
        return row.idx
    def hide(self):
        self.div.hide()
    def set_name(self, name = "No name"):
        self.name = name

