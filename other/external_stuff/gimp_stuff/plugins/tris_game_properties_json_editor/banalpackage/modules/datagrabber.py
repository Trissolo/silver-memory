class DataGrabber():
    def _populate_from_files(self):
        import json
        from gi.repository import GLib
        directory_separator = GLib.DIR_SEPARATOR_S
        filepath = GLib.path_get_dirname(__file__)
        wanted = "other"
        basedir = f"{filepath[0:filepath.index(wanted)]}src/game/gamedata"
        #read all json files:
        res = []
        for filename in [*["Bool", "Crumble", "Nibble", "Byte"], "hovernames"]:
            with open(f"{basedir}{directory_separator}{filename}.json".lower()) as json_file:
                res.append(json.load(json_file))
        # PSEUDO INTERNAL CONSTS
        #print(*res, sep="AZAZAZAZAZ\n")
        return res
        #original code before the "return" above:
        #self.raw_hovernames = res.pop()
        #self.raw_vars = res
        #print("res", res, sep="\n")
        #print("raw_hovernames", self.raw_hovernames, sep="\n")
    def make_summary(self):
        '''
        store = Gtk.ListStore.new([str, str, str, str, str])
        store.append(['Mario', 'Rossi', "#000", "#888", '#999']) 
        store.append(['Germy', 'Moscon', "#000", '#f44', '#44f'])

        tw = Gtk.TreeView.new()
        tw.set_model(store) #(model=store)
        print(tw)

        cell_a = Gtk.CellRendererText.new()

        column_one = Gtk.TreeViewColumn("Header_Nome", cell_a, text=0, foreground=2, background=3) #, underline=4, size=5)
        column_one.set_name("Column_one")
        column_two = Gtk.TreeViewColumn("Header_Cognome", cell_a, text=1, foreground=2, background=4)
        column_two.set_name("Column_two")
        tw.append_column(column_one)
        tw.append_column(column_two)

        self.div.pack_start(tw, False, False, 1)
        self.dialog.show_all()

        tw.get_selection().unselect_all()
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active)
        return tw
        '''
    def initialize_internal_stuff(self):
        self.ntr_thingProps = ["kind", "hoverName", "suffix", "skipCond", "animation", "noInteraction"]
        self.ntr_vars_kinds = ["Bool", "Crumble", "Nibble", "Byte"]

        #hmmm
        #['Background', 'Ridiculously Faraway', 'Trigger Area', 'Covered', 'Always Back', 'Depth Sorted', 'Foreground']
        #[-5, 0, 1, 2, 3, 4, 800]
        self.ntr_depth = {-5: 'Background', 0: 'Ridiculously Faraway', 1: 'Trigger Area', 2: 'Covered', 3: 'Always Back', 4: 'Depth Sorted', 800: 'Foreground'} #{'Background': -5,'Ridiculously Faraway': 0,'Trigger Area': 1,'Covered': 2,'Always Back': 3,'Depth Sorted': 4,'Foreground': 800}
        self.raw_hovernames = None
        self.raw_vars = None
        self._populate_from_files()

        debu = []
        for elem in dir(self):
            if elem.startswith("raw") or elem.startswith("ntr"):
                debu.append(elem)
        print(f"INTERNAL DATA: {debu}")


    '''
        _base_dir = ""
        vars = []
        props = None

        @classmethod
        def _set_basedir(cls):
            import sys
            cls._base_dir = f"{sys.path[0]}/trispackage/gamedata/"

        @classmethod
        def _load_local_file(cls, filename, subfolder =""):
            import json
            with open(f"{cls._base_dir}{subfolder}{filename}.json") as json_file:
                return json.load(json_file)
    '''