import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class GuiBarGenerator():
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    def top_bar_write(self, text = "No message yet"):
        self._top_label.set_text(text)
    def top_bar_refresh_layer(self, widget = None):
        self.update_layer()
        self.top_bar_write(self.layer.get_name())
    def next_layer_from_button(self, button):
        self.select_adjacent_layer(button.dir)
        self.top_bar_refresh_layer()
    def generate_top(self):
        # container
        subdiv = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        self.get_content_area().pack_start(subdiv, False, False, 1)
        # params
        temp_tuple = (
        (GimpUi.ICON_VIEW_REFRESH, self.top_bar_refresh_layer),
        (GimpUi.ICON_GO_PREVIOUS, self.next_layer_from_button, -1),
        (GimpUi.ICON_GO_NEXT, self.next_layer_from_button, 1)
        )
        # add buttons
        for icon_name, click_callback, *additiona_prop  in temp_tuple:
            button =  GimpUi.Button.new_from_icon_name(icon_name, 1)
            button.set_halign(1)
            button.set_valign(1)
            #button.set_name(f'Btn_{name}')
            if len(additiona_prop):
                button.dir = additiona_prop[0]
            if click_callback is not None:
                button.connect('clicked', click_callback)
            # Finally add the new button to container
            subdiv.pack_start(button, False, False, 2)
     
        # add label
        label = Gtk.Label.new("Layer name")
        subdiv.pack_start(label, True, True, 2)
        #subdiv.set_center_widget(label)
        subdiv.reorder_child(label, 3)
        self._top_label = label
        # Done! Show the Bar!
        subdiv.show_all()
        return True

        # for p in (
        #     (GimpUi.ICON_VIEW_REFRESH, self.clicked_update_layer, "refresh_layer"),
        #     (GimpUi.ICON_GO_PREVIOUS, self.expensive_next, "sel_prev_layer", "dir", -1),
        #     (GimpUi.ICON_GO_NEXT, self.expensive_next, "sel_next_layer", "dir", 1),
        #     (GimpUi.ICON_DOCUMENT_SAVE, self.brandnew_generate_json, "generate_json"),
        #     (GimpUi.ICON_TOOL_CAGE, self.get_polygons, "extract_paths"),
        #     (GimpUi.ICON_FORMAT_JUSTIFY_LEFT, self.show_rscript, "copy_rscript")
        #     ):
        #     icon, action, name, *other = p
        #     button = GimpUi.Button.new_from_icon_name(icon, 1)
        #     button.connect('clicked', action)
        #     button.set_name(f'Btn_{name}')
        #     button.set_halign(1)
        #     button.set_valign(1)
        #     if len(other):
        #         setattr(button, other[0], other[1])
        #     subdiv.pack_start(button, False, False, 2)

        # # label
        # label = Gtk.Label.new("Layer name")
        # subdiv.pack_start(label, True, True, 2)
        # #subdiv.set_center_widget(label)
        # subdiv.reorder_child(label, 3)
        # subdiv.show_all()