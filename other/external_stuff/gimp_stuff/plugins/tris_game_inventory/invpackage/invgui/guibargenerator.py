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
        return self
    
    def top_bar_refresh_layer(self, button):
        self.update_layer()

    def next_layer_from_button(self, button):
        self.select_adjacent_layer(button.dir).update_layer()

    def generate_top(self, box = None):
        # container
        if box is None:
            box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
            box.set_name("Top_Bar")
            self.get_content_area().pack_start(box, False, False, 1)
            print("Was none")
        else:
            print("box received", box.get_name())
        # params
        temp_tuple = (
            (GimpUi.ICON_VIEW_REFRESH, self.top_bar_refresh_layer),
            (GimpUi.ICON_GO_PREVIOUS, self.next_layer_from_button, -1),
            (GimpUi.ICON_GO_NEXT, self.next_layer_from_button, 1),
            #(GimpUi.ICON_DOCUMENT_SAVE, self.top_bar_refresh_layer)
        )

        for params in temp_tuple:
            b = self._gui_element_default_icon_button(*params)
            box.pack_start(b , False, False, 2)
     
        # add label
        label = Gtk.Label.new("Layer name")
        box.pack_start(label, True, True, 2)
        #box.set_center_widget(label)
        box.reorder_child(label, 3)
        self._top_label = label
        # Done! Show the Bar!
        box.show_all()
        return True
    
    @staticmethod
    def _gui_element_default_icon_button(icon_name, click_callback, custom_attribute = None):
        button = GimpUi.Button.new_from_icon_name(icon_name, 1)
        button.set_halign(1)
        button.set_valign(1)
        button.connect('clicked', click_callback)
        #button.set_name(f'Btn_{name}')
        if custom_attribute:
            button.dir = custom_attribute
        return button
        
