import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .imagestuff import ImageStuff

class GuiBarGenerator(ImageStuff):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def top_bar_write(self, text = "No message yet"):
        self._top_label.set_text(text)
        return self
    
    def top_bar_refresh_layer(self, button):
        self.update_layer()

    def top_bar_next_layer(self, button):
        self.select_adjacent_layer(button.dir).update_layer()

    def generate_top_bar(self):
        # container
        box = self._gui_element_box(name="Top Bar")

        # params
        temp_tuple = (
            (GimpUi.ICON_VIEW_REFRESH, self.top_bar_refresh_layer),
            (GimpUi.ICON_GO_PREVIOUS, self.top_bar_next_layer, -1),
            (GimpUi.ICON_GO_NEXT, self.top_bar_next_layer, 1),
            (GimpUi.ICON_DOCUMENT_SAVE, self.placeholder_button_click)
        )

        for params in temp_tuple:
            b = self._gui_element_default_icon_button(*params)
            box.pack_start(b, False, False, 2)
     
        # add label
        self._top_label = label = Gtk.Label.new("Layer name")
        box.pack_start(label, True, True, 2)
        #box.set_center_widget(label)
        box.reorder_child(label, 3)
        
        
        # Done! Show the Bar!
        box.show_all()
        return True
    
    def middle_bar_remove_parasite(self, button):
        print("Removing...")
        return #self.detach_parasite_from_current_layer()
    
    def generate_middle_bar(self):
        box = self._gui_element_box(name="Middle Bar")

        b = self._gui_element_default_icon_button(GimpUi.ICON_CLOSE, self.middle_bar_remove_parasite)
        box.pack_start(b, False, False, 2)

        self._middle_label = Gtk.Label.new("Generic Message")
        box.pack_start(self._middle_label, True, True, 2)

        box.show_all()
        return
        
    
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
    def _gui_element_box(self, isHorizontal=True, addToContentArea=True, name=None):
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL if isHorizontal else Gtk.Orientation.VERTICAL, 2)
        if name:
            box.set_name(name)
        if addToContentArea:
            self.get_content_area().pack_start(box, False, False, 1)
        return box
    
    def placeholder_button_click(self, widget):
        model = self.tw.get_model()
        print("Model:", model)
        model[self.curr_sel.row_idx][4] = self.tw.color_set 
        print(self.curr_sel)
        return print(f"Clicked {widget.get_name()}")
