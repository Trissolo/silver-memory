import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .hovernameschooser import hovernamesChooser
from .ToolSuffix import ToolSuffix
from .TrisSummary import TrisSummary
from .trisLabel import TrisLabel
from .generic_helpers import make_box, make_button
from .Necessary import Necessary
from .TrisData import TrisData

class TrisDialog(Necessary, GimpUi.Dialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_border_width(10)
        self.set_name("THE TrisDialog!")
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Done (Save [not yet implemented])", Gtk.ResponseType.OK)

        #top bar
        top_div = self.make_top_bar()
        self.get_content_area().pack_start(top_div, False, False, 4)

        #containers
        left_box, right_box = self.generate_containers()

        # slots:
        # hovernamesChooser --> 1 slot
        # ToolSuffix ---------> 2 slots
        hardcoded_slot_amount = [1, 2]
        #populate
        #for idx, prop in enumerate(self.gamedata["thingProps"]):
        for idx, tool_class in enumerate([hovernamesChooser, ToolSuffix]):
            prop = self.gamedata["thingProps"][idx]
            # build the TrisData and place it in the appropriate array inside the 'Necessary' class
            slots = hardcoded_slot_amount[idx]
            Necessary._parasite_data_ary.append(TrisData(slots))
            
            # build the SummaryWidget
            summary_widget = TrisSummary(prop, idx)
            left_box.pack_start(summary_widget.div, False, False, 0)
            self.summary_widgets_ary.append(summary_widget)
            #and now the ToolWidget
            temp_tool_widget = tool_class(prop, idx)
            self.tool_widgets_ary.append(temp_tool_widget)
            right_box.pack_start(temp_tool_widget.div, True, True, 0)
        
        print("TRICAZZUS!")
        #test
        #Necessary.update_layer()
        #Necessary.grab_existing_parasite_data()
        #### END TrisDialog init ####
    
    def refresh_all(self):
        self.hide_all_tools()
        for wid in self.summary_widgets_ary:
            print(f"Refreshing: {wid}")
            wid.refresh()
        print("Refresh_all (done)\n")

    def hide_all_tools(self):
        for tool_widget in self.tool_widgets_ary:
            tool_widget.hide()
        return self
        
    def generate_summary_widget(self, param, idx):
        return TrisSummary(param, idx, self)
       
    def generate_containers(self):
        temp_sp = 4

        left_box = make_box(False, temp_sp, "Summary Box")
        right_box = make_box(True, temp_sp, "Tools Box")   
        ulteriore = make_box(True, temp_sp, "Ulteriore")

        ulteriore.pack_start(left_box, False, True, temp_sp)
        ulteriore.pack_start(right_box, True, True, temp_sp)

        self.get_content_area().pack_start(ulteriore, True, True, temp_sp)
        self.get_content_area().set_name("Dialog Content Area")

        self.left_box = left_box
        self.right_box = right_box
        return left_box, right_box
    
    def make_top_bar(self):
        update_button = make_button(GimpUi.ICON_VIEW_REFRESH, "Update Layer", self.update_button_action)

        label_for_image_name = TrisLabel(f"<{self.image.get_name()}>")
        label_for_image_name.set_name("Descr Image Name")
        label_for_image_name.show()

        top_div = make_box(True, 4, "Div Top Bar")

        top_div.pack_start(update_button, False, False, 0)
        top_div.pack_start(label_for_image_name, True, True, 0)

        self.update_button = update_button
        self.label_for_image_name = label_for_image_name
        return top_div
    
    def update_button_action(self, button):
        self.update_current_layer()
        self.label_for_image_name.set_text(self.current_layer.get_name(), bgcolor=0x656598, pad=6)

        #not sure if this method is the right place for this
        self.refresh_all()
