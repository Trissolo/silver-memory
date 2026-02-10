import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def test():
    print('Isolated stuff here')

def util_eventbox_for_widget(widget, on_click_handler, *custom_args):
    eventbox = Gtk.EventBox()
    eventbox.set_name(f"EventBox for {widget.get_name()}")
    #
    # def minimun_handler(evbox, event):
    #     pass
    #
    if callable(on_click_handler):
        eventbox.connect("button-press-event", on_click_handler, *custom_args) #type(self).on_click_handler)
    eventbox.add(widget)
    #eventbox.show()
    return eventbox

class TrisLabel(Gtk.Label):
    def __init__(self, text = "My TrisLabel"):
        super().__init__(self)
        self.set_use_markup(True)
        self.set_name("La TrisLABEL (my extended Gtk.Label -> the click-enabled Widget)")
        self.last_entered_raw_text = ""
        self.set_default_text(text)
        self.show()
    
    def set_default_text(self, text):
        self.default_text = text
    
    def write(self, text = None, color=None, bgcolor=None, size=100, pad=0, padleft=0, padright=0, monospace=False, italic=False, bold = False):
        if text is None: text = self.default_text
        self.last_entered_raw_text = text
        self.set_markup(type(self).assemble_span(text, color, bgcolor, size, pad, padleft, padright, monospace, italic, bold))
    
    @classmethod
    def assemble_span(cls, text, color=None, bgcolor=None, size=100, pad=0, padleft=0, padright=0, monospace=False, italic=False, bold=False):
        color = f'color="#{cls.int_to_hex_string(color)}"' if type(color) == int else ""
        bgcolor = f'bgcolor="#{cls.int_to_hex_string(bgcolor)}"' if type(bgcolor) == int else ""
        size = f'size="{size}%"' if type(size) == int else ""
        pad = " " * pad
        padleft = " " * padleft
        padright = " " * padright
        if italic: text = f"<i>{text}</i>"
        if bold: text = f"<b>{text}</b>"
        if monospace: text = f"<tt>{text}</tt>"
        return f"<span {color} {bgcolor} {size}>{pad}{padleft}{text}{padright}{pad}</span>"  
    
    @staticmethod
    def int_to_hex_string(num):
        return str(hex(num)).removeprefix("0x").zfill(6)
    
    _special_chars = {True: "🟡", False: "⚫"}

    def get_special(self, key = None):
        return type(self)._special_chars.get(key, "🚫")
    # End TrisLabel class

#class PropWidget(Gtk.Box):
#    def __init__(self, property, idx):
#        super().__init__(self)

    
class PorcusDialog(GimpUi.Dialog):
    def __init__(self, tris_manager):
        super().__init__(self)
        self.set_border_width(10)
        self.tris_manager = tris_manager
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Done (Save)", Gtk.ResponseType.OK)
        
        left_box, right_box = self.generate_containers()

        self.widget_list = []
        
        for idx, prop in enumerate(tris_manager.gamedata["thingProps"]):
            summary_widget = self.generate_summary_widget(prop, idx)
            left_box.pack_start(summary_widget, True, True, 0)
            
            right_w = self.generate_tool_widget(prop, idx)
            self.widget_list.append(right_w)
            right_box.pack_start(right_w, True, True, 0)
        #test separator:
        #temp_sep = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        #print(temp_sep.get_visible())
        #temp_sep.show()
        #left_box.pack_start(temp_sep, False, True, 0)
        # end PorcusDialog's __init__

    @staticmethod
    def show_tool_widget(button , wlist):
        for elem in wlist:
            elem.hide()
        wlist[button.idx].show()
    def generate_tool_widget(self, param, idx):
        return Gtk.Label.new(f"[Prop #{param} label]")
    def generate_summary_widget(self, param, idx):
            toggle_prop_tools_button = GimpUi.Button.new_with_label(f"Prop-{param} ->")
            toggle_prop_tools_button.idx = idx
            toggle_prop_tools_button.connect('clicked', self.show_tool_widget, self.widget_list)
            toggle_prop_tools_button.show()
            return toggle_prop_tools_button
    def generate_containers(self):
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left_box.set_name("Summary Box")
        left_box.show()

        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        right_box.set_name("Tools Box")
        right_box.show()
        
        ulteriore = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        ulteriore.set_name("Ulteriore")
        ulteriore.show()
        ulteriore.pack_start(left_box, True, True, 4)
        ulteriore.pack_start(right_box, True, True, 4)

        self.get_content_area().pack_start(ulteriore, True, True, 4)
        self.get_content_area().set_name("Dialog Content Area")
        return left_box, right_box


#dialogazzo = PorcusDialog()
#dialogazzo.show_all()
#dialogazzo.run()
#dialogazzo.destroy()


'''
class WidgetTree:
    def __init__(self, root_dir):
        self._generator = _TreeGenerator(root_dir)
    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)

class _TreeGenerator:   
    def __init__(self, root_dir):
        self._root_dir = root_dir #pathlib.Path(root_dir)
        self._tree = []
        self.PIPE = "│"
        self.ELBOW = "└──"
        self.TEE = "├──"
        self.PIPE_PREFIX = "│   "
        self.SPACE_PREFIX = "    "
    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree
    def _tree_head(self):
        self._tree.append(f"{self._root_dir}")
        self._tree.append(self.PIPE)
    def _tree_body(self, directory, prefix=""):
        entries = directory.get_children() #directory.iterdir()
        entries = sorted(entries, key=lambda entry: not hasattr(entry, 'get_children')) #entry.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            if hasattr(entry, 'get_children'):
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)
    
    def _add_directory(self, directory, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {directory.get_name()}")
        if index != entries_count - 1:
            prefix += self.PIPE_PREFIX
        else:
            prefix += self.SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())
    
    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.get_name()}")

#widget =
#WidgetTree(widget).generate()
'''
