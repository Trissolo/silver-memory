import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .TrisEnum import TrisEnum
from .generic_helpers import make_listbox, make_box, make_button
from .Necessary import Necessary

class hovernamesChooser(Necessary):
    def __init__(self, prop, idx):
        self.idx = idx
        self.property = prop
        self.enum = TrisEnum(self.gamedata['onHoverNames'], "Things names (on_pointer_over")
        # Value to save in the parasite
        self.data_for_parasite = None
        self.lettererichieste = "a"

        # "div"
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=0)
        self.div.set_hexpand(True)

        #searchWidget
        searchWidget = Gtk.SearchEntry()
        searchWidget.show()    
        searchWidget.connect("search-changed", self.on_search_activated)

        # ListBox:
        listbox = make_listbox(self.enum.tlist)
        listbox.set_sort_func(self.sort_func, None, False)
        listbox.set_filter_func(self.tris_filter_func, False)
        listbox.connect("row-activated", self.on_row_activated_grid)

        #scrolled
        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        scrolled.set_hexpand(True)

        #top container
        self.preview_label = Gtk.Label.new("----")
        self.preview_label.show()
        self.confirm_button = make_button(GimpUi.ICON_GO_PREVIOUS, "Confirm HoverName Button")# GimpUi.Button.new_from_icon_name(GimpUi.ICON_MENU_LEFT, 1) #Gtk.Button.new_with_label("Click Me")
        self.confirm_button.connect("clicked", self.on_confirm_clicked)

        # reset option!
        self.clear_pending_option()

        tcont = make_box(True, 0)
        tcont.pack_start(self.preview_label, True, True, 2)
        tcont.pack_end(self.confirm_button, False, False, 2)
        tcont.show()

        self.listbox = listbox
        self.scrolled = scrolled

        self.div.pack_start(tcont, False, False, 1)
        self.div.pack_start(searchWidget, False, False, 1)
        self.div.pack_start(scrolled, True, True, 1)

    def show(self):
        self.div.show()
        self.listbox.show()
        self.scrolled.show()
    def hide(self):
        self.div.hide()
    @staticmethod
    def sort_func(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        print(self.lettererichieste)
        self.listbox.invalidate_filter()
    def tris_filter_func(self, row, notify_destroy):
        return True if self.lettererichieste.lower() in row.data.lower() else False
    def on_row_activated_grid(self, listbox_widget, row):
        num, text = self.enum.get_all(row.data)
        self.preview_label.set_text(f"{text} [{num}]")
        self.set_data_for_parasite(num)
        self.confirm_button.show()
    
    def clear_pending_option(self):
        self.confirm_button.hide()
        self.preview_label.set_text("----")
        self.set_data_for_parasite()
        return self
    
    def on_confirm_clicked(self, button):
        # transfer data for parasite to the SummaryWidget
        data = self.get_data_for_parasite()
        summary_widget = self.summary_widget_from_idx(self.idx)

        summary_widget.receive_data(data)
        self.clear_pending_option()

        # GUI stuff
        # hide these tools
        self.hide()
        # Make the Save button accessible
        summary_widget.button_b.show()
        return self
    
    def get_button(self):
        return self.confirm_button
    def set_data_for_parasite(self, num=None):
        self.data_for_parasite = num
        return self
    def get_data_for_parasite(self):
        return self.data_for_parasite
