import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#from ..toolwidgets.KindsWidget import KindsWidget
#from ..mixins.LayerManager import LayerManager
#from ..gamedata.GamedataGatherer import GamedataGatherer
from ..gamedata.GamedataGatherer import GamedataGatherer

class LeftTreeViev():
    def build_trislist(self):
        print("Trislist!", GamedataGatherer.props, GamedataGatherer.props_datasize, GamedataGatherer.hoverNames)
        store = Gtk.ListStore.new([str, str, str, str, str])
        self.store = store
        store.append(['Mario', 'Rossi', "#000", "#888", '#999']) 
        store.append(['Germy', 'Moscon', "#000", '#f44', '#44f'])

        tw = Gtk.TreeView.new()
        tw.set_model(store) #(model=store)
        print(tw)

        cell_a = Gtk.CellRendererText.new()

        column_one = Gtk.TreeViewColumn("Header_Nome", cell_a, text=0, foreground=2, background=3) #, underline=4, size=5)
        column_one.set_name("Column_one")
        column_two = Gtk.TreeViewColumn("Header_Cognome", cell_a, text=1, foreground=2, background=4)
        column_two.set_name("Column_two")
        tw.append_column(column_one)
        tw.append_column(column_two)

        self.div.pack_start(tw, False, False, 1)
        self.dialog.show_all()

        tw.get_selection().unselect_all()
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active)
        return tw

    def on_active(self, treeview, row_idx, colu):
        print(f"TreeView: {treeview}\nRow[{row_idx}]\nColumn: {colu.get_name()}")
        treeview.get_selection().unselect_all()
        for i, elem in enumerate(treeview.get_columns()):
            self.store[i][3] = "#777"

        self.store[row_idx][3] = "#ff0"
