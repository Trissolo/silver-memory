import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp

# Grab Gtk and Gdk for 'copy to clipboard' method:
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class GenericUtils():
    def _load_local_json(self, name_file):
        import json
        from gi.repository import GLib
        directory_separator = GLib.DIR_SEPARATOR_S
        filepath = GLib.path_get_dirname(__file__)
        wanted = "other"
        basedir = f"{filepath[0:filepath.index(wanted)]}src/game/gamedata"

        if type(name_file) is str:
            name_file = [name_file]
        
        res = []
        
        for filename in name_file:
            path_as_str = f"{basedir}{directory_separator}{filename}.json"
            assert GLib.file_test(path_as_str, GLib.FileTest.EXISTS), f"The file '{filename}.json' does not exist. Aborting."
            with open(path_as_str) as json_file:
                res.append(json.load(json_file))
        
        # check for duplicates
        duplicates = []
        for current_array, current_name in zip(res, name_file):
            temp_set = set(current_array)
            if len(current_array) != len(temp_set):
                duplicates.append([f'❌ {current_name}.json  Not unique: "{c}".' for c in temp_set if current_array.count(c) != 1])

        if len(duplicates):
            self.output_message("\n".join(*duplicates)) # self.output_message(f"Duplicates:\n{'\n'.join(duplicates)}")


        return res[0] if len(res) == 1 else res
    
    def load_json_vars(self):
        return self._load_local_json(["bool", "crumble", "nibble", "byte"])
    def load_json_hovernames(self):
        return self._load_local_json("hovernames")
    
    @staticmethod
    def output_message(text):
        # MessageHandlerType.MESSAGE_BOX = 0, CONSOLE = 1, ERROR_CONSOLE = 2
        Gimp.message_set_handler(Gimp.MessageHandlerType.MESSAGE_BOX)
        Gimp.message(text)
        Gimp.message_set_handler(Gimp.MessageHandlerType.CONSOLE)
        return True
    
    @staticmethod
    def output_string_to_clipboard(text = "Nothing"):
        # gi.require_version("Gtk", "3.0")
        # from gi.repository import Gtk
        # gi.require_version('Gdk', '3.0')
        # from gi.repository import Gdk
        tempcl = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        tempcl.set_text(text, -1)
        return True
