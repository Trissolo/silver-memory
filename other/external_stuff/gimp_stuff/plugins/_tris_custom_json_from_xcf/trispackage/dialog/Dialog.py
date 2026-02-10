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
from ..mixins.RightTreeView import LeftTreeViev

class TrisDialog(LayerManager, LeftTreeViev):
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
        #self.tw = LeftTreeViev()
        self.tw = self.build_trislist()
    
    

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
        