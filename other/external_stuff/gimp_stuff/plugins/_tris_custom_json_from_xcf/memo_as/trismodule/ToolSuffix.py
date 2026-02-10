import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .TrisEnum import TrisEnum
from .Necessary import Necessary
from .generic_helpers import make_button, make_box, multipack

class ToolSuffix(Necessary):
    vars_names = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"]
    def __init__(self, prop, idx):
        self.idx = idx
        self.property = prop

        self._enums = []
        self.actual_varkind = 0

        self.data_for_parasite = []
        self._populate_enums()
        self.lettererichieste = "a"
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=0)
        self.div.set_hexpand(True)

        self.fake_radio = None
        self.forbidden_value = None
        self.radio_container = self._build_radio_buttons()
        self.clear_pending_option()

        #searchWidget
        searchWidget = Gtk.SearchEntry()
        searchWidget.show()    
        searchWidget.connect("search-changed", self.on_search_activated)
        self.searchWidget = searchWidget

        # ListBox:
        listbox = Gtk.ListBox()
        listbox.set_name("Listbox Varnames")
        listbox.show()
        

        # populate the ListBox
        for idx, names_ary in enumerate(self._enums):
            for item in names_ary.tlist:
                optn_label = Gtk.Label.new(item)
                optn_label.show()
                option = Gtk.ListBoxRow.new()
                option.set_name(f"option {item}")
                option.data = item
                option.kind = idx
                option.add(optn_label)
                option.show()
                listbox.add(option)

        listbox.set_sort_func(self.sort_listbox, None, False)
        listbox.set_filter_func(self.tris_filter_func, False)
        listbox.connect("row-activated", self.on_row_activated)

        #scrolled
        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)
        scrolled.set_hexpand(True)
        scrolled.show()

        #top container
        self.preview_label = Gtk.Label.new("----")
        self.preview_label.show()
        self.confirm_button = make_button(GimpUi.ICON_MENU_LEFT, "Confirm HoverName Button")# GimpUi.Button.new_from_icon_name(GimpUi.ICON_MENU_LEFT, 1) #Gtk.Button.new_with_label("Click Me")
        self.confirm_button.connect("clicked", self.on_confirm_clicked)

        # Top bar
        tcont = make_box(True, 0)
        tcont.pack_start(self.preview_label, True, True, 2)
        tcont.pack_end(self.confirm_button, False, False, 2)
        tcont.show()

        self.div.pack_start(tcont, False, False, 1)  
        self.div.pack_start(self.radio_container, False, False, 0)      
        self.div.pack_start(searchWidget, False, False, 1)
        self.div.pack_start(scrolled, True, True, 1)

        self.listbox = listbox
        self.div.connect("show", self.set_radio_status)

    def hide(self):
        self.div.hide()

    def set_radio_status(self, widget):
        complemetary_widget = self.summary_widget_from_idx(self.idx)
        # duplicate code
        para = complemetary_widget.get_parasite()
        if para:
            data = Necessary.grab_parasite_data(para)[0]
            for elem in self.fake_radio.get_group():
                if elem.value == data:
                    elem.set_active(True)
                    self.set_actual_varkind(self.forbidden_value)
                    return
        else:
            self.fake_radio.set_active(True)
        # End duplicate code

    def on_search_activated(self, searchentry):
        self.lettererichieste = searchentry.get_text()
        print(self.lettererichieste)
        self.listbox.invalidate_filter()

    def on_confirm_clicked(self, button):
        # transfer data for parasite to the SummaryWidget
        #
        if self.data_for_parasite[0] == self.forbidden_value or self.data_for_parasite[1] is None:
            return
        data = self.data_for_parasite.copy()
        summary_widget = self.summary_widget_from_idx(self.idx)
        summary_widget.receive_data(data)
        self.clear_pending_option()

    def clear_pending_option(self):
        qualc = self.radio_container.get_children()[0]
        print("qualc", qualc.get_name())
        # togliere da qui in su
        #self.radio_container.get_children()[0].emit("toggled")
        self.radio_container.show()


    def on_row_activated(self, listbox_widget, row):
        num, text = self.enum.get_all(row.data)
        print(num, text)
        self.preview_label.set_text(f"{text} {type(self).vars_names[self.actual_varkind]}[{num}]")
        self.data_for_parasite[1] = num
        self.confirm_button.show()

    @staticmethod
    def sort_listbox(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    
    def tris_filter_func(self, row, notify_destroy):
        return True if row.kind == self.actual_varkind and self.lettererichieste.lower() in row.data.lower() else False

    def _populate_enums(self):
        for idx, elem in enumerate(type(self).vars_names):
            self._enums.append(TrisEnum(self.gamedata[elem], f"Names for {elem} variables"))

    @property
    def enum(self):
        return self._enums[self.actual_varkind]

    def _build_radio_buttons(self):
        radio_container = make_box(is_horizontal=True, spacing=0, name="Radio Buttons Container")
        radio_container.set_homogeneous(True)

        # hardcoded
        self.forbidden_value = len(type(self).vars_names)
        prev = button = Gtk.RadioButton.new_from_widget(None)
        prev.set_label("Nothing")
        prev.set_name("Nothing")
        prev.value = self.forbidden_value
        prev.connect("toggled", self.on_button_toggled)
        self.fake_radio = prev

        for idx, var_kind in enumerate(type(self).vars_names):
            button = Gtk.RadioButton.new_from_widget(prev)
            button.set_label(f"{var_kind.capitalize()} ({idx})")
            button.set_name(var_kind)
            button.value = idx
            button.connect("toggled", self.on_button_toggled)
            radio_container.pack_start(button, False, False, 0)
            button.show()
            prev = button
        return radio_container
        # _build_radio_buttons END
    
    def on_button_toggled(self, button):
        print(f"*** on_button_toggled called by {button.get_name()} [{button.value}]")
        for b in button.get_group():
            b.set_inconsistent(False)
        
        if button.get_active():
            self.set_actual_varkind(button.value)
            self.listbox.invalidate_filter()
            self.searchWidget.set_text("")
            self.searchWidget.emit("search-changed")
        #print("Bu status")
        for b in button.get_group():
            print(f"{'* ' if b.get_active() else '  '}[{b.get_name()}] {b.value}")
    
    def set_actual_varkind(self, value = 0):
        self.actual_varkind = value
        self.data_for_parasite.clear()
        self.data_for_parasite.append(value)
        self.data_for_parasite.append(None)
        if value != self.forbidden_value:
            print(f"\n***\nset_actual_varkind():\nactual_varkind = {self.actual_varkind} ({type(self).vars_names[value]})\nPara data array: {self.data_for_parasite}\n***\n")
    
    def show(self):
        self.div.show()