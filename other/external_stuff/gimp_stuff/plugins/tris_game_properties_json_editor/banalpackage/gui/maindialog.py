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
        #CONT
        imp_box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.get_content_area().pack_start(imp_box, True, True, 2)
        imp_box.pack_end(Gtk.Stack.new(), True, True, 2)
        self.aiut()
        self.build_main_dictionary()
        #TESTING Multi:
        #m = MultiChooser(self.raw_vars, self.ntr_vars_kinds)
        #self.get_content_area().pack_start(m, True, True, 2)
        #Building GUI:
        #self.get_content_area().pack_start(VersatileBox().make_kind_selector(self.ntr_depth), False, False, 2)
        #self.get_content_area().pack_start(SingleChooser(["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei"]), True, True, 2)
        #self.get_content_area().pack_start(SingleChooser(self.raw_hovernames), True, True, 2)
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
            print(f"PROP: {prop} --> Val: {size}")
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




        #print("PARENT:", stack.get_parent())
        stack.get_parent().show_all()
        stack.set_visible_child(core_stuff[0]['wid'])
        

    def _on_destroy(self, widget):
        #a.conf_a("Fare the well!")
        print(f"ON DESTROY CALLED! TEST:{self is widget}\n:)" )
        for elem in self.core_stuff:
            elem.clear()
        self.core_stuff.clear()
        self.current_sel = None
    def greet(self):
        print(f"Hi from {self.get_name()} 😎!")
    def get_stack(self):
        print("getting_ctack", self.get_content_area().get_children()[1].get_children())
        return self.get_content_area().get_children()[1].get_children()[1]
    def on_active_row(self, treemodel, row_idx, colu):
        print(f"TreeView: {treemodel}\nRow[{row_idx}]\nColumn: {colu.get_name()}")
        treemodel.get_selection().unselect_all()
        store = treemodel.get_model()
        #store[row_idx][1] = letters[randint(0, 25)]*4
        #store[row_idx][2] = letters[randint(0, 25)]*4
        #for i, elem in enumerate(treemodel.get_columns()):
        amount = treemodel.get_n_columns()
        for i in range(store.iter_n_children(None)):
            store[i][amount] = "#777"
        store[row_idx][amount] = "#ff0"
        print(row_idx, type(self.core_stuff), row_idx.get_indices()[0] )
        #cu = self.core_stuff[row_idx.get_indices()[0]]
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
        print(tw)

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

        self.get_content_area().get_children()[1].pack_start(tw, False, False, 1)
        tw.show()

        tw.get_selection().unselect_all()
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
