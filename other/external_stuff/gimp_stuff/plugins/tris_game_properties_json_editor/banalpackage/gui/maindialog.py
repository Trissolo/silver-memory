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
        #print("Prima di bind_widgets:", *self.get_content_area().get_children())
        #for elem in self.get_content_area().get_children():
        #    print(elem.get_name())
        #print("Prima di bind_widgets:", *self.get_content_area().get_children()[2].get_children())
        self.bind_widgets()

        #temp_as = self.get_content_area().get_children()[0]
        
        #for w in temp_as:
        #    print(w.get_name())

        #Kinds
        temp_as = self.core_stuff[0]['wid']
        for button in temp_as.get_children(): #.get_children()[0].get_children():
            #print(button.get_name())
            button.connect('clicked', self.paras_kind)
        
        #Name on mouse hover
        temp_as = self.core_stuff[1]['wid']
        #print("🐢NAME🌍", temp_as.get_children()[1].get_child().get_child().get_name())
        temp_as.get_children()[1].get_child().get_child().connect('row-activated', self.paras_overname)
        #print("🌍", temp_as.get_name(), *temp_as.get_children()[0].get_children(), sep="\n")

        #VARS!
        temp_as = self.core_stuff[2]['wid']
        vars_wid = temp_as.get_children()[1].get_children()
        for idx, single in enumerate(vars_wid):
            list = single.get_children()[1].get_child().get_child()
            #list.idx = idx
            list.connect('row-activated', self.paras_vars)
            #print("🐢VARS🌍", )#[1].get_child().get_child().get_name())
        #print("First_LEV:", *temp_as, len(temp_as))
        #print("Widgets in MainBar:", *self.get_content_area().get_children()[0].get_children(), sep="\n")
        '''
        print("Follia:")
        from banalpackage.modules.follia import WidgetTree
        q = self
        print(WidgetTree(q).generate())
        '''
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
        var_size = { "kind": 1, "hoverName": 1, "suffix": 2, "skipCond": 3} #, "animation": 1, "noInteraction": 1 }
        core_stuff = self.core_stuff = []
        stack = self.get_stack()
        
        for prop, size in var_size.items():
            #print(f"PROP: {prop} --> Val: {size}")
            core_stuff.append({'prop': prop, 'size': size})
        
        #kind:
        wkind = VersatileBox().make_kind_selector(source_depths)
        core_stuff[0]['wid'] = wkind
        stack.add_named(wkind, "kind")

        names = SingleChooser(source_hnames)
        core_stuff[1]['wid'] = names
        stack.add_named(names, "names")

        vars_wid = MultiChooser(source_variables, source_varcat)
        core_stuff[2]['wid'] = vars_wid
        core_stuff[3]['wid'] = vars_wid
        stack.add_named(vars_wid, "vars")

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
        self.current_sel = None
        #self.remove_image_references()
    def greet(self):
        print(f"Hi from {self.get_name()} 😎!")
    def bind_widgets(self):
        self.get_mainbar_box().get_children()[0].connect("clicked", self.clicked_update_layer)
    def get_mainbar_box(self):
        return self.get_content_area().get_children()[0]
    def get_stack(self):
        print("Stack PAth", self.get_content_area().get_children()[2].get_children()[1].get_path())
        return self.get_content_area().get_children()[2].get_children()[1]
    def on_active_row(self, treemodel, row_idx, colu):
        treemodel.get_selection().unselect_all()
        store = treemodel.get_model()
        #store[row_idx][1] = letters[randint(0, 25)]*4
        #store[row_idx][2] = letters[randint(0, 25)]*4
        first_cell_color = treemodel.get_n_columns()
        other_cells_color = first_cell_color + 1
        for i in range(store.iter_n_children(None)):
            store[i][first_cell_color] = "#777"
            store[i][other_cells_color] = "#666"
        store[row_idx][first_cell_color] = "#770"
        store[row_idx][other_cells_color] = "#270"
        self.current_sel = self.core_stuff[row_idx.get_indices()[0]]
        self.get_stack().set_visible_child(self.current_sel['wid'])


    def aiut(self):
        cont = ['kind', 'hoverName', 'suffix', 'skipCond']# , 'animation', 'noInteraction']
        store = Gtk.ListStore.new([str]*5)
        predef = "---"
        for pname in cont:
            store.append([pname, predef, predef, "#000", "#888"])
            
        #store.append(['Germy', 'Moscon', 'QWQW', '#000', '#f44'])

        tw = Gtk.TreeView.new()
        tw.set_model(store) #(model=store)
        #print(tw)

        cell = Gtk.CellRendererText.new()

        #props = ['kind', 'hoverName', 'suffix', 'skipCond']# , 'animation', 'noInteraction']
        col_names = ["Prop", "Readable", "Effective"]
        bg_int = len(col_names)
        bg_others = bg_int + 1

        for idx, name in enumerate(col_names):
            col = Gtk.TreeViewColumn(name, cell, text= idx, background= min(bg_int, bg_others))
            tw.append_column(col)
            bg_int += 1
            
        #column_one = Gtk.TreeViewColumn("Header_Nome", cell_a, text=0, foreground=2, background=3) #, underline=4, size=5)
        #column_one.set_name("Column_one")
        #column_two = Gtk.TreeViewColumn("Header_Cognome", cell_a, text=1, foreground=2, background=4)
        #column_two.set_name("Column_two")
        #tw.append_column(column_one)
        #tw.append_column(column_two)
        self.get_content_area().get_children()[2].pack_start(tw, False, False, 1)
        #self.get_content_area().get_children()[1].pack_start(tw, False, False, 1)
        tw.show()

        tw.get_selection().unselect_all()
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
    def unpack_current_sel(self):
        return self.current_sel["prop"], self.current_sel["size"], self.current_sel["wid"]
    def clicked_update_layer(self, button):
        self.update_layer()
        self.get_mainbar_box().get_children()[1].set_text(self.layer.get_name())
    def paras_kind(self, button):
        prop, size, wid = self.unpack_current_sel()
        print(f"Attaching --{prop}: [{button.key}] ({wid.source[button.key]})")
        #prop, size, wid = self.unpack_current_sel()
        #print(prop, size, wid)
    def paras_overname(self, listbox, row):
        print(f"Hovernames [{row.idx}]")#listbox, row)
    def paras_vars(self, listbox, row):
        prop, size, wid = self.unpack_current_sel()
        print(f"Vars: [{wid.get_kind_from_child()}, {row.idx}]\nReq. length: {size}")
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
    def para_data_to_ary(self, data):
        '''Convert a <bytes array> to a compact int array'''
        bytes_as_string = str(object=bytes(data), encoding='ascii')
        return [int(x) for x in bytes_as_string.split(" ")]
    def get_prop_parasite(self, prop_string):
        return self.layer.get_parasite(prop_string)
    def remove_prop_parasite(self, prop_string):
        if prop_string in self.layer.get_parasite_list(): #old_parasite:
            self.layer.detach_parasite(prop_string)
    def has_parasite(self, prop_string):
        return prop_string in self.layer.get_parasite_list()
