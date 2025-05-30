import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ..trismodule.TrisEnum import TrisEnum
from ..trismodule.trisLabel import TrisLabel

class TrisChooserGrid():
    def __init__(self, trisParent, json_prop, json_list):
        self.trisParent = trisParent
        self.json_prop = json_prop
        # build a brand new Enum! (...and so, all the enums in 'trisParent' becomes superfluous )
        self.tris_enum = TrisEnum(json_list)
        self.lettererichieste = "e"
        #self.lbl_value.set_size_request(150, 110)
        #from here
        self.prop_key = TrisLabel(json_prop)
        self.prop_key.write_default(json_prop, [0xdedede, 0x565656, 150, 4, True])
        self.prop_value = TrisLabel("Prop-value")
        self.prop_human_readable_value = TrisLabel("Prop-human_readable")
        self.pseudobutton_delete_value = TrisLabel("Delete")
        self.pseudobutton_select_new_value = TrisLabel("New")
        hn_grid = Gtk.Grid.new()
        hn_grid.attach(self.prop_key, 0, 0, 2, 1)
        hn_grid.attach(self.prop_human_readable_value, 2, 0, 2, 1)
        hn_grid.attach(self.prop_value, 4, 0, 2, 1)
        hn_grid.attach(self.pseudobutton_delete_value, 5, 1, 1, 1)
        hn_grid.attach(self.pseudobutton_select_new_value, 5, 2, 1, 1)
        # to here
        # the Search field:
        searcWidget = Gtk.SearchEntry()
        searcWidget.show()
        searcWidget.connect("search-changed", self.on_search_activated, self)
        # the ListBox:
        listbox = Gtk.ListBox()
        # populate the ListBox
        for item in self.tris_enum.tlist:
            listbox_element = Gtk.ListBoxRow.new()
            listbox_element.data = item
            listbox_element.add(Gtk.Label(label = item))
            listbox.add(listbox_element)
        listbox.set_sort_func(self.sort_func, None, False)
        listbox.set_filter_func(self.tris_filter_func, self, False)
        listbox.connect("row-activated", self.on_row_activated_grid, self)
        listbox.set_hexpand(True)
        #set_hexpand(True)
        self.listbox = listbox
        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        hn_grid.attach(searcWidget, 6, 0, 2, 1)
        hn_grid.attach(scrolled, 6, 1, 2, 3)
        hn_grid.show_all()
        self.hn_grid = hn_grid
    def get_grid(self):
        return self.hn_grid
    @staticmethod
    def tb_ba_action(button, self):
        print("TrisChooser: Not yet implemented save parasite", self.tris_enum.get_all(2))
        print(self.current_layer.get_name(), "<--")
    @staticmethod
    def on_search_activated(searchentry, self):
        self.lettererichieste = searchentry.get_text()
        self.listbox.invalidate_filter()
    @staticmethod
    def sort_func(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    @staticmethod
    def tris_filter_func(row, self, notify_destroy):
        #print(data, "<--------- ORCUS")
        return True if self.lettererichieste.lower() in row.data.lower() else False
    @staticmethod
    def on_row_activated_grid(listbox_widget, row, self):
        print("Accesso inutile a trisLayer", self.current_layer.get_name())
        num, text = self.tris_enum.get_all(row.data)
        #self.lbl_value.set_text(f'{text} [{num}]')
        #self.prop_key.write_default()
        self.prop_value.write_default(num, [0x5566aa, 0xdada86, 200, 6, True])
        self.prop_human_readable_value.write_default(text)
    
    @property
    def current_layer(self):
        return self.trisParent.current_layer
    
    @staticmethod
    def toggle_btn_handler(button, self):
        container = self.box
        if container.get_visible():
            container.hide()
            button.set_label(f"⚫ {self.json_prop}") #"🕳️"
        else:
            container.show()
            button.set_label(f"🟠 {self.json_prop}") # 👁️") #"🟠"
        print(self.current_layer.get_name())
    
    def insert(self, *args):
        for w in args:
            self.box.pack_start(w, False, False, 1)
        return self
