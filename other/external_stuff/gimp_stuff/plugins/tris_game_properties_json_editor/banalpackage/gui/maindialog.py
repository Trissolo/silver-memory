import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


'''
class MainDialog():
    def __init__(self):
        print("This is the Main Dialog!")

class Altr():
    def conf_a(self, param= "Param di A"):
        print(f"Setting param for Altr Class: {param}")
        self.param = param
'''
from ..modules.datagrabber import DataGrabber
from .singlechooser import SingleChooser
from .versatilebox import VersatileBox
from .multichooser import MultiChooser
from .binarybox import BinaryBox

class MainDialog(GimpUi.Dialog, DataGrabber):
    def __new__(cls):
        print("Creating MainDialog")
        gag = super(MainDialog, cls).__new__(cls)
        return gag
    def __init__(self, *args):
        super().__init__(*args)
        self.set_title("Tris JSON generator")
        self.set_keep_above(True)
        self.set_name("az")
        self.add_button("_Done (Close)", Gtk.ResponseType.CANCEL)
        #common stuff
        self.current_sel = None
        self._uff_arr = []
        self.core_stuff = []
        self.rscript = "{}"
        self.connect("destroy", self._on_destroy)
        self._json_properties_with_size = { "kind": 1, "hoverName": 1, "suffix": 2, "skipCond": 3, "noInteraction": 1} #, "animation": 1 }
        #MAINBAR:
        self.get_content_area().pack_start(VersatileBox().make_main_bar(), False, False, 2)
        #Preview:
        self.get_content_area().pack_start(VersatileBox().make_preview_bar(), True, False, 2)
        #CONT
        imp_box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        imp_box.set_name("Imporatnt Box")
        self.get_content_area().pack_start(imp_box, True, True, 2)
        imp_box.pack_end(Gtk.Stack.new(), True, True, 2)
        self.aiut()
        self.build_main_dictionary()
        self.bind_widgets()

        #Kinds
        temp_as = self.core_stuff[0]['wid']
        for button in temp_as.get_children():
            button.connect('clicked', self.paras_kind)
        
        #Name on mouse hover
        temp_as = self.core_stuff[1]['wid']
        temp_as.get_children()[1].get_child().get_child().connect('row-activated', self.paras_overname)

        #VARS!
        temp_as = self.core_stuff[2]['wid']
        vars_wid = temp_as.get_children()[1].get_children()
        for idx, single in enumerate(vars_wid):
            list = single.get_children()[1].get_child().get_child()
            #list.idx = idx
            list.connect('row-activated', self.paras_vars)
        #supplementary vars action 
        button_skip = temp_as.get_children()[2].get_children()[1]
        button_skip.connect('clicked', self.paras_skip)
        #print(f"{button_skip=}")


        #print(f"🐢Current🌍 {temp_as} {temp_as.get_children()[2].get_children()[1]}")
        '''
        print("Follia:")
        from banalpackage.modules.follia import WidgetTree
        q = self
        print(WidgetTree(q).generate())
        '''
        #self.get_left_liststore()
        # Test:
        #check = self.get_content_area()
        #Gtk.Orientation.HORIZONTAL: 0
        #Gtk.Orientation.VERTICAL: 1
        #check.set_valign(Gtk.Align.FILL)
        #print(f"ORIENTATION: {check.get_orientation()}\n get_spacing: {check.get_spacing()}")
        #print(f"get_vexpand: {check.get_vexpand()}\nget_hexpand: {check.get_hexpand()}")
    def build_main_dictionary(self):
        #print("🎅TIPO:", self.get_content_area().get_children()[1].get_children()[0].get_name()) #[1].get_children()[0])
        source_depths = {-5: 'Background', 0: 'Ridiculously Faraway', 1: 'Trigger Area', 2: 'Covered', 3: 'Always Back', 4: 'Depth Sorted', 800: 'Foreground'}
        source_varcat = ["Bool", "Crumble", "Nibble", "Byte"]
        source_variables = self._populate_from_files()
        source_hnames = source_variables.pop()
        #json_props_ori = ["kind", "hoverName", "suffix", "skipCond", "animation", "noInteraction"]
        #var_size_ori = { "kind": 1, "hoverName": 1, "suffix": 2, "skipCond": 3, "animation": 1, "noInteraction": 1 }
        var_size = self._json_properties_with_size #{ "kind": 1, "hoverName": 1, "suffix": 2, "skipCond": 3} #, "animation": 1, "noInteraction": 1 }
        core_stuff = self.core_stuff
        stack = self.get_stack()
        
        for prop, size in var_size.items():
            #print(f"PROP: {prop} --> Val: {size}")
            core_stuff.append({'prop': prop, 'size': size})
        
        #kind:
        wkind = VersatileBox().make_kind_selector(source_depths)
        core_stuff[0]['wid'] = wkind
        stack.add_named(wkind, "kind")
        #name:
        names = SingleChooser(source_hnames)
        core_stuff[1]['wid'] = names
        stack.add_named(names, "names")
        #vars:
        vars_wid = MultiChooser(source_variables, source_varcat)
        core_stuff[2]['wid'] = vars_wid
        core_stuff[3]['wid'] = vars_wid
        stack.add_named(vars_wid, "vars")
 
        #no interaction
        no_interaction_widget = BinaryBox()
        core_stuff[4]['wid'] = no_interaction_widget
        no_interaction_widget.get_default_button().connect("clicked", self.paras_nointeraction)
        stack.add_named(no_interaction_widget, "nointeraction")
        
        # Fake widget
        fakew = Gtk.Label.new("Select the prop on the left")
        stack.add_named(fakew, "fake")
        stack.get_parent().show_all()
        stack.set_visible_child(fakew)
    def _on_destroy(self, widget):
        print(f"ON DESTROY CALLED!\n:)" )
        self.remove_image_references()
        for elem in self.core_stuff:
            elem.clear()
        self.core_stuff.clear()      
        self._uff_arr.clear()
        self._json_properties_with_size.clear()
        self._uff_arr = self.current_sel = self._json_properties_with_size = self.rscript = None 
    def greet(self):
        print(f"Hi from {self.get_name()} 😎!")
    def bind_widgets(self):
        #main bar button: update layers
        self.get_mainbar_box().get_children()[0].connect("clicked", self.clicked_update_layer)
        self.get_mainbar_box().get_children()[1].connect("clicked", self.expensive_next)
        self.get_mainbar_box().get_children()[2].connect("clicked", self.expensive_next)
        #main bar button: generate JSON
        self.get_mainbar_box().get_children()[4].connect("clicked", self.generate_json)
        self.get_mainbar_box().get_children()[5].connect("clicked", self.get_polygons)
        self.get_mainbar_box().get_children()[6].connect("clicked", self.show_rscript)
        #button_remove_existing_parasite:
        self.get_content_area().get_children()[1].get_children()[0].connect('clicked', self.gui_delete_parasite)
    def get_mainbar_box(self):
        return self.get_content_area().get_children()[0]
    def get_left_liststore(self):
        #self.greet()
        return self.get_content_area().get_children()[2].get_children()[0].get_model()
    def get_treeview(self):
         return self.get_content_area().get_children()[2].get_children()[0]
    def get_stack(self):
        #print("Stack PAth", self.get_content_area().get_children()[2].get_children()[1].get_path())
        return self.get_content_area().get_children()[2].get_children()[1]
    def gui_delete_parasite(self, button):
        if self.current_sel is not None:
            self.remove_prop_parasite(self.current_sel.get('prop'))
            self.refresh_summary()
    def on_active_row(self, liststore, row_idx, colu):
        liststore.get_selection().unselect_all()
        #print("liststore is self.get_treeview()?", liststore is self.get_treeview())
        store = liststore.get_model()
        first_cell_color = liststore.get_n_columns()
        other_cells_color = first_cell_color + 1
        self.refresh_summary(liststore)
        #for i in range(store.iter_n_children(None)):
        #    store[i][first_cell_color] = "#777"
        #    store[i][other_cells_color] = "#666"
        store[row_idx][first_cell_color] = "#447"
        store[row_idx][other_cells_color] = "#336"
        self.current_sel = self.core_stuff[row_idx.get_indices()[0]]
        self.get_stack().set_visible_child(self.current_sel['wid'])
        #vars adjustement
        print(f"🍕{self.current_sel['wid'].get_name()}")
    def unselect_rows(self):
            self.current_sel = None
            self.get_stack().set_visible_child_name("fake")

    def aiut(self):
        store = Gtk.ListStore.new([str]*5)
        predef = "---"
        for pname in self._json_properties_with_size.keys():
            store.append([pname, predef, predef, "#000", "#888"])
            
        tw = Gtk.TreeView.new()
        tw.set_model(store) #(model=store)

        cell = Gtk.CellRendererText.new()

        col_names = ["Prop", "Readable", "Effective"]
        bg_int = len(col_names)
        bg_others = bg_int + 1

        for idx, name in enumerate(col_names):
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=min(bg_int, bg_others))
            tw.append_column(col)
            bg_int += 1
        self.get_content_area().get_children()[2].pack_start(tw, False, False, 1)
        tw.show()

        tw.get_selection().unselect_all()
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
    def unpack_current_sel(self, param = None):
        if param is None:
            param = self.current_sel
        return param["prop"], param["size"], param["wid"]
    def clicked_update_layer(self, button):
        self.update_layer()
        self.set_internal_message(self.layer.get_name())
        self.refresh_summary()
        self.unselect_rows()
    def refresh_summary(self, treeview = None):
        if treeview is None:
            treeview = self.get_treeview()
        #print("🍰 Exploring treeview")
        #print(treeview.get_n_columns())
        color_prop_colu = treeview.get_n_columns()
        other_color = color_prop_colu + 1

        store = treeview.get_model() #self.get_left_liststore()
        for idx, element in enumerate(self.core_stuff):
            prop, size, wid = self.unpack_current_sel(element)
            if self.has_parasite(prop):
                parasite = self.get_parasite_from_propstring(prop)
                ary = self.parasite_data_to_ary(parasite)
                #print(f"PROP: {prop} 🍒ary: {ary}")
                store[idx][1] = wid.get_readable(ary, size)
                store[idx][2] = f"{ary}"
                store[idx][color_prop_colu] ="#471"
                store[idx][other_color] = "#260"
            else:
                store[idx][1] = "---"
                store[idx][2] = "---"
                store[idx][color_prop_colu] = store[idx][other_color] = "#444"
                #store[idx][other_color] = "#666"
        
        #prop, size, wid = self.clicked_update_layer()
        '''
        para_names_list = self.layer.get_parasite_list()
        print(f"🍑 Parasite list:")
        print(f"{para_names_list=}")
        for pname in para_names_list:
            parasite = self.layer.get_parasite(pname)
            print(f"🍊 {pname=}", parasite.get_data())
            print("🍒First D (parasite_data_to_ary):", self.parasite_data_to_ary(parasite), type(self.parasite_data_to_ary(parasite)))
        '''
    def manifest_changed_row(self):
        prop, size, wid = self.unpack_current_sel()
        parasite = self.get_parasite_from_propstring(prop)
        ary = self.parasite_data_to_ary(parasite)
        row = self.get_treeview().get_model()[self.core_stuff.index(self.current_sel)]
        row[1] = wid.get_readable(ary, size)
        row[2] = f"{ary}"
    def paras_kind(self, button):
        prop, size, wid = self.unpack_current_sel()
        res = [button.key]
        #print(f"Attaching --{prop}: [{button.key}] ({wid.source[button.key]})")
        self.attach_prop_parasite(prop, [button.key])
        #print(f"🇿🇼 The parasite contains {self.ary_from_parasite_name(prop)}")
        self.manifest_changed_row()
    def paras_overname(self, listbox, row):
        print(f"Hovernames [{row.idx}]")#listbox, row)
        prop, size, wid = self.unpack_current_sel()
        res = [row.idx]
        self.attach_prop_parasite(prop, res)
        self.manifest_changed_row()
    def paras_vars(self, listbox, row):
        prop, size, wid = self.unpack_current_sel()
        temp_ary = [wid.get_kind_from_child(), row.idx]
        if size == 2:
            self.attach_prop_parasite(prop, temp_ary)
            self.manifest_changed_row()
        else:
            temp_ary.append(None)
            self._uff_arr.clear()
            [self._uff_arr.append(x) for x in temp_ary]
            print(f"{self._uff_arr=}")
            
    def paras_skip(self, button):
        prop, size, wid = self.unpack_current_sel()
        spinbutton = button.get_parent().get_children()[0]
        print(f"UFFARRAY: {self._uff_arr} Skip. Oth: {button.get_parent().get_children()=}")
        self._uff_arr[2] = spinbutton.get_value_as_int()
        self.attach_prop_parasite(prop, self._uff_arr)
        self.manifest_changed_row()
    def paras_nointeraction(self, button):
        prop, size, wid = self.unpack_current_sel()
        res = [button.key]
        #print(f"Attaching --{prop}: [{button.key}] ({wid.source[button.key]})")
        self.attach_prop_parasite(prop, res)
        self.manifest_changed_row()

    # Current .xcf stuff
    def provide_image(self, image):
        self.image = image
        self.layer = None
        self.update_layer()
    def update_layer(self):
        self.layer = self.image.get_selected_layers()[0]
        #print(f"Layer: {self.layer.get_name()}")
    def remove_image_references(self):
        self.image = None
        self.layer = None
        print("No more reference to .xcf file")
    
    # PARASITE STUFF
    def ary_to_bytes(self, data):
        '''Encode an array of any integer in a <bytes array> '''
        return (" ".join([str(el) for el in data])).encode('ascii')
    def parasite_data_to_ary(self, parasite):
        '''Convert a <bytes array> to a compact int array'''
        bytes_as_string = str(object=bytes(parasite.get_data()), encoding='ascii')
        test_res = [int(x) for x in bytes_as_string.split(" ")]
        return test_res
    def get_parasite_from_propstring(self, prop_string):
        #print(f"Getting parasite for prop {prop_string=}", self.layer.get_parasite(prop_string))
        return self.layer.get_parasite(prop_string)
    def remove_prop_parasite(self, prop_string):
        if self.has_parasite(prop_string): #prop_string in self.layer.get_parasite_list(): #old_parasite:
            self.layer.detach_parasite(prop_string)
    def has_parasite(self, prop_string):
        return prop_string in self.layer.get_parasite_list()
    def attach_prop_parasite(self, prop_string, ary):
        self.remove_prop_parasite(prop_string)
        self.layer.attach_parasite(Gimp.Parasite.new(prop_string, 1, self.ary_to_bytes(ary)))
    def ary_from_parasite_name(self, prop_string):
        if not self.has_parasite(prop_string):
            print(f"⚠️ \nNo parasite with property '{prop_string}' in the current layer ({self.layer.get_name()})")
        else:
            print(f"ary_from_para for PROP '{prop_string}': {self.get_parasite_from_propstring(prop_string)=}")
            return self.parasite_data_to_ary(self.get_parasite_from_propstring(prop_string))
    # JSON functions:
    @staticmethod
    def manage_area(layer, obj):
        #print(f"Area = {layer.get_name()}")
        _succ, x, y = layer.get_offsets()
        obj['rect'] = [x, y, layer.get_width(), layer.get_height()]
    def manage_coords(layer, obj, kind):
        _succ, x, y = layer.get_offsets()
        if kind == 4:
            obj["x"] = layer.get_width() // 2 + x
            obj["y"] = y + layer.get_height()
        else:
            obj["x"] = x
            obj["y"] = y
    def generate_json(self, button):
        import json
        #['kind', 'hoverName', 'suffix', 'skipCond', 'noInteraction']
        #  0       1            2         3           4
        possible_properties = [*self._json_properties_with_size.keys()]
        #message:
        print(f"Defining json... {possible_properties} t:{type(possible_properties)}")
        #return list
        things_array = []
        real_res = {'things': things_array}
        #iteration:
        for layer in (l for l in self.image.get_layers() if l.get_visible()):
            parasites = layer.get_parasite_list()
            #print(f"{layer.get_name()}")
            if possible_properties[0] in parasites:
                curr_kind = self.parasite_data_to_ary(layer.get_parasite(possible_properties[0]))[0]
                if curr_kind == -5:
                    real_res['bg'] = layer.get_name()
                    continue
                obj = {'kind': curr_kind}
                things_array.append(obj)
                #hoverName
                if possible_properties[1] in parasites:
                    obj[possible_properties[1]] = self.parasite_data_to_ary(layer.get_parasite(possible_properties[1]))[0]
                #skipCond
                if possible_properties[3] in parasites:
                    obj[possible_properties[3]] = self.parasite_data_to_ary(layer.get_parasite(possible_properties[3]))
                # Trigger area
                if curr_kind == 1:
                    type(self).manage_area(layer, obj)
                    continue
                obj["frame"] = layer.get_name().rstrip("0123456789")
                #suffix
                if obj["frame"] != layer.get_name() and possible_properties[2] in parasites:
                    obj[possible_properties[2]] = self.parasite_data_to_ary(layer.get_parasite(possible_properties[2]))
                type(self).manage_coords(layer, obj, curr_kind)

            else:
                #print("No kind")
                continue
        #real_res["basescript"] = self.assemble_basescript(things_array)
        self.rscript = self.assemble_basescript(real_res)
        print("json Done!")
        self.copy_text_to_clipboard(json.dumps(real_res, indent = None))
        self.set_internal_message()
        #Gimp.message_set_handler(Gimp.MessageHandlerType.MESSAGE_BOX) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2
        #Gimp.message(final)#json.dumps(final, indent=None))#things_array, indent = None))
        #Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE)
    def get_polygons(self, button):
        import json
        polys = {}
        for path in self.image.get_paths():
            if len(path.get_strokes()) == 0:
                continue
            res = []
            for curr_stroke in path.get_strokes():
                bp = path.stroke_get_points(curr_stroke).controlpoints
                res.append(" ".join([str(int(x)) for pair in zip(bp[0::6], bp[1::6]) for x in pair]))
            polys[path.get_name()] = res[0] if len(res) == 1 else res
        self.copy_text_to_clipboard(json.dumps(polys, indent = 1))
        self.set_internal_message("🔹Paths copied to ClipBoard")
    def set_internal_message(self, message = "🟢 JSON copied to Clipboard"):
        self.get_mainbar_box().get_children()[3].set_text(message)
    def copy_text_to_clipboard(self, text = "Nothing"):
        tempcl = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        tempcl.set_text(text, -1)
    def expensive_next(self, button):
        #print(f":( Expensive: {button.dir}")
        layers = self.image.get_layers()
        if not self.layer or len(layers) < 2:
            #print("Skipping :(")
            return
        next_idx = layers.index(self.layer) + button.dir
        self.image.set_selected_layers([layers[0] if next_idx == len(layers) else layers[next_idx]])
        self.clicked_update_layer(None)
    def assemble_basescript(self, real_res):
        res = ""
        nl = "\n"
        sp = " "
        frame_prop = "frame"
        gen_start = f"{nl}{sp*4}static "


        for idx, elem in enumerate(real_res.get('things')):
            comment = elem[frame_prop] if frame_prop in elem else "AREA"
            res+= f"{sp*4}// {comment}{gen_start}{idx}(thing){{console.log(thing.frame.name);}}{nl*2}"

        return f"export default class rs{self.image.get_name()[4:-4]}{nl}{{{nl}{res}}}\n"
    def show_message(self, message = "Test\ntest"):
        Gimp.message_set_handler(Gimp.MessageHandlerType.MESSAGE_BOX) # MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2
        Gimp.message(message)
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE)
        return self
    def show_rscript(self, button):
        self.copy_text_to_clipboard(self.rscript)
        self.set_internal_message("📜 rscript copyed")
