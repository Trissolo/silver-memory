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
            (GimpUi.ICON_DOCUMENT_SAVE, self.top_bar_generate_json),
            (GimpUi.ICON_FORMAT_JUSTIFY_LEFT, self.top_bar_generate_script)
            #(GimpUi.ICON_TOOL_CAGE, self.get_polygons, ),
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
        selected = self.curr_sel

        self.detach_parasite_from_current_layer(selected.prop)
        row = self.tw.get_model()[selected.row_idx]
        row[1] = row [2] = self.CONST_TEXT_EMPTY
        row[3] = "#784332"
    
    def generate_middle_bar(self):
        box = self._gui_element_box(name="Middle Bar")

        b = self._gui_element_default_icon_button(GimpUi.ICON_CLOSE, self.middle_bar_remove_parasite)
        box.pack_start(b, False, False, 2)

        self._middle_label = self._gui_element_label("Generic Message", True)
        box.pack_start(self._middle_label, True, True, 2)

        box.show_all()
        return
    
    def middle_bar_write(self, text):
        borders = " " * 16
        color = None
        lab = self._middle_label
        if lab.get_justify() == Gtk.Justification.LEFT:
            lab.set_justify(Gtk.Justification.FILL)
            color="#755"
        else:
            lab.set_justify(Gtk.Justification.LEFT)
            color="#557"
        return lab.set_markup(f'<span background="{color}">{borders}{text}{borders}</span>')
    
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
    def _gui_element_paned(self):
        paned = Gtk.Paned.new(orientation=Gtk.Orientation.HORIZONTAL)
        self.get_content_area().pack_start(paned, True, True, 0)
        return paned
    def _gui_element_label(self, text, useMarkup = False):
        label = Gtk.Label(text)
        label.set_use_markup(useMarkup)
        label.show()
        return label
    
    def placeholder_button_click(self, widget):
        print("Clicked button", widget.get_name())

    def top_bar_generate_json(self, widget):
        self.generate_json()
        self.middle_bar_write("You can now paste the JSON")
    def top_bar_generate_script(self, widget):
        res = []
        triggerArea_params = '(ta, actor, boolInside)'
        thing_params = '(thing)'
        
        for i, layer in enumerate(self._layer_iterator()): #(l for l in self.image.get_layers() if 'kind' in l.get_parasite_list() and self.extract_array_from_parasite('kind', l)[0] > 0)):
            current_kind = self.extract_array_from_parasite('kind', layer)[0]

            if current_kind == -5:
                continue

            isTriggerZone = current_kind == 1

            for scripttext in (
            '',
            f"// {layer.get_name()}",
            f'static {i}{triggerArea_params if isTriggerZone else thing_params}',
            '{',
            f'    console.log({"ta" if isTriggerZone else "thing"});',
            '}'
            ):
                res.append(scripttext)

        res = '\n    '.join(res)

        header = f'export default class rs{self.extract_id_for_json()}'

        self.output_string_to_clipboard(f'{header}\n{{{res}\n}}\n')

        return self.middle_bar_write("Script ready")
