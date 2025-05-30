import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


from .LayerManager import LayerManager
from .TrisData import TrisData
from  ..logic.prefabs.MarkupLabel import MarkupLabel  #prefabs.MarkupLabel import MarkupLabel
#from .prefabs.LeftSummary import LeftSummary
from ..splitted_gamedata.gamedata_grabber import thingProps_dataSize

#vars_ary, hover_names_ary, thingKind_dict
#vars_names_ary, hover_names_ary, thingProps_dataSize, thingKind_dict = grab_file_hardcoded()
#thingProps_props = thingProps_dataSize.keys()

print(f"{TrisData=}")

print(f"{MarkupLabel=}")

class TrisSummary(LayerManager):
    datasize_by_property = thingProps_dataSize
    def __init__(self, property, names_array):
        super().__init__(None)
        self.property = property
        self.data = TrisData(type(self).datasize_by_property[property], None)
        self.names_array = names_array
        
        # GUI stuff
        #self.left = LeftSummary(property=property)
        self.div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        #self.div.pack_start(self.left.div, False, False, 0)
        self.div.show()

        #print(f"(Summary for '{property}' here!)")
        #print(f"{property} widget has also:\n{self.names_array=}")

    def refresh(self):
        para = self.layer.get_parasite(self.property)
        if para is None:
            self.data.reset_final()
            self.data.proposal_rejected()
        else:
            self.data.absorb_parasite(para)
        
        #print(f"Layer {self.layer.get_name()} <{self.property}: {self.parse_final()}>\n")
        #return self.parse_final()
        self.on_left_gui()
    def on_left_gui(self):
        val = self.parse_final()
        if val is None:
            val = "- - - -"
        self.left.label_b.write(val, width=20, monospace=True)

    def parse_ary(self, ary):
        #print("Parsing Array:", ary)
        val_at_zero = ary[0]
        return None if val_at_zero is None else self.names_array[val_at_zero]
    
    def parse_final(self):
        return self.parse_ary(self.data.final)
    
    def parse_proposed(self):
        return self.parse_ary(self.data.proposed)




'''
from .trisLabel import TrisLabel

from .generic_helpers import make_button, make_box, multipack
from .Necessary import Necessary

class TrisSummary(Necessary):
    def __init__(self, prop, idx):
        self.property = prop
        self.idx = idx
        self.parasite_data = None

        #First Label
        self.label_key = TrisLabel(f"{prop}:")
        self.label_key.set_xalign(0)

        #Second Label (current value)
        self.label_value = TrisLabel("----")
        self.label_value.set_xalign(0)

        # First Button (open tools)
        self.button_a = make_button(GimpUi.ICON_GO_NEXT, f"Button_a {prop}", self.manifest_tool_widget)
        
        # Second Button (save the changes)
        self.button_b = make_button(GimpUi.ICON_DOCUMENT_SAVE, f"Button_b for saving: {prop}", self.save_prop_in_parasite)
        self.button_b.hide()

        # Third Button (clear ongoing changes)
        #self.button_c = make_button(GimpUi.ICON_GO_DOWN, f"Button_c for canceling: {prop}", self.clear_reset_cancel)

        # Fourth Button (clear ongoing changes)
        self.button_d = make_button(GimpUi.ICON_DIALOG_ERROR, f"Button_d for REMOVE: {prop}", self.on_remove_clicked)
        self.button_d.hide()

        # Box container
        div = make_box(True, 4, f"Div Left for{prop}")
        multipack(div, self.label_key, self.label_value, packing=True, spacing=2)
        multipack(div, self.button_a, self.button_b, self.button_d, from_end=True, packing=False, spacing=2)
        self.div = div

        #At first the save button is hidden
        self.button_b.hide()
        
        # (end TrisSummary init)
    
    def show(self):
        self.div.show()
        return self
    
    def hide(self):
        self.div.hide()
        return self
    
    def _show_off_json_key(self, use_bold = False, use_italic = False):
        self.label_key.write(text=None, color=0x989898, monospace=True, bold=use_bold, italic=use_italic, size=110)
        return self
    
    def _show_off_json_value(self, text = None, highlight = False):
        self.label_value.write(text=text, bgcolor=0x45ba76, size=116, pad=1, monospace=True) if highlight else self.label_value.write(text, size=116, pad=2, monospace=True)
        return self
    
    def labels_no_data(self):
        self._show_off_json_key()
        self._show_off_json_value()
        return self
    
    def labels_existing_data(self, text):
        self._show_off_json_key(use_bold=True)
        self._show_off_json_value(text)
        return self
    
    def labels_potential_data(self, text):
        self._show_off_json_key(use_italic=True)
        self._show_off_json_value(text, highlight=True)
        return self

    def receive_data(self, para_data):
        self.parasite_data = para_data
        parsed_text = self.parse_parasite_data(para_data)
        self.labels_potential_data(parsed_text)
        self.button_b.show()
        return self
    
    def manifest_tool_widget(self, button):
        target_widget = self.tool_widget_from_idx(self.idx)
        to_be_shown = not target_widget.div.get_visible()
        for tool_widget in self.tool_widgets_ary:
            tool_widget.hide()
        if to_be_shown: target_widget.show()
    
    def clear_reset_cancel(self, button):
        button.hide()
        self.refresh()
    
    def get_parasite(self):
        return self.current_layer.get_parasite(self.property)

    def refresh(self):
        para = self.get_parasite()
        if para is None:
            self.labels_no_data()
        else:
            data = Necessary.grab_parasite_data(para)
            parsed_text = self.parse_parasite_data(data)
            self.labels_existing_data(parsed_text)
            self.button_d.show()
            # duplicate code
            for tool_widget in self.tool_widgets_ary:
                tool_widget.hide()
            # end duplicate code
    
    def save_xcf(self):
        Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, self.image, self.image.get_xcf_file(), None)
        self.image.is_dirty()
        self.image.clean_all()
        return self
    
    def remove_parasite(self):
        if self.property in self.current_layer.get_parasite_list():
            self.current_layer.detach_parasite(self.property)
        return self
    
    def add_parasite(self):
        d = Necessary.encode_data(self.parasite_data)
        p = Gimp.Parasite.new(name=self.property, flags=Gimp.PARASITE_PERSISTENT, data=d)
        self.current_layer.attach_parasite(p)
        #return self.save_xcf()
        return print(f"Parasite '{self.property}' attached to layer")
    
    def save_prop_in_parasite(self, button):
        self.remove_parasite().add_parasite()
        self.button_b.hide()
        self.refresh()
    
    def parse_parasite_data(self, data):
        result = None
        if type(data) is int:
            result = self.gamedata["onHoverNames"][data]
        else: #if type(data is list):
            value_text = self.tool_widget_from_idx(self.idx).enum.get_corresponding(data[1])
            kind_text = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"][data[0]]
            result = f"{value_text} ({kind_text.capitalize()} #{data[1]})"
            if len(data) == 3:
                result = f"if {result} == {data[2]}"
        return result
    
    def on_remove_clicked(self, button):
        self.remove_parasite()
        self.button_d.hide()
        self.refresh()
'''
