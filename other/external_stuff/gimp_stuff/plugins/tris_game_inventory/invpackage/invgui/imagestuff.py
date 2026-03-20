import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp

from ..misc.generic_utils import GenericUtils

class ImageStuff(GenericUtils):
    def remove_image_references(self):
        self.image = None
        self.layer = None
    def update_layer(self):
        '''Set the currently selected layer as active layer'''
        self.layer = self.image.get_selected_layers()[0]
        self.top_bar_write(self.layer.get_name())
        self.tw_refresh_hard()
        return self
    
    def select_adjacent_layer(self, addendum = 1):
        '''This method assumes that the argument 'button' is an Object with the property 'dir' set to 1 or -1.'''
        layers = self.image.get_layers()
        layers_length = len(layers)
        if not self.layer or layers_length < 2:
            print("No next layer. Skipping :(")
            return
        next_idx = layers.index(self.layer) + addendum
        self.image.set_selected_layers([layers[0] if next_idx == layers_length else layers[next_idx]])
        return self
    
    def attach_array_to_current_layer(self, parasite_name, integers_array):
        '''Creates a parasite with the given name and attaches it to the current layer.
        If a parasite with the same name already exists, it will be eliminated before the process.'''
        # If an old parasite with the same name already exists, detach it:
        if parasite_name in self.layer.get_parasite_list():
            self.layer.detach_parasite(parasite_name)
        # convert ary to string. i.e. [300, 150, 10] -> "300 150 10"
        stringa_dati = " ".join(map(str, integers_array)) 
        # Crea il parassita. 
        # In GIMP 3, i dati devono essere passati come bytes o GLib.Bytes
        dati_bytes = stringa_dati.encode('ascii')
        # Finally creates the parasite and attach it
        new_parasite = Gimp.Parasite.new(parasite_name, Gimp.PARASITE_PERSISTENT, dati_bytes)       
        return self.layer.attach_parasite(new_parasite)
    
    def extract_array_from_parasite(self, parasite_name, layer = None):
        '''Returns the array contained in the parasite identified by the given name.
        Or an empty array if the parasite does not exist.'''
        if layer is None:
            layer = self.layer
        parasite = layer.get_parasite(parasite_name)
        if not parasite:
            print(f"No parasite with name: {parasite_name}.")
            return []
        # 1. Ottieni i byte e decodificali in stringa "300 150 10"
        #raw_data = parasite.get_data()
        stringa_dati = bytes(parasite.get_data()).decode('ascii')  
        # 2. Trasforma la stringa in una lista di interi [300, 150, 10]
        try:
            integers_array = [int(n) for n in stringa_dati.split()]
            return integers_array
        except ValueError:
            return []
        
    def detach_parasite_from_current_layer(self, parasite_name):
        '''If the current layer contains a parasite identified by the specified name, that parasite is deleted.'''
        if parasite_name in self.layer.get_parasite_list():
            self.layer.detach_parasite(parasite_name)
        return
    
    def get_final_value(self, parasite_name, layer):
        return self.manage_array(self.extract_array_from_parasite(parasite_name, layer))
    
    def get_owned_parasites(self, layer = None):
        if layer is None:
            layer = self.layer
        return layer.get_parasite_list()
    
    @staticmethod
    def merge_vcoords(kind, index):
        if kind > 3:
            raise ValueError(f"kind ({kind}) is too big!")
        return (index << 2) | kind
        
    @staticmethod
    def separate_vcoords(vcoord):
        return [vcoord & 3, vcoord >> 2]
        
    def manage_array(self, ary):
        l = len(ary)
        if l == 0:
            raise ValueError(f"Array is empty!")
        if l == 1:
            return ary[0]
        vcoords = self.merge_vcoords(ary[0], ary[1])
        if l == 2:
            return vcoords
        elif l == 3:
            return [vcoords, ary[2]]
        else:
            raise ValueError(f"Array length ({l}) out of range!")
        
    def summary_debug(self, to_clipboard = True):
        layers = self.image.get_layers()
        empty = []
        res = []
        #emojis = ['✅', '❎', '🔘', '☀️', '🔥', '🌊', '💩', '🪨', '🛑', '✨']
        for l in layers:
            paras = l.get_parasite_list()
            layer_name = l.get_name()
            if len(paras) > 0:
                res.append(f"\n* {layer_name}:")
                if 'kind' in paras:
                    res.append(f"    * KIND: {self.extract_array_from_parasite('kind', l)[0]}")
                    paras.remove('kind')
                else:
                    res.append("    !!!! no KIND property")
                for elem in paras:
                    ary = self.extract_array_from_parasite(elem, l)
                    res.append(f"    - {elem}: {self.manage_array(ary)} {ary}")
            else:
                empty.append(layer_name)
        if (to_clipboard):
            self.output_string_to_clipboard(f"{'\n'.join(res)}\n\nEmpty:\n{'\n'.join(empty)}")
        else:
            print("\n".join(res))
        return True
    
    
    # @staticmethod
    def extract_id_for_json(self):
        name = self.image.get_name()
        pruned = name[4:-4]
        return int(pruned) if pruned.isdigit() else name
    
    @staticmethod
    def add_peculiar_properties(layer, obj, kind_value, remaining_props):
        _succ, x, y = layer.get_offsets()
        if kind_value == 1:
            obj['rect'] = [x, y, layer.get_width(), layer.get_height()]
            if 'suffix' in remaining_props:
                print("Removing 'suffix'")
                remaining_props.remove('suffix')
            return
        elif kind_value == 4:
            obj["x"] = layer.get_width() // 2 + x
            obj["y"] = y + layer.get_height()
        elif kind_value == 5:
            obj["x"] = layer.get_width() // 2 + x
            obj["y"] = layer.get_height() // 2 + y
        else:
            obj["x"] = x
            obj["y"] = y

        obj["frame"] = layer.get_name().rstrip("0123456789")

    def generate_json(self):
        import json

        #{ "kind": 1, "hoverName": 1, "suffix": 2, "skipCond": 3, "noInteraction": 1, "roomStatus": 8, "roomVariable": 8}
        #kind, hoverName, suffix, skipCond, noInteraction, roomStatus, roomVariable

        props = ['kind', 'hoverName', 'suffix', 'skipCond', 'noInteraction', 'roomStatus', 'roomVariable']

        kind, *other, room_props, _ = props

        room_props = props[-2:]

        things_array = []
        room_res = {'things': things_array, 'id': self.extract_id_for_json()}

        for layer in self._layer_iterator():
            parasites = layer.get_parasite_list()
            
            kind_value = self.get_final_value(kind, layer)
            if kind_value == -5:
                room_res['bg'] = layer.get_name()
                for rp in (potental_rp for potental_rp in room_props if potental_rp in parasites):
                    room_res[rp] = self.get_final_value(rp, layer)
                continue

            obj = {kind: kind_value}
            things_array.append(obj)
            parasites.remove(kind)
            print(f"Props to add: {parasites}")
            self.add_peculiar_properties(layer, obj, kind_value, parasites)
            for prop in parasites:
                obj[prop] = self.get_final_value(prop, layer)
            
        self.output_string_to_clipboard(json.dumps(room_res, indent=None, sort_keys=True))
        return
    
    def _layer_iterator(self):
        return (l for l in self.image.get_layers() if l.get_visible() and 'kind' in l.get_parasite_list())

        



'''
from collections import namedtuple

FakeWidget = namedtuple("FakeWidget", "dir")

button_next = FakeWidget(1)
button_prev = FakeWidget(-1)
test = ImageStuff(image = Gimp.get_images()[0])
'''

'''
image
layer
update_layer
remove_image_references
select_adjacent_layer
attach_array_to_current_layer
detach_parasite_from_current_layer
extract_array_from_parasite
get_owned_parasites
'''

'''
class ImageStuff():
    def __init__(self, *, image, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.layer = None
    def remove_image_references(self):
        self.image = None
        self.layer = None
    def update_layer(self):
        #Set the currently selected layer as active layer
        self.layer = self.image.get_selected_layers()[0]
    def attach_array_to_layer(self, parasite_name, integers_array):
        if parasite_name in self.layer.get_parasite_list():
            self.layer.detach_parasite(parasite_name)
        # convert ary to string. i.e. [300, 150, 10] -> "300 150 10"
        stringa_dati = " ".join(map(str, integers_array)) 
        # Crea il parassita. 
        # In GIMP 3, i dati devono essere passati come bytes o GLib.Bytes
        dati_bytes = stringa_dati.encode('ascii')
        nuovo_parassita = Gimp.Parasite.new(parasite_name, Gimp.PARASITE_PERSISTENT, dati_bytes)       
        self.layer.attach_parasite(nuovo_parassita)
    def extract_parasite_data(self, parasite_name, layer = None):
        
        parasite = self.layer.get_parasite(parasite_name)
        if not parasite:
            print(f"No parasite with name: {parasite_name}.")
            return []
        # 1. Ottieni i byte e decodificali in stringa "300 150 10"
        raw_data = parasite.get_data()
        stringa_dati = bytes(raw_data).decode('ascii')  
        # 2. Trasforma la stringa in una lista di interi [300, 150, 10]
        try:
            integers_array = [int(n) for n in stringa_dati.split()]
            return integers_array
        except ValueError:
            return []

test = ImageStuff(image = Gimp.get_images()[0])
'''
'''
#temp reference:
test_dialog = GimpUi.Dialog.new()
test_dialog.add_button("_Canc", Gtk.ResponseType.CANCEL)
sub_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
our_content_area = test_dialog.get_content_area()
our_content_area.pack_start(sub_box, True, True, 1)

def add_custom_button(icon_name, container, action):
  newbutton = GimpUi.Button.new_from_icon_name(icon_name, 1)
  newbutton.connect("clicked", action)
  newbutton.set_halign(1)
  newbutton.set_valign(1)
  container.pack_start(newbutton, False, False, 2)
  return newbutton

def add_standard_label(container, name = f"A standard Label"):
  l = Gtk.Label.new(name)
  container.pack_start(l, True, True, 2)
  return l

def generic_on_click(button):
  print(f"pressed {button.get_name()}")

def another_on_click(button):
  print("This is a different method")


# [GimpUi.ICON_CHAR_PICKER, GimpUi.ICON_CLOSE, GimpUi.ICON_CLOSE_ALL, GimpUi.ICON_COLOR_PICK_FROM_SCREEN]
for elem in [GimpUi.ICON_CAP_BUTT, GimpUi.ICON_CAP_ROUND, GimpUi.ICON_CAP_SQUARE, GimpUi.ICON_CENTER]:
  add_custom_button(elem, sub_box, generic_on_click)

for elem in [GimpUi.ICON_CHAR_PICKER, GimpUi.ICON_CLOSE, GimpUi.ICON_CLOSE_ALL, GimpUi.ICON_COLOR_PICK_FROM_SCREEN]:
  add_custom_button(elem, sub_box, generic_on_click)

label = add_standard_label(sub_box)

#Sì! Lo centra
sub_box.set_center_widget(label)
sub_box.reorder_child(label, 3)

our_content_area.show()
test_dialog.show_all()

#print("LABEL IDX", sub_box.get_children().index(label))
#test_dialog.destroy()


# Gtk.PackType.END
# for idx, w in enumerate(sub_box.get_children()):
#   expand, fill, padding, pack_type = sub_box.query_child_packing(w)
#   print(expand, fill, padding, pack_type, w.__class__.__name__)
#   if w.__class__.__name__ == "Label":
#     must_move=True
#   if must_move:
#     print(f"Moving [{idx}]...")
#     print("Before", sub_box.query_child_packing(w)[3])
#     sub_box.set_child_packing(w, expand, fill, padding, Gtk.PackType.END)
#     print("AFTER", sub_box.query_child_packing(w)[3])


#test_dialog.destroy()

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp

def salva_dati_layer(layer, lista_interi):
    # Converte [300, 150, 10] -> "300 150 10"
    stringa_dati = " ".join(map(str, lista_interi))
    
    # Crea il parassita. 
    # In GIMP 3, i dati devono essere passati come bytes o GLib.Bytes
    dati_bytes = stringa_dati.encode('utf-8')
    new_parasite = Gimp.Parasite.new("mio_gioco_dati", Gimp.PARASITE_PERSISTENT, dati_bytes)
    
    layer.attach_parasite(new_parasite)

def leggi_dati_layer(layer):
    parasite = layer.get_parasite("mio_gioco_dati")
    if not parasite:
        return []

    # 1. Ottieni i byte e decodificali in stringa "300 150 10"
    raw_data = parasite.get_data()
    stringa_dati = bytes(raw_data).decode('utf-8')
    
    # 2. Trasforma la stringa in una lista di interi [300, 150, 10]
    try:
        lista_interi = [int(n) for n in stringa_dati.split()]
        return lista_interi
    except ValueError:
        return []
'''
