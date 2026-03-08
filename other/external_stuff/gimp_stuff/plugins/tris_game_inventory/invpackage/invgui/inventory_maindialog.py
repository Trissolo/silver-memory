import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# dataclass
from dataclasses import dataclass

@dataclass
class SelectionInfo:
    prop: str | None
    size: int | None
    row_idx: int | None
    wid: Gtk.Widget | None
    def clear(self):
        self.prop = None
        self.size = None
        self.row_idx = None
        self.wid = None
    def set_widget(self, widget):
        self.wid = widget
        return self

# from .imagestuff import ImageStuff
from .guibargenerator import GuiBarGenerator

class InventoryDialog(GimpUi.Dialog, GuiBarGenerator): #, ImageStuff):
    def __init__(self, image, *args):
        # First of all
        super().__init__(title="Tris Inventory Generator", *args)
        
        #0 the Dialog chores:
        #self.set_title("Tris Inventory generator")
        self.set_keep_above(True)
        self.add_buttons( "Done [close]", Gtk.ResponseType.OK)
        self.connect("destroy", self._on_destroy)
        self.set_name("Inv. Dialog")

        #1 Set the Image and Current Layer:
        self.image = image
        self.layer = None

        #2 the containers!
        # results = [value for num in numbers if (value := slow(num)) > 0]
        #top_bar, middle_bar = ary = [(p := Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)) for _ in range(3) if p.set_name(f'box_#{_}') is None]
        #top_bar, middle_bar = [p for name in ["Top Bar", "Middle Bar"] if (p := Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)) and p.set_name(name) == self.get_content_area().pack_start(p, False, True, 2)]

        #3 Populate the Top Bar
        self.generate_top_bar()

        #4 Populate the Middle Bar
        self.generate_middle_bar()

        #5 the core widgets!
        # ...

        #6 Set the Layer!
        #self.update_layer()
        # test:
        for child in self.get_content_area().get_children():
            print(child.get_name())

        #self.generate_json()
        self.build_tw()
        #self.summary_debug()
    
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

        column_amount = len(column_headers)

        id_for_others = column_amount + 1

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
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=3 if idx==0 else 4)
            tw.append_column(col)
        
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
        self.get_content_area().pack_start(tw, False, False, 1)
        tw.show_all()

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
