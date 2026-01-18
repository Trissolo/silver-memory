import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
        self.set_name("az")
        self.add_button("_Done (Close)", Gtk.ResponseType.CANCEL)
        self.connect("destroy", self._on_destroy)
        #self.initialize_internal_stuff()
        self.current_sel = None
        self._uff_arr = []
        self.core_stuff = []
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
        
        button_skip = temp_as.get_children()[2].get_children()[1]
        button_skip.connect('clicked', self.paras_skip)
        print(f"{button_skip=}")


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
        #vars
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
        self._uff_arr = self.current_sel = self._json_properties_with_size = None 
        #self.remove_image_references()
    def greet(self):
        print(f"Hi from {self.get_name()} 😎!")
    def bind_widgets(self):
        self.get_mainbar_box().get_children()[0].connect("clicked", self.clicked_update_layer)
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
    def on_active_row(self, liststore, row_idx, colu):
        liststore.get_selection().unselect_all()
        print("liststore is self.get_treeview()?", liststore is self.get_treeview())
        store = liststore.get_model()
        #store[row_idx][1] = letters[randint(0, 25)]*4
        #store[row_idx][2] = letters[randint(0, 25)]*4
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
        self.get_mainbar_box().get_children()[1].set_text(self.layer.get_name())
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
        
    def paras_kind(self, button):
        prop, size, wid = self.unpack_current_sel()
        print(f"Attaching --{prop}: [{button.key}] ({wid.source[button.key]})")
        self.attach_prop_parasite(prop, [button.key])
        print(f"🇿🇼 The parasite contains {self.ary_from_parasite_name(prop)}")
    def paras_overname(self, listbox, row):
        print(f"Hovernames [{row.idx}]")#listbox, row)
        prop, size, wid = self.unpack_current_sel()
        #print(f"Attaching --{prop}: [{button.key}] ({wid.source[button.key]})")
        self.attach_prop_parasite(prop, [row.idx])
    def paras_vars(self, listbox, row):
        prop, size, wid = self.unpack_current_sel()
        #print(f"Vars: [{wid.get_kind_from_child()}, {row.idx}]\nReq. length: {size}")
        temp_ary = [wid.get_kind_from_child(), row.idx]
        #print(f"🍇Vars parasite: '{prop}' - {temp_ary} - {type(temp_ary)}, {temp_ary=}")
        if size == 2:
            self.attach_prop_parasite(prop, temp_ary)
        else:
            temp_ary.append(None)
            self._uff_arr.clear()
            [self._uff_arr.append(x) for x in temp_ary]
            print(f"{self._uff_arr=}")
            
            #show spinbutton
            
        #print(f"MA FUNZIONA? 🇿🇼 The parasite contains {self.ary_from_parasite_name(prop)=}")
    def paras_skip(self, button):
        prop, size, wid = self.unpack_current_sel()
        print(f"Skip. Oth: {button.get_parent().get_children()=}")
        spinbutton = button.get_parent().get_children()[0]
        self._uff_arr[2] = spinbutton.get_value_as_int()
        self.attach_prop_parasite(prop, self._uff_arr)
    def paras_nointeraction(self, button):
        prop, size, wid = self.unpack_current_sel()
        #print(f"Attaching --{prop}: [{button.key}] ({wid.source[button.key]})")
        self.attach_prop_parasite(prop, [button.key])


    # Current .xcf stuff
    def provide_image(self, image):
        self.image = image
        self.layer = None
        self.update_layer()
    def update_layer(self):
        self.layer = self.image.get_selected_layers()[0]
        print(f"Layer: {self.layer.get_name()}")
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
        #print(f"String bytes_as_string: {bytes_as_string} ({type(bytes_as_string)})")
        test_res = [int(x) for x in bytes_as_string.split(" ")]
        #print(f"Returning: {test_res=}, Type: {type(test_res)}")
        return test_res
        #return [int(x) for x in bytes_as_string.split(" ") if print(f"x={x}") == None]
    def get_parasite_from_propstring(self, prop_string):
        #print(f"Getting parasite for prop {prop_string=}", self.layer.get_parasite(prop_string))
        return self.layer.get_parasite(prop_string)
    def remove_prop_parasite(self, prop_string):
        if self.has_parasite(prop_string): #prop_string in self.layer.get_parasite_list(): #old_parasite:
            self.layer.detach_parasite(prop_string)
    def has_parasite(self, prop_string):
        return prop_string in self.layer.get_parasite_list()
    def attach_prop_parasite(self, prop_string, ary):
        print(f"Ary to attach: {ary=} | type: {type(ary)}")
        self.remove_prop_parasite(prop_string)
        self.layer.attach_parasite(Gimp.Parasite.new(prop_string, 1, self.ary_to_bytes(ary)))
    def ary_from_parasite_name(self, prop_string):
        if not self.has_parasite(prop_string):
            print(f"⚠️ \nNo parasite with property '{prop_string}' in the current layer ({self.layer.get_name()})")
        else:
            print(f"ary_from_para for PROP '{prop_string}': {self.get_parasite_from_propstring(prop_string)=}")
            return self.parasite_data_to_ary(self.get_parasite_from_propstring(prop_string))
