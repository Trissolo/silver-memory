import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrisBuilder():
    @staticmethod
    def make_gimp_button(label, clicked_handler = None, *sc_params):# = None, extended_clicked_handler = None, ec_params = None):
        button = GimpUi.Button.new()
        button.set_label(label)
        if callable(clicked_handler):
            button.connect("clicked", clicked_handler, *sc_params) if sc_params else button.connect("clicked", clicked_handler)
        #if callable(extended_clicked_handler):
        #    button.connect("extended-clicked", extended_clicked_handler, *ec_params) if ec_params else button.connect("extended-clicked", modifier, extended_clicked_handler)
        button.show()
        return button
    
    @staticmethod
    def make_label(text, use_markup = True):
        newLabel = Gtk.Label.new(text)
        newLabel.set_use_markup(use_markup)
        newLabel.show()
        return newLabel
    
    @staticmethod
    def make_clickable_label(text, use_markup = False, callback = False, *callback_args):
        label = Gtk.Label.new(text)
        label.set_use_markup(True)

        eventbox = Gtk.EventBox()
        eventbox.add(label)
        if callable(callback):
            eventbox.connect("button-press-event", callback, *callback_args)
        eventbox.show()
        return eventbox

class TrisLabel(Gtk.Label):
    def __init__(self, lbl):
        super().__init__(label = lbl)
        self.set_use_markup(True)
        self.set_default_style()
        self.eventbox = None

        # temporary use. Remember to delete the following line
        self.show()
    
    def write_default(self, text, list_params = None):
        self.raw_text_entered = text
        if list_params is None:
            list_params = self.default_style_params
        self.set_markup(self.assemble_span(text, *list_params))
        return self
    
    def assemble_span(self, text, color = None, bgcolor = None, size = 100, ts = 0, monospace = False):
        color = f'color="#{str(hex(color)).removeprefix("0x").zfill(6)}"' if type(color) == int else ""
        bgcolor = f'bgcolor="#{str(hex(bgcolor)).removeprefix("0x").zfill(6)}"' if type(bgcolor) == int else ""
        size = f'size="{size}%"' if type(size) == int else ""
        t = " " * ts
        text = f"<tt>{text}</tt>" if monospace else text
        return f"<span {color} {bgcolor} {size}>{t}{text}{t}</span>"
    
    def set_default_style(self, color = 0x202040, bgcolor = 0x2c2e53, size = 150, ts = 3, monospace = True):
            self.default_style_params = [color, bgcolor, size, ts, monospace]
            return self
    
    def add_to_box(self, box, widget = None, at_end = False, expand = False, fill=False,  padding=2):
            if widget is None:
                widget = self
            box.pack_end(widget, expand, fill, padding) if at_end else box.pack_start(widget, expand, fill, padding)
            return self
    
    def add_to_new_eventbox(self, callback, *cb_args):
            assert self.eventbox is not None, "There is already an EventBox for TrisLabel!"
            eventbox = Gtk.EventBox()
            if callable(callback):
                eventbox.connect("button-press-event", callback, *cb_args)
            eventbox.add(self)
            eventbox.show()
            self.eventbox = eventbox
            return eventbox







class TrisBase(Gtk.Frame):
    def __init__(self, trisParent, json_prop): #, json_list):
        super().__init__()
        self.trisParent = trisParent
        self.json_prop = json_prop
        #self.tris_enum = TrisEnum(json_list)

        

        #Poperties:
        #self.current_layer

        self.set_label_widget(TrisBuilder.make_gimp_button(f"🟠 {json_prop}", type(self).toggle_btn_handler, self))
        
        #container
        self.box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        
        self.add(self.box)
        self.lbl_key = TrisBuilder.make_label(self.json_prop, False)
        self.lbl_value = TrisBuilder.make_label("--......-", False)

        #self.lbl_key.set_hexpand(True)
        #self.lbl_value.set_hexpand(True)
        self.insert(self.lbl_key, self.lbl_value)



    @property
    def current_layer(self):
        return self.trisParent.current_layer
    
    @staticmethod
    def toggle_btn_handler(button, self):
        container = self.box
        if container.get_visible():
            container.hide()
            button.set_label(f"⚫ {self.json_prop}") #"🕳️"
        else:
            container.show()
            button.set_label(f"🟠 {self.json_prop}") # 👁️") #"🟠"
        print(self.current_layer.get_name())
    
    def insert(self, *args):
        for w in args:
            self.box.pack_start(w, False, False, 1)
        return self

# TO DO: derive this class form from one that, via a button, can toggle the visibility of its only child
class TrisChooserGrid():
    def __init__(self, trisParent, json_prop, json_list):
        self.trisParent = trisParent
        self.json_prop = json_prop
        # build a brand new Enum! (...and so, all the enums in 'trisParent' becomes superfluous )
        self.tris_enum = TrisEnum(json_list)

        self.lettererichieste = "e"
        #self.lbl_value.set_size_request(150, 110)

        #from here
        self.prop_key = TrisLabel(json_prop)
        self.prop_key.write_default(json_prop, [0xdedede, 0x565656, 150, 4, True])
        self.prop_value = TrisLabel("Prop-value")
        self.prop_human_readable_value = TrisLabel("Prop-human_readable")
   
        self.pseudobutton_delete_value = TrisLabel("Delete")
        self.pseudobutton_select_new_value = TrisLabel("New")

        hn_grid = Gtk.Grid.new()
        hn_grid.attach(self.prop_key, 0, 0, 2, 1)
        hn_grid.attach(self.prop_human_readable_value, 2, 0, 2, 1)
        hn_grid.attach(self.prop_value, 4, 0, 2, 1)
        hn_grid.attach(self.pseudobutton_delete_value, 5, 1, 1, 1)
        hn_grid.attach(self.pseudobutton_select_new_value, 5, 2, 1, 1)
        
        # to here

        # the Search field:
        searcWidget = Gtk.SearchEntry()
        searcWidget.show()
        searcWidget.connect("search-changed", self.on_search_activated, self)

        # the ListBox:
        listbox = Gtk.ListBox()
        
        # populate the ListBox
        for item in self.tris_enum.tlist:
            listbox_element = Gtk.ListBoxRow.new()
            listbox_element.data = item
            listbox_element.add(Gtk.Label(label = item))
            listbox.add(listbox_element)

        listbox.set_sort_func(self.sort_func, None, False)
        listbox.set_filter_func(self.tris_filter_func, self, False)
        listbox.connect("row-activated", self.on_row_activated_grid, self)
        listbox.set_hexpand(True)
        #set_hexpand(True)

        self.listbox = listbox

        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)

        hn_grid.attach(searcWidget, 6, 0, 2, 1)
        hn_grid.attach(scrolled, 6, 1, 2, 3)
        hn_grid.show_all()
        self.hn_grid = hn_grid

    def get_grid(self):
        return self.hn_grid

    @staticmethod
    def tb_ba_action(button, self):
        print("TrisChooser: Not yet implemented save parasite", self.tris_enum.get_all(2))
        print(self.current_layer.get_name(), "<--")
    
    @staticmethod
    def on_search_activated(searchentry, self):
        self.lettererichieste = searchentry.get_text()
        self.listbox.invalidate_filter()
    
    @staticmethod
    def sort_func(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    
    @staticmethod
    def tris_filter_func(row, self, notify_destroy):
        #print(data, "<--------- ORCUS")
        return True if self.lettererichieste.lower() in row.data.lower() else False
    
    @staticmethod
    def on_row_activated_grid(listbox_widget, row, self):
        print("Accesso inutile a trisLayer", self.current_layer.get_name())
        num, text = self.tris_enum.get_all(row.data)
        #self.lbl_value.set_text(f'{text} [{num}]')
        #self.prop_key.write_default()
        self.prop_value.write_default(num, [0x5566aa, 0xdada86, 200, 6, True])
        self.prop_human_readable_value.write_default(text)
    
    @property
    def current_layer(self):
        return self.trisParent.current_layer
    
    @staticmethod
    def toggle_btn_handler(button, self):
        container = self.box
        if container.get_visible():
            container.hide()
            button.set_label(f"⚫ {self.json_prop}") #"🕳️"
        else:
            container.show()
            button.set_label(f"🟠 {self.json_prop}") # 👁️") #"🟠"
        print(self.current_layer.get_name())
    
    def insert(self, *args):
        for w in args:
            self.box.pack_start(w, False, False, 1)
        return self




















class TrisChooser(TrisBase):
    def __init__(self, trisParent, json_prop, json_list): #, json_list):
        super().__init__(trisParent, json_prop)
        self.tris_enum = TrisEnum(json_list)
        self.lettererichieste = "e"
        self.lbl_value.set_size_request(150, 110)

        btn = TrisBuilder.make_gimp_button("Q", type(self).tb_ba_action, self)
        #btn.set_vexpand(False)

        searcWidget = Gtk.SearchEntry()
        searcWidget.show()
        searcWidget.connect("search-changed", self.on_search_activated, self)

        listbox = Gtk.ListBox()
        
        for item in self.tris_enum.tlist:
            listbox_element = Gtk.ListBoxRow.new()
            listbox_element.data = item
            listbox_element.add(Gtk.Label(label = item))
            listbox.add(listbox_element)

        listbox.set_sort_func(self.sort_func, None, False)
        listbox.set_filter_func(self.tris_filter_func, self, False)
        listbox.connect("row-activated", self.on_row_activated, self)
        listbox.set_hexpand(True)
        #for itlab in self.get_children()[0].get_children():
        #    itlab.set_hexpand(True)

        self.listbox = listbox

        scrolled = Gtk.ScrolledWindow.new(None, None)
        scrolled.add(listbox)

        paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        paned.pack1(searcWidget, False, False)
        paned.pack2(scrolled, False, False)
        paned.show()



        btn_provando_un_altro = TrisBuilder.make_clickable_label("Altro", True)
        btn_provando_un_altro.get_children()[0].set_markup('<span bgcolor="#8a9" color="#2378bd"> Altro </span>')

        button_holder = Gtk.ButtonBox.new(Gtk.Orientation.VERTICAL)
        button_holder.pack_start(btn, False, False, 2)

        button_holder.pack_start(btn_provando_un_altro, False, False, 4)
        button_holder.pack_start(TrisBuilder.make_gimp_button("Terzo"), False, False, 4)
        button_holder.pack_start(TrisBuilder.make_gimp_button("Ultimo"), False, False, 4)



        self.insert(button_holder, paned)
        #end test
        #self.insert(btn, paned)

    @staticmethod
    def tb_ba_action(button, self):
        print("TrisChooser: Not yet implemented save parasite", self.tris_enum.get_all(2))
        print(self.current_layer.get_name(), "<--")
    
    @staticmethod
    def on_search_activated(searchentry, self):
        self.lettererichieste = searchentry.get_text()
        self.listbox.invalidate_filter()
    
    @staticmethod
    def sort_func(row_1, row_2, data, notify_destroy):
        return row_1.data.lower() > row_2.data.lower()
    
    @staticmethod
    def tris_filter_func(row, self, notify_destroy):
        #print(data, "<--------- ORCUS")
        return True if self.lettererichieste.lower() in row.data.lower() else False
    
    @staticmethod
    def on_row_activated(listbox_widget, row, self):
        print("Accesso inutile a trisLayer", self.current_layer.get_name())
        num, text = self.tris_enum.get_all(row.data)
        self.lbl_value.set_text(f'{text} [{num}]')
#
class TrisFrame(Gtk.Frame):
    trisParent = None

    #@classmethod
    #def set_trisParent(cls, trisParent):
    #    cls.trisParent = trisParent
    

    colors = ["#f7e26b", "#eb8931", "#ccc", "#3939c8"] #["#111", "#81c784", "#333", "#777"]

    
    @staticmethod
    def first_button_clicked(widget, self):
        print("Click", self.bool_test)
        self.bool_test = not self.bool_test
        self.write_prop(self.bool_test)

    
    @staticmethod
    def toggle_visibility(widget, container, raw_name):
        if container.get_visible():
            container.hide()
            widget.set_label(f"{raw_name} ⚫") #"🕳️"
        else:
            container.show()
            widget.set_label(f"{raw_name} 👁️")
    

    def __init__(self, json_prop, trisParent):
        super().__init__()
        self.json_prop = json_prop
        self.trisParent = trisParent
        trisParent.add_to_manager(json_prop, self)
        self.bool_test = True

        self.box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        self.add(self.box)

        toggle_button = TrisBuilder.make_gimp_button(json_prop + " (Tris-toggle)", type(self).toggle_visibility, self.box, self.json_prop)
        self.set_label_widget(toggle_button)

        self.json_key = TrisBuilder.make_label(f"Prop: {json_prop}???")
        self.json_value = TrisBuilder.make_label("Value ???")

        self.btn_as = GimpUi.Button.new_from_icon_name("edit-delete", 1)
        self.btn_as.connect("clicked", type(self).first_button_clicked, self)

        self.insert(self.json_key, self.json_value, self.btn_as)

        self.show_all()
    
    
    @property
    def current_layer(self):
        return self.trisParent.current_layer
    

    def insert(self, *args):
        for w in args:
            self.box.pack_start(w, False, False, 1)
        return self
       
    
    def write_prop(self, value_is_set = True):
        cols = type(self).colors
        fgc, bgc = (cols[0], cols[1]) if value_is_set else (cols[2], cols[3])
        self.json_key.set_markup(f'<span background="{bgc}" foreground="{fgc}"> {self.json_prop} </span>:') # <i>[0, 4]</i>')
        return self
    

    def add_paned_test(self):     
            searcWidget = Gtk.SearchEntry()
            searcWidget.show()
            
            def on_search_activated(searchentry, self):
                t = searchentry.get_text()
                self.lettererichieste = t
                self.listbox.invalidate_filter()
                #print(f"SearchEntry text: {t if len(t) != 0 else '---'}")
            
            searcWidget.connect("search-changed", on_search_activated, self)
            paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
            paned.pack1(searcWidget, False, False)
            paned.show()
            self.insert(paned)

            scrolled = Gtk.ScrolledWindow.new(None, None)
            paned.pack2(scrolled, False, False)

            listbox = Gtk.ListBox()
            scrolled.add(listbox)

            self.lettererichieste = "e"

            for item in ["gene", "elevator", "thought", "patience", "explanation", "chemistry", "movie", "excitement"]: #items:
                listbox_element = Gtk.ListBoxRow.new()
                listbox_element.data = item
                listbox_element.add(Gtk.Label(label = item))
                listbox.add(listbox_element)
            
            def sort_func(row_1, row_2, data, notify_destroy):
                return row_1.data.lower() > row_2.data.lower()
            
            listbox.set_sort_func(sort_func, None, False)

            def another_filter_func(row, data, notify_destroy):
                return True if data.lettererichieste in row.data else False
            
            listbox.set_filter_func(another_filter_func, self, False)

            self.listbox = listbox

            def on_row_activated(listbox_widget, row, self):
                print("Accesso inutile a trisLayer", self.current_layer.get_name())
                self.json_value.set_markup(f'<i>{row.data}</i>')
                #print("Option", row.data, instance.lettererichieste)

            listbox.connect("row-activated", on_row_activated, self)


class TrisEnum:
    def __init__(self, ary, desc = "not specified"):
        assert len(ary) == len({x for x in ary}), "TrisEnum: Duplicate names in parameter List"
        tlist = []
        tdict = {}
        for idx, elem in enumerate(ary):
            tlist.append(elem)
            tdict[idx] = elem
            tdict[elem] = idx
        self.tdict = tdict
        self.tlist = tlist
        self.get = self.get_corresponding
        self.desc = desc
    def get_list(self):
        return self.tlist
    def get_corresponding(self, param):
        if not self.has(param):
            raise KeyError(f'Element NOT present in TrisEnum: {param}') 
        return self.tdict[param]
    def get_all(self, param):
        value = self.get_corresponding(param)
        return (value, self.tdict[value]) if type(value) is int else (self.tdict[value], value)
    def has(self, param):
            return param in self.tdict
    def get_length(self):
        #return len(self.tdict) >> 1
        return len(self.tlist)
    def __repr__(self):
        l = self.get_length()
        a = f"TrisEnum for: {self.desc}, lenght: {l}.\n"
        if l > 0:

            a += f"Elem[0]: '{self.tlist[0]}', elem[1]: '{self.tlist[1]}', elem[last]: '{self.tlist[-1]}'\n"

        return a


# 
def elenca_figli(widget, lev = 1, idx = 0, lc = 1, hastrai = False, sp = "    ", hook = "╰╴", vpipe = "│"):
            if hasattr(widget, 'get_children'):
                gra = "└─" if (lc - idx) == 1 else "├─"
                indent = f"{sp * lev}" if not hastrai else f"{sp * (lev-1)}{vpipe}"
                print(f"{indent}{gra}{widget.get_name()}😫")
                chi = widget.get_children()
                lc = len(chi)
                for idx, elem in enumerate(chi):
                    elenca_figli(elem, lev + 1, idx, lc,((lc - idx) == 0), sp, hook, vpipe)
            else:
                print(f"{sp * (lev + 1)}└─{widget.get_name()}")


'''
    def elenca_figli(self, widget, lev = 1, idx = 0, lc = 1, hastrai = False, sp = "    ", hook = "╰╴", vpipe = "│"):
            if hasattr(widget, 'get_children'):
                gra = "└─" if (lc - idx) == 1 else "├─"
                indent = f"{sp * lev}" if not hastrai else f"{sp * (lev-1)}{vpipe}"
                print(f"{indent}{gra}{widget.get_name()}")
                chi = widget.get_children()
                lc = len(chi)
                for idx, elem in enumerate(chi):
                    self.elenca_figli(elem, lev + 1, idx, lc,((lc - idx) == 0), sp, hook, vpipe)
            else:
                print(f"{sp * (lev + 1)}└─{widget.get_name()}")
    '''

#def build_node(name = "Some node"):
#     return _Node(name)

'''
def build_tree(root, lev = 0, next_id = 0, res = dict()):
    if not root in res:
        res[root] = _Node(root.get_name(), lev, next_id + 1)
        if hasattr(root, 'get_children'):
            for child in root.get_children():
                #next_id = next_id + 1
                build_tree(child, lev + 1, next_id, res)
    return res
             

class _Node:
    def __init__(self, name, level = 0, id = 0, neighbours = set()):
        self.name = name
        self.neighbours = neighbours
        self.isContainer = False
        self.level = level
        self.id = id
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def isContainer(self):
        return self._isContainer
    
    @isContainer.setter
    def isContainer(self, value):
        self._isContainer = value
    
    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

'''
#__all__ = ["build_node", "elenca_figli"]


'''
#extended_click
extended_click
def standard_click(widget):
    print("Standard click")

 
def extended_click(widget, event):
    print("Extended click", event)


dialogazzo = GimpUi.Dialog.new()
dialogazzo.set_title('Test_update_button')

main_box = dialogazzo.get_content_area()

button = GimpUi.Button()

main_box.pack_start(button, False, False, 1)

button.connect("clicked", standard_click)
button.connect("extended-clicked", extended_click)

mnem_label = Gtk.Label.new_with_mnemonic("_Update")
mnem_label.get_mnemonic_keyval()
mnem_label.set_mnemonic_widget(button)

#main_box.pack_start(mnem_label, False, False, 1)
button.add(mnem_label)


dialogazzo.show_all()
dialogazzo.run()

#dialogazzo.destroy()



def fargs(*args):
    print(f"Len: {len(args)}")
    for idx, elem in enumerate(args):
        print(f"elem at pos #{idx} is: {elem}")


dialogazzo = GimpUi.Dialog.new()
dialogazzo.set_title('Test')

main_box = dialogazzo.get_content_area()

listbox = Gtk.ListBox()



main_box.pack_start(listbox, False, False, 1)
#main_box.pack_start(listbox_element, False, False, 1)

#items = "This is a sorted ListBox Fail".split()
items = ["gene", "elevator", "thought", "patience", "explanation", "chemistry", "movie", "excitement"]

for item in items:
    listbox_element = Gtk.ListBoxRow.new()
    listbox_element.data = item
    listbox_element.add(Gtk.Label(label = item))
    listbox.add(listbox_element)

def sort_func(row_1, row_2, data, notify_destroy):
    return row_1.data.lower() > row_2.data.lower()

def filter_func(row, data, notify_destroy):
    return False if row.data == "excitement" else True

listbox.set_sort_func(sort_func, None, False)
listbox.set_filter_func(filter_func, None, False)

def on_row_activated(listbox_widget, row):
    print(row.data)

listbox.connect("row-activated", on_row_activated)



def another_filter_func(row, data, notify_destroy):
    return True if row.data.startswith("e") else False

#listbox.invalidate_filter()
listbox.set_filter_func(another_filter_func, None, None)


dialogazzo.show_all()
dialogazzo.run()

#dialogazzo.destroy()
'''

'''
def trutil_build_main_dialog(name, btn_ok = None, btn_cancel = None):
    dialog = GimpUi.Dialog.new()
    dialog.set_name(name)
    dialog.set_title(name)
    if isinstance(btn_ok, str):
        dialog.add_button(btn_ok, Gtk.ResponseType.OK)  #Gtk.ResponseType.APPLY)
    if isinstance(btn_cancel, str):
        dialog.add_button(btn_cancel, Gtk.ResponseType.CANCEL)
    return dialog


def trutil_box_insert(box, child, show = True, padding = 2):
    #if not isinstance(child, list):
    #    child = [child]
    #for c in child:       
    #    box.pack_start(c, False, False, padding)
    #return box
    box.pack_start(child, False, False, padding)
    if show:
          child.show()
    return box

def trutil_make_button(name, label = "",  click_handler = None, extended_click_handler = None):
    pulsante = GimpUi.Button.new() if label == "" else GimpUi.Button.new_with_label(label)
    pulsante.set_name(name)
    pulsante.set_size_request(80, 60)
    pulsante.show()
    if callable(click_handler):
        pulsante.connect('clicked', click_handler)
    if callable(extended_click_handler):
        pulsante.connect("extended-clicked", extended_click)
    return pulsante


def trutil_make_label_mnemonic(text, mnem_widget = None, add_to_widget = False):
    temp = "_"
    mnem_label = Gtk.Label.new_with_mnemonic(text if text.startswith(temp) else f"{temp}{text}")
    if mnem_widget:
        #mnem_label.get_mnemonic_keyval()
        mnem_label.set_mnemonic_widget(mnem_widget)
        if add_to_widget:
            mnem_widget.add(mnem_label)
        mnem_label.add(mnem_widget)
    mnem_label.show()
    return mnem_label


inner_label.set_use_markup(True)
inner_label.set_markup('<span foreground="#5687ff" size="x-large">skipCondition</span>: <i>[0, 4]</i>')
inner_label.set_markup('<



'''

'''
#hardcoded

dialogazzo = GimpUi.Dialog.new()
dialogazzo.set_title('Test')

main_box = dialogazzo.get_content_area()

listbox = Gtk.ListBox()



main_box.pack_start(listbox, False, False, 1)
#main_box.pack_start(listbox_element, False, False, 1)

#items = "This is a sorted ListBox Fail".split()
items = ["gene", "elevator", "thought", "patience", "explanation", "chemistry", "movie", "excitement"]

uniqueObject = {"lettererichieste": "e"}

for item in items:
    listbox_element = Gtk.ListBoxRow.new()
    listbox_element.data = item
    listbox_element.add(Gtk.Label(label = item))
    listbox.add(listbox_element)

def sort_func(row_1, row_2, data, notify_destroy):
    return row_1.data.lower() > row_2.data.lower()

listbox.set_sort_func(sort_func, None, False)

#def filter_func(row, data, notify_destroy):
#    return False if row.data == "excitement" else True

def another_filter_func(row, data, notify_destroy):
    return True if data["lettererichieste"] in row.data else False

# "register" filter function, passing in the "control" object
#listbox.set_filter_func(another_filter_func, None, False)
listbox.set_filter_func(another_filter_func, uniqueObject, False)

# Action when the user click on a voice
def on_row_activated(listbox_widget, row):
    print(row.data)

listbox.connect("row-activated", on_row_activated)

dialogazzo.show_all()

uniqueObject["lettererichieste"] = "ex"
listbox.invalidate_filter()
'''

'''
#SearchEntry hardcoded

dialogazzo = GimpUi.Dialog.new()
dialogazzo.add_button("_Cancel", Gtk.ResponseType.CANCEL)

def on_search_activated(searchentry):
    t = searchentry.get_text()
    print(f"SearchEntry text: {t if len(t) != 0 else '---'}")

sew = Gtk.SearchEntry()

# "activate" signal -> emitted by Enter key press
#sew.connect("activate", on_search_activated)

# During text insertion
sew.connect("search-changed", on_search_activated)

dialogazzo.get_content_area().pack_start(sew, False, False, 1)

sew.show()

dialogazzo.run()
#dialogazzo.destroy()
'''

'''
# Custom Class!
class ExtFrame(Gtk.Frame):
    #staticmethod
    def customDestroy(widget):
        print("customDestroy:", widget.porconame)
    
    def __init__(self, name = "Label not specified"):
        super().__init__(label=name)
        self.custom_destroy_id = self.connect("destroy", type(self).customDestroy)
        self.porconame = "Porco Name!"
        self.show()

'''

'''
uff :(
def make_gimp_button(label, clicked_handler = None, sc_params = None, extended_clicked_handler = None, ec_params = None):
    button = GimpUi.Button.new()
    button.set_label(label)
    if callable(clicked_handler):
        button.connect("clicked", clicked_handler, *sc_params) if sc_params else button.connect("clicked", clicked_handler)
    if callable(extended_clicked_handler):
        button.connect("extended-clicked", extended_clicked_handler, modifier, *ec_params) if ec_params else button.connect("extended-clicked", modifier, extended_clicked_handler)
    button.show()
    return button

def altHandler(widget, modifier, one, two, qwe):
    print(one, two, qwe)

def standcl(widget, q, w):
    print(q, w)
'''
'''
# con helper
def make_clickable_markup_label(text, callback = False, *args):
    label = Gtk.Label(label=text)
    label.set_use_markup(True)
    eventbox = Gtk.EventBox()
    if callable(callback):
        eventbox.connect("button-press-event", callback, *args)
    eventbox.add(label)
    eventbox.show()
    return eventbox

def on_button_press_event(a, b, c):
    print("ORCUS-DEUS!", a, b, c[0])

eventbox = make_clickable_label("EAZZ", True, on_button_press_event, [*"ZXCVB"])
dialogazzo = GimpUi.Dialog.new()
dialogazzo.get_content_area().pack_start(eventbox, False, False, 1)
dialogazzo.show_all()


def assemble_span(text, color = None, bgcolor = None, size = 100, ts = 0, monospace = False):
    color = f'color="#{str(hex(color)).removeprefix("0x").zfill(6)}"' if type(color) == int else ""
    bgcolor = f'bgcolor="#{str(hex(bgcolor)).removeprefix("0x").zfill(6)}"' if type(bgcolor) == int else ""
    size = f'size="{size}%"' if type(size) == int else ""
    t = " " * ts
    text = f"<tt>{text}</tt>" if monospace else text
    return f"<span {color} {bgcolor} {size}>{t}{text}{t}</span>"


lab = eventbox.get_children()[0]
lab.set_markup(assemble_span("RIAZZ", None, 0xaabbff, 5))
'''
