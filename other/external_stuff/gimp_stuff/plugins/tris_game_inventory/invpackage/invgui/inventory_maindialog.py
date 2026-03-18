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
        self._swap_condition_ary = [None] * 3

        #3 the Stack (empty for now)
        self.stack = Gtk.Stack.new()
        self.tw = Gtk.TreeView.new()


        #4 Populate the Top Bar
        self.generate_top_bar()

        #5 Populate the Middle Bar
        self.generate_middle_bar()

        #6 the core widgets!
        self.prepare_rowInfos()

        #7 the TreeView
        tw = self.build_tw()

        #8 initial message on stack
        self.stack.add_named(self._gui_element_label("Select a property on the left"), "startmessage")
        self.stack.set_visible_child_name("startmessage")

        #9 the Paned!
        paned = self._gui_element_paned()
        paned.pack1(tw)
        paned.pack2(self.stack)
        paned.show_all()

        # test:
        print("Test: 'Dialog content area' children")
        for child in self.get_content_area().get_children():
            print(child.get_name())

        #10 Ready!
        self.curr_sel = self.row_infos[0]
        self.update_layer()

        # END __init__ method
    
    def set_current_prop(self, array):
        compressed_ary = self.manage_array(array)
        print(f"Attaching {array} ({compressed_ary}) to Prop: {self.curr_sel.prop}")
        self.attach_array_to_current_layer(self.curr_sel.prop, array)
        row = self.tw.get_model()[self.curr_sel.row_idx]
        row[1] = self.curr_sel.wid.get_readable(array, self.curr_sel.size)
        row[2] = f"{array}"
        row[3] = row[4] = self.CONST_COLOR_SET
        
        return

    def _on_destroy(self, widget):
        self.remove_image_references()

        self._top_label = None
        self.stack = None

        for elem in self.row_infos:
            elem.clear()
        self.row_infos = self.row_infos.clear()

        self._swap_condition_ary = self._swap_condition_ary.clear()

        print("Inventory plugin destroyed!")
    
    def build_tw(self):
        row_infos = self.row_infos

        self.curr_sel = None

        column_headers = ["Prop", "Readable", "Effective"]

        # attribute mapping

        first_colum_color = len(column_headers)

        other_colums_color = first_colum_color + 1

        #print(f"{first_colum_color=}, {other_colums_color=}")

        mytypes = [str] * len(column_headers)

        cell_types = [*mytypes, str, str]

        # the Store/Model!
        store = Gtk.ListStore.new(cell_types)

        # the TreeView
        tw = self.tw

        tw.set_model(store)

        # constants AS!
        self.CONST_TEXT_EMPTY = "---"
        self.CONST_COLOR_EMPTY = "#333"
        self.CONST_COLOR_SELECTED = "#454"
        self.CONST_COLOR_SET = "#66a"

        # populate the store:
        for row in row_infos:
            store.append([row.prop, self.CONST_TEXT_EMPTY, self.CONST_TEXT_EMPTY, self.CONST_COLOR_EMPTY, self.CONST_COLOR_EMPTY])
        
        cell = Gtk.CellRendererText.new()

        for idx, name in enumerate(column_headers):
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=first_colum_color if idx==0 else other_colums_color)
            tw.append_column(col)
        
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
        # paned_container.pack1(tw)
        tw.show_all()
        return tw
        
    def on_active_row(self, treeview, row_idx, colu):
        print("On Active Row!")
        index_as_int = row_idx.get_indices()[0]
        treeview.get_selection().unselect_all()

        # GUI tests:
        model = treeview.get_model()
        if self.curr_sel is not None:
            prev_row =  model[self.curr_sel.row_idx]
            prev_row[3] = prev_row[4] = self.CONST_COLOR_EMPTY if prev_row[1] == self.CONST_TEXT_EMPTY else self.CONST_COLOR_SET
        model[index_as_int][3] = model[index_as_int][4] = self.CONST_COLOR_SELECTED
        #model[index_as_int][4] = self.CONST_COLOR_EMPTY if model[index_as_int][1] == self.CONST_TEXT_EMPTY else "#894532"
        
        # important
        self.curr_sel = self.row_infos[index_as_int]
        self.show_appropriate_right_widget()

    def show_appropriate_right_widget(self):
        self.stack.set_visible_child(self.curr_sel.wid)
        if type(self.curr_sel.wid) is MultiChooser:
            temp_multichooser = self.curr_sel.wid
            temp_multichooser.deduce_bottom_box_visibility_by_size(self.curr_sel.size)
            if self.curr_sel.size == 3:
                print("Size is 3")
                self._swap_condition_ary = [None] * 3
                temp_multichooser.get_condition_preview_label().set_text("select the variable")
            else:
                print("Size is lesser than 3")
        return
    
    def tw_refresh_hard(self, model=None):
        if model == None:
            model = self.tw.get_model()

        props = self.layer.get_parasite_list()

        

        for property_index, row in enumerate(model):
            if row[0] in props:
                row[3] = row[4] = self.CONST_COLOR_SET
                ary = self.extract_array_from_parasite(row[0])
                print(f"✂️ tw_refresh_hard: {row[0]} {ary} {self.curr_sel.wid.get_name()}")
                row[1] = f"{self.row_infos[property_index].wid.get_readable(ary, self.row_infos[property_index].size)}"
                row[2] = f"{ary}"
            else:
                for idx, value in enumerate([self.CONST_TEXT_EMPTY, self.CONST_TEXT_EMPTY, self.CONST_COLOR_EMPTY, self.CONST_COLOR_EMPTY], start=1):
                   row[idx]=value
        return True
    
    def prepare_rowInfos(self):
        #return self.prepare_row_infos_game() if self.crossroads else self.prepare_row_infos_inventory()
        return self.prepare_row_infos_inventory() if self.crossroads else self.prepare_rowInfos_game()
    
    def prepare_rowInfos_game(self):
        wid_kind = self.build_chooser_kind(isMonoChooser=False)
        wid_unary = self.build_chooser_kind(isMonoChooser=True)
        widget_vars = self.build_chooser_vars()
        widget_overnames = self.build_chooser_overnames()

        json_props_size = (
            ('kind', 1, wid_kind),
            ('hoverName', 1, widget_overnames),
            ('suffix', 2, widget_vars),
            ('skipCond', 3, widget_vars),
            ('noInteraction', 1, wid_unary),
            ('roomStatus', 2, widget_vars),
            ('roomVariable', 2, widget_vars)
        )
        
        # print("Debug row_infos")
        # [print(prop_name, size, wid) for idx, (prop_name, size, wid) in enumerate(json_props_size)]
        row_infos = [SelectionInfo(prop_name, size, idx, wid) for idx, (prop_name, size, wid) in enumerate(json_props_size)]

        self.row_infos = row_infos

        # print('✨ DEBUG CORE INFO ✨')
        # for i, elem in enumerate(row_infos):
        #     print(row_infos[i], i == elem.row_idx, "row_infos[i]", row_infos[i] == elem)       
        return row_infos
    
    def prepare_row_infos_inventory(self):
        #wid_kind = self.build_chooser_kind(isMonoChooser=False)
        wid_unary = self.build_chooser_kind(isMonoChooser=True)
        #widget_vars = self.build_chooser_vars()
        #widget_overnames = self.build_chooser_overnames()

        json_props_size = (
            ('cumulable', 1, wid_unary),
            ('special', 1, wid_unary),
            ('another_prop', 1, wid_unary)
        )
        
        row_infos = [SelectionInfo(prop_name, size, idx, wid) for idx, (prop_name, size, wid) in enumerate(json_props_size)]

        self.row_infos = row_infos

        return row_infos
    
    def build_chooser_overnames(self): #, stack_container):
        ch = SingleChooser(source=self.load_json_hovernames(), var_kind=None)
        # signal
        ch.get_salient_widget().connect('row-activated', self.handler_chooser_overnames)
        # add to container
        self.stack.add_named(ch, "widget overnames")
        return ch
    def handler_chooser_overnames(self, listbox, row):
        name_idx = row.idx
        self.set_current_prop([name_idx])
        return True
    
    def build_chooser_vars(self):
        mc = MultiChooser(self.load_json_vars())
        # signal 
        for elem in mc.get_listboxes():
           elem.connect('row-activated', self.handler_chooser_vars)
        #button confirm signal
        mc.get_confirm_button().connect('clicked', self.handler_confirm_condition)
        # add to container
        self.stack.add_named(mc, "widget_vars")
        return mc
    def handler_chooser_vars(self, listbox, row):
        print(f"New lbs [{listbox.var_kind}, {row.idx}] SIZE: {self.curr_sel.size}")
        if self.curr_sel.size == 2:
            self.set_current_prop([listbox.var_kind, row.idx])
            return
        else:
            self._swap_condition_ary[0] = listbox.var_kind
            self._swap_condition_ary[1] = row.idx
            self.curr_sel.wid.get_condition_preview_label().set_text(f"if {listbox.var_kind}, {row.idx} equals (?) -->")
    def handler_confirm_condition(self, confirm_button):
        lab, spin, _ = confirm_button.get_parent().get_children()
        retrieved_spinbutton = confirm_button.get_parent().get_children()[1]
        value = retrieved_spinbutton.get_value_as_int()
        self._swap_condition_ary[2] = value
        print(f"🚌 Condition: {self._swap_condition_ary}")
        if self._swap_condition_ary.count(None) != 0:
            lab.set_text("First of all SELECT the condition!")
        else:
            a, b, c = self._swap_condition_ary
            lab.set_text(f"  If [{a}, {b}] equals {c} <-> ")
            self.set_current_prop(self._swap_condition_ary)

        #"bottom box get_children", lab.get_name(), spin.get_name(), confirm_button.get_name())

        
    def build_chooser_kind(self, isMonoChooser):
        kc = DictChooser(isMonoChooser)
        for elem in kc.get_salient_widgets():
            elem.connect('clicked', self.handler_chooser_kind)
        self.stack.add_named(kc, "widget_mono" if len(kc.source) == 1 else "widget_kinds")
        return kc
    def handler_chooser_kind(self, button):
        print(f"Saving kind: {button.key}")
        self.set_current_prop([button.key])
