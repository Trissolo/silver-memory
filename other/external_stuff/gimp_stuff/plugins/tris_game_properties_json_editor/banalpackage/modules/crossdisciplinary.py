class CrossDisciplinary():
    def _iu_message(self):
        print("This is from CrossDisciplinary class!")
    @staticmethod
    def integer_to_binary(x = 0, prepend_zeroes = True):
        resulting_string = f'{x:0>8b}' if prepend_zeroes else f'{x:b}'
        print(resulting_string)
        return resulting_string
    @staticmethod
    def _gather_vcoords(kind, index):
        if kind > 3:
            raise ValueError(f"kind ({kind}) is too big!")
        return (index << 2) | kind
    @staticmethod
    def _disassemble_vcoords(vcoord):
        return [vcoord & 3, vcoord >> 2]
    @classmethod
    def manage_array(cls, ary):
        l = len(ary)
        if l == 1:
            return ary[0]
        vcoords = CrossDisciplinary._gather_vcoords(ary[0], ary[1])
        if l == 2:
            return vcoords
        elif l == 3:
            return [vcoords, ary[2]]
        else:
            raise ValueError(f"Array length ({l}) out of range!")
    @classmethod
    def add_button(cls):
        print("Adding button")
    @staticmethod
    def put_polys_in_order(source_dict):
        res = {}
        for key, val in source_dict.items():
            first_char = key[0]
            
            if first_char not in res:
                res[first_char] = []
            
            # If the key is exactly the single character (e.g., "a"), 
            # insert it at the front. Otherwise, append to the end.
            if key == first_char:
                res[first_char].insert(0, val)
            else:
                res[first_char].append(val)
    
        # sorted_polys = put_in_order(obj)
        # print(json.dumps(list(sorted_polys.values()), indent=4))
        # print(json.dumps(sorted_polys, indent=4), f"\npoly_params: {json.dumps(list(sorted_polys.values()), indent=4)}")
        return res
    


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
    nuovo_parassita = Gimp.Parasite.new("mio_gioco_dati", Gimp.PARASITE_PERSISTENT, dati_bytes)
    
    layer.attach_parasite(nuovo_parassita)

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
