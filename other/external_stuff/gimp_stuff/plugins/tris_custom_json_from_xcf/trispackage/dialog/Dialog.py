import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#from ..toolwidgets.KindsWidget import KindsWidget
from ..mixins.LayerManager import LayerManager
from ..gamedata.GamedataGatherer import GamedataGatherer

class TrisDialog(LayerManager):
    def __init__(self, image):
        
        LayerManager.provide_image(image)
        self.gui_widget = []
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.dialog = self.build_dialog(self.div)
        #self.main_bar = MainBar()
        print(GamedataGatherer)
        #test_kinds_widget = KindsWidget(2)#"kind")
        #test_kinds_widget.info()
        #self.dialog.get_content_area().pack_start(test_kinds_widget.div, True, True, 2)
        self.build_trislist()
    
    def build_trislist(self):
        print("Trislist...")
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
        #dialogazzo.show_all()
        self.dialog.show_all()

        tw.get_selection().unselect_all()
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active)

    def on_active(self, treeview, row_idx, colu):
        print(f"TreeView: {treeview}\nRow[{row_idx}]\nColumn: {colu.get_name()}")
        treeview.get_selection().unselect_all()
        for i, elem in enumerate(treeview.get_columns()):
            self.store[i][3] = "#777"

        self.store[row_idx][3] = "#ff0"


    #def refresh_all(self, button):
    #    self.update_layer()
    #    self.main_bar.write_layer_name(self.layer)

        #print(self.layer.get_name())
        #print("\nREFRESHING:")
        #for widget in self.gui_widget:
        #    widget.refresh()
         
    def build_dialog(self, child):
        dialog = GimpUi.Dialog.new()
        dialog.set_title('Test_update_button')
        dialog.set_border_width(10)
        dialog.set_name("THE TrisDialog!")
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Done (Save [not yet implemented])", Gtk.ResponseType.OK)
        dialog.get_content_area().pack_start(child, False, False, 0)
        return dialog
        