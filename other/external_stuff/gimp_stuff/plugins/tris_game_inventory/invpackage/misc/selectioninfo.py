import gi

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
