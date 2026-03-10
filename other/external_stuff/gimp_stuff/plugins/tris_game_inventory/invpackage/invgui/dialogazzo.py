import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# dataclass
from dataclasses import dataclass

@dataclass
class SelectionInfo:
    prop: str | None
    size: int | None
    row_idx: int | None
    wid: Gtk.Widget | None
    def clear(self):
        self.prop = None
        self.size = None
        self.row_idx = None
        self.wid = None
    def set_widget(self, widget):
        self.wid = widget
        return self


class Dialogazzo(GimpUi.Dialog):
    def __init__(self, *args):
        # First of all
        super().__init__(title="Tris Inventory Generator", *args)
        self.add_buttons( "Ok (Close)", Gtk.ResponseType.OK)
        self.connect("destroy", self._on_destroy)
        self.row_infos = []
        self.curr_sel = None
        self.build_schemino()
        self.show_all()
    def _on_destroy(self, widget):
        print("Checking row_info:", self.row_infos[0])
        for elem in self.row_infos:
            elem.clear()
        self.row_infos = self.row_infos.clear()
        self.destroy()
        print('Calling "super().destroy()"')
        super().destroy()
    def build_schemino(self):
        # self.get_content_area().pack_start(tw, False, False, 1)

        row_infos = self.row_infos

        properties_size = {
            "kind": 1,
            "hoverName": 1,
            "suffix": 2,
            "skipCond": 3,
            "noInteraction": 1,
            "roomStatus": 2,
            "roomVariable": 2
        }
        column_headers = ["Prop", "Readable", "Effective"]

        column_amount = len(column_headers)

        id_for_others = column_amount + 1

        mytypes = [str] * len(column_headers)

        cell_types = [*mytypes, str, str]

        # the Store/Model!
        store = Gtk.ListStore.new(cell_types)

        # the TreeView
        tw = Gtk.TreeView.new()

        tw.set_model(store)

        # constants AS!
        tw.text_empty = "---"
        tw.color_empty = "#343434"
        tw.color_selected = "#ff0"
        tw.color_set = "#66a"

        # populate the store:
        for idx, (prop, size) in enumerate(properties_size.items()):
            store.append([prop, tw.text_empty, tw.text_empty, tw.color_empty, tw.color_empty])
            row_infos.append(SelectionInfo(prop, size, idx, None))
        
        cell = Gtk.CellRendererText.new()

        for idx, name in enumerate(column_headers):
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=3 if idx==0 else 4)
            tw.append_column(col)
        
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
        self.get_content_area().pack_start(tw, False, False, 1)
    def on_active_row(self, liststore, row_idx, colu):
        print("On Active Row!")
        index_as_int = row_idx.get_indices()[0]
        liststore.get_selection().unselect_all()
        model = liststore.get_model()
        if self.curr_sel is not None:
            model[self.curr_sel.row_idx][3] = model[self.curr_sel.row_idx][4]
        model[index_as_int][3] = liststore.color_selected
        model[index_as_int][4] = liststore.color_empty
        self.curr_sel = self.row_infos[index_as_int]
        print(f"CurrSel: {self.curr_sel}")
        print(f"Analogies? {index_as_int=} -> {self.curr_sel.row_idx} -*- {model[row_idx][0]=} -> {self.curr_sel.prop} {model[row_idx][0]}")


dialogazzo = Dialogazzo()
#dialogazzo.destroy()
