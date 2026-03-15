import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .gui_bar_generator import GuiBarGenerator
from ..misc.selectioninfo import SelectionInfo
from .singleChooser import SingleChooser
from .multiChooser import MultiChooser
from .dictChooser import DictChooser

class InventoryDialog(GimpUi.Dialog, GuiBarGenerator):
    def __init__(self, image, crossroads, *args):
        # First of all
        super().__init__(title="Tris Inventory Generator", *args)

        # Is this the Inventory Dialog (True) or the Properties Dialog (False)?
        self.crossroads = crossroads
        
        #0 the Dialog chores:
        self.set_keep_above(True)
        self.connect("destroy", self._on_destroy)
        self.set_name("Inv. Dialog")
        # self.add_buttons( "Done [close]", Gtk.ResponseType.OK)

        #1 Set the Image and Current Layer:
        self.image = image
        self.layer = None

        #2 'global' paraphernalia
        self.curr_sel = None
        self.row_infos = None

        self.stack = None
        self.tw = None

        #3

        #4 Populate the Top Bar
        self.generate_top_bar()

        #5 Populate the Middle Bar
        self.generate_middle_bar()

        # the Paned!
        paned = self._gui_element_paned()
        stack = Gtk.Stack.new()
        paned.pack2(stack)
        self.prepare_rowInfos(stack=stack)
        tw = self.build_tw()
        paned.pack1(tw)
        paned.show_all()
        #print(stack.get_children())
        self.stack = stack

        #6 the core widgets!
        # ...
        

        #5 Set the Layer!

        # self.update_layer()


        # test:
        print("Test: 'Dialog content area' children")
        for child in self.get_content_area().get_children():
            print(child.get_name())

        #6 Ready!
        

        #self.curr_sel = self.row_infos[3]
        #self.build_chooser_overnames(stack)
        #self.build_chooser_vars(stack)

        

        
        
        self.update_layer()
        # self.tw_refresh_hard()
        # self.summary_debug()
        # self.generate_json()
        # self.load_json_hovernames()

        # END __init__ method
    
    def set_current_prop(self, array):
        compressed_ary = self.manage_array(array)
        print(f"Attanching {array} ({compressed_ary}) to Prop: {self.curr_sel.prop}")
        #self.attach_array_to_current_layer(self.curr_sel.prop, array)
        return

    def _on_destroy(self, widget):
        self.remove_image_references()

        self._top_label = None

        for elem in self.row_infos:
            elem.clear()
        self.row_infos = self.row_infos.clear()

        print("Inventory plugin destroyed!")
    
    def build_tw(self):
        row_infos = self.row_infos # = self.prepare_rowInfos()

        self.curr_sel = None

        column_headers = ["Prop", "Readable", "Effective"]

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
        for row in row_infos:
            store.append([row.prop, tw.text_empty, tw.text_empty, tw.color_empty, tw.color_empty])
        
        cell = Gtk.CellRendererText.new()

        for idx, name in enumerate(column_headers):
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=first_colum_color if idx==0 else other_colums_color)
            tw.append_column(col)
        
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
        # paned_container.pack1(tw)
        tw.show_all()
        self.tw = tw
        return tw
        
    def on_active_row(self, treeview, row_idx, colu):
        print("On Active Row!")
        index_as_int = row_idx.get_indices()[0]
        treeview.get_selection().unselect_all()
        self.curr_sel = self.row_infos[index_as_int]
        print(f"qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq {self.curr_sel.wid=}")
        self.stack.set_visible_child(self.curr_sel.wid)

        # Additional tests:
        model = treeview.get_model()
        if self.curr_sel is not None:
            model[self.curr_sel.row_idx][3] = model[self.curr_sel.row_idx][4]
        model[index_as_int][3] = treeview.color_selected
        model[index_as_int][4] = treeview.color_empty
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
    
    def prepare_rowInfos(self, stack):
        wid_kind = self.build_chooser_kind(isMonoChooser=False, stack_container=stack)
        wid_unary = self.build_chooser_kind(isMonoChooser=True, stack_container=stack)
        wid_wars = self.build_chooser_vars(stack)
        wid_hevernames = self.build_chooser_overnames(stack)

        json_props_size = (
            ('kind', 1, wid_kind),
            ('hoverName', 1, wid_hevernames),
            ('suffix', 2, wid_wars),
            ('skipCond', 3, wid_wars),
            ('noInteraction', 1, wid_unary),
            ('roomStatus', 2, wid_wars),
            ('roomVariable', 2, wid_wars)
        )
        print("Debug core_stuff")
        [print(prop_name, size, wid) for idx, (prop_name, size, wid) in enumerate(json_props_size)]
        core_stuff = [SelectionInfo(prop_name, size, idx, wid) for idx, (prop_name, size, wid) in enumerate(json_props_size)]

        self.row_infos = core_stuff

        # print('✨ DEBUG CORE INFO ✨')
        # for i, elem in enumerate(core_stuff):
        #     print(core_stuff[i], i == elem.row_idx, "core_stuff[i]", core_stuff[i] == elem)       
        return core_stuff
    
    def build_chooser_overnames(self, stack_container):
        ch = SingleChooser(source=self.load_json_hovernames(), var_kind=None)
        #self.row_infos[1].set_widget(ch)
        # signal
        ch.get_salient_widget().connect('row-activated', self.handler_chooser_overnames)
        # add to container
        stack_container.add_named(ch, "widget overnames")
        return ch
    def handler_chooser_overnames(self, listbox, row):
        name_idx = row.idx
        #print(f"Choosed: {name_idx} -> {self.row_infos[1].wid.get_readable([name_idx])}")
        self.set_current_prop([name_idx])
        return True
    
    def build_chooser_vars(self, stack_container):
        mc = MultiChooser(self.load_json_vars())
        # signal
        for elem in mc.get_listboxes():
           elem.connect('row-activated', self.handler_chooser_vars)
        # add to container
        stack_container.add_named(mc, "widget_vars")
        return mc
    def handler_chooser_vars(self, listbox, row):
        print(f"New lbs [{listbox.var_kind}, {row.idx}]")
        self.set_current_prop([listbox.var_kind, row.idx])
    def build_chooser_kind(self, isMonoChooser, stack_container):
        kc = DictChooser(isMonoChooser)
        for elem in kc.get_salient_widgets():
            elem.connect('clicked', self.handler_chooser_kind)
        stack_container.add_named(kc, "widget_mono" if len(kc.source) == 1 else "widget_kinds")
        return kc
    def handler_chooser_kind(self, button):
        print(f"Saving kind: {button.key}")
        self.set_current_prop([button.key])




        



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
