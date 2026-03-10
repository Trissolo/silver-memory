import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .gui_bar_generator import GuiBarGenerator
from ..misc.selectioninfo import SelectionInfo

class InventoryDialog(GimpUi.Dialog, GuiBarGenerator):
    def __init__(self, image, crossroads, *args):
        # First of all
        super().__init__(title="Tris Inventory Generator", *args)

        print(f"Crossroads: {type(crossroads)}")
        
        #0 the Dialog chores:
        self.set_keep_above(True)
        # self.add_buttons( "Done [close]", Gtk.ResponseType.OK)
        self.connect("destroy", self._on_destroy)
        self.set_name("Inv. Dialog")

        #1 Set the Image and Current Layer:
        self.image = image
        self.layer = None

        #2 Populate the Top Bar
        self.generate_top_bar()

        #3 Populate the Middle Bar
        self.generate_middle_bar()

        #4 the core widgets!
        # ...

        #5 Set the Layer!

        # self.update_layer()
        # test:
        for child in self.get_content_area().get_children():
            print(child.get_name())

        #6 Ready!
        self.build_tw()
        self.update_layer()
        self.grab_core_props_game()
        # self.tw_refresh_hard()
        # self.summary_debug()
        # self.generate_json()
        self.load_json_hovernames()
    
    def set_current_prop(self):
        #self.attach_array_to_current_layer()
        return

    def _on_destroy(self, widget):
        self.remove_image_references()
        self._top_label = None
        print("Checking row_info:", self.row_infos[0])
        for elem in self.row_infos:
            elem.clear()
        self.row_infos = self.row_infos.clear()
        print("Inventory plugin destroyed!")
    
    def build_tw(self):
        # self.get_content_area().pack_start(tw, False, False, 1)

        row_infos = self.row_infos = []

        self.curr_sel = None

        properties_size = {
            "kind": 1,
            "hoverName": 1,
            "suffix": 2,
            "skipCond": 3,
            "noInteraction": 1,
            "roomStatus": 2,
            "roomVariable": 2
        }
        column_headers = ["Prop", "Readable", "Effective"]

        print(f"Debug locals so far: {locals()}")

        # attribute mapping

        first_colum_color = len(column_headers)

        other_colums_color = first_colum_color + 1

        print(f"{first_colum_color=}, {other_colums_color=}")

        mytypes = [str] * len(column_headers)

        cell_types = [*mytypes, str, str]

        # the Store/Model!
        store = Gtk.ListStore.new(cell_types)

        # the TreeView
        tw = Gtk.TreeView.new()

        tw.set_model(store)

        # constants AS!
        tw.text_empty = "---"
        tw.color_empty = "#343434"
        tw.color_selected = "#ff0"
        tw.color_set = "#66a"

        # populate the store:
        for idx, (prop, size) in enumerate(properties_size.items()):
            store.append([prop, tw.text_empty, tw.text_empty, tw.color_empty, tw.color_empty])
            row_infos.append(SelectionInfo(prop, size, idx, None))
        
        cell = Gtk.CellRendererText.new()

        for idx, name in enumerate(column_headers):
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=first_colum_color if idx==0 else other_colums_color)
            tw.append_column(col)
        
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
        self.get_content_area().pack_start(tw, False, False, 1)
        tw.show_all()
        self.tw = tw
        

    def on_active_row(self, liststore, row_idx, colu):
        print("On Active Row!")
        index_as_int = row_idx.get_indices()[0]
        liststore.get_selection().unselect_all()
        model = liststore.get_model()
        if self.curr_sel is not None:
            model[self.curr_sel.row_idx][3] = model[self.curr_sel.row_idx][4]
        model[index_as_int][3] = liststore.color_selected
        model[index_as_int][4] = liststore.color_empty
        self.curr_sel = self.row_infos[index_as_int]
        print(f"CurrSel: {self.curr_sel}")
        print(f"Analogies? {index_as_int=} -> {self.curr_sel.row_idx} -*- {model[row_idx][0]=} -> {self.curr_sel.prop} {model[row_idx][0]}")
    
    def tw_refresh_hard(self, tw=None, model=None):
        if tw == None:
            tw = self.tw
            model = tw.get_model()
        props = self.layer.get_parasite_list()
        #print(f"{props=}")
        for row in model:
            if row[0] in props:
                row[3] = row[4] = tw.color_set
                ary = self.extract_array_from_parasite(row[0])
                row[1] = f"{ary}"
            else:
                for idx, value in enumerate([tw.text_empty, tw.text_empty, tw.color_empty, tw.color_empty], start=1):
                   #print(f"row[{idx}] = {value}")
                   row[idx]=value
        return True
    def grab_core_props_game(self):
        json_props_size = (
            ('kind', 1),
            ('hoverName', 1),
            ('suffix', 2),
            ('skipCond', 3),
            ('noInteraction', 1),
            ('roomStatus', 2),
            ('roomVariable', 2)
        )

        core_stuff = [SelectionInfo(prop_name, size, idx, None) for idx, (prop_name, size) in enumerate(json_props_size)]
        print('✨ DEBUG CORE INFO ✨')
        for i, elem in enumerate(core_stuff):
            print(core_stuff[i], i == core_stuff[i].row_idx)
        
        return

        



'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MioDialogo(Gtk.Dialog):
    def __init__(self, genitore):
        # Inizializzazione con titolo e finestra genitore
        #super().__init__(title="Esempio Sottoclasse", transient_for=genitore, flags=0)
        super().__init__(title="Esempio Sottoclasse")
        
        # Aggiunta dei pulsanti standard nell'area delle azioni (in basso)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        # Accesso all'area dei contenuti per aggiungere widget personalizzati
        area_contenuti = self.get_content_area()
        etichetta = Gtk.Label(label="Vuoi confermare questa operazione?")
        area_contenuti.add(etichetta)
        # Mostra tutti i widget all'interno del dialogo
        self.show_all()

# Esempio di utilizzo (senza una finestra principale completa)
dialogo = MioDialogo(None)
risposta = dialogo.run()

if risposta == Gtk.ResponseType.OK:
    print("Hai cliccato OK")
else:
    print("Hai annullato")

dialogo.destroy()
'''
