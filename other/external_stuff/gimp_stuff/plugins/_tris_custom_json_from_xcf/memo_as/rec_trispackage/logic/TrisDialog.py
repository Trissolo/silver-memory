from .LayerManager import LayerManager
#from .TrisSummary import TrisSummary
from .TrisSummaryOld import TrisSummary
#from ..summary_stuff.TrisSummary import TrisSummary
#from ..summarystuff.TrisSummary import TrisSummary
from ..splitted_gamedata.gamedata_grabber import thingProps_dataSize, names
from .prefabs.MainBar import MainBar
import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrisDialog(LayerManager):
    def __init__(self, image):
        super().__init__(image=image)
        self.gui_widget = []
        self.div = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.dialog = self.build_dialog(self.div)
        self.main_bar = MainBar()

        
        self.div.pack_start(self.main_bar.div, False, False, 0)

        #self.main_bar.refresh_button_action(self.update_layer)
        self.main_bar.refresh_button_action(self.refresh_all)

        # Test layer stuff...

        print(f"TrisDialog's {self.layer.get_name() =}")
        print("KEYS:", *thingProps_dataSize.keys())
        newsumm = TrisSummary('kind', ["abc", "def", "ghi"])
        self.div.pack_start(newsumm.div, False, False, 0)


        for jproperty in thingProps_dataSize.keys():
            prop_widget = TrisSummary(jproperty, names["hover_names_ary"])
            self.gui_widget.append(prop_widget)
            self.div.pack_start(prop_widget.div, False, False, 0)
        
    def refresh_all(self, button):
        self.update_layer()
        self.main_bar.write_layer_name(self.layer)

        #print(self.layer.get_name())
        print("\nREFRESHING:")
        for widget in self.gui_widget:
            widget.refresh()
         
    def build_dialog(self, child):
        dialog = GimpUi.Dialog.new()
        dialog.set_title('Test_update_button')
        dialog.set_border_width(10)
        dialog.set_name("THE TrisDialog!")
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Done (Save [not yet implemented])", Gtk.ResponseType.OK)
        dialog.get_content_area().pack_start(child, False, False, 0)
        return dialog
        
