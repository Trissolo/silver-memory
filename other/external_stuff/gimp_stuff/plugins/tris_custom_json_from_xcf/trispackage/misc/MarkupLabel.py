
import gi

#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp

#gi.require_version("GimpUi", "3.0")
#from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MarkupLabel(Gtk.Label):
    def __init__(self, text = "My MarkupLabel"):
        super().__init__()
        self.set_use_markup(True)
        self.set_name(f"MarkupLabel {text}")
        self.last_entered_raw_text = ""
        self.set_default_text(f" {text}")
        self.show()
        #alias?
        self.set_text = self.write
    
    def set_default_text(self, text):
        self.default_text = text
    
    def write(self, text = None, color=None, bgcolor=None, size=100, width=0, align="<", monospace=False, italic=False, bold = False):
        if text is None: text = self.default_text
        self.last_entered_raw_text = text
        self.set_markup(type(self).assemble_span(text, color, bgcolor, size, width, align, monospace, italic, bold))
    
    @classmethod
    def assemble_span(cls, text, color=None, bgcolor=None, size=100, width=0, align = "<", monospace=False, italic=False, bold=False):
        if width > 0: text = f"{text:{align}{width}}"
        color = f'color="#{cls.int_to_hex_string(color)}"' if type(color) == int else ""
        bgcolor = f'bgcolor="#{cls.int_to_hex_string(bgcolor)}"' if type(bgcolor) == int else ""
        size = f'size="{size}%"' if type(size) == int else ""
        if italic: text = f"<i>{text}</i>"
        if bold: text = f"<b>{text}</b>"
        if monospace: text = f"<tt>{text}</tt>"
        return f"<span {color} {bgcolor} {size}>{text}</span>"  
    
    @staticmethod
    def int_to_hex_string(num):
        return str(hex(num)).removeprefix("0x").zfill(6)
    _special_chars = {True: "🟡", False: "⚫"}
    def get_special(self, key = None):
        return type(self)._special_chars.get(key, "🚫")
    # End TrisLabel class
