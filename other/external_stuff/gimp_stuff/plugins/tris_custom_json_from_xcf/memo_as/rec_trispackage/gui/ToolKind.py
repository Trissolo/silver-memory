import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#from ..summary_stuff.TrisSummary import TrisSummary

class ToolKind():
    def __init__(self, property, azzus):
        print("CAMARONNAAAAAAAAAAAAAAAAAAAAAAAAAAAA", super())

        from ..splitted_gamedata.gamedata_grabber import names
        super().__init__('kind')
        self.names = names["kind"]
        #self.right_div = self.build_radio_buttons(self.handler)
        #self.div.pack_end(self.right_div, True, True, 2)

        # end INIT
    def handler(self, button):
        print(button)

    def make_div(self):
        div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2) #Gtk.Orientation.VERTICAL, 2)
        div.set_name("KindBox")
        div.show()
        return div
    
    def build_radio_buttons(self, on_button_toggled):
        div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2) #Gtk.Orientation.VERTICAL, 2)
        div.set_name("KindBox")
        div.show()

        sub_divs=[]
        for n in range(2):
            subdiv =Gtk.Box.new(Gtk.Orientation.VERTICAL, 2)
            subdiv.show()
            sub_divs.append(subdiv)

        prev = Gtk.RadioButton.new_from_widget(None)
        prev.set_label("Nothing")
        prev.set_name("Nothing")
        prev.value = None
        fake_radio = prev

        for numeric_value in self.names:
            if type(numeric_value) is int:
                kind_name = self.names[numeric_value]
                button = Gtk.RadioButton.new_from_widget(prev)
                button.set_label(f"{kind_name.capitalize()} ({numeric_value})")
                button.set_name(kind_name)
                button.value = numeric_value
                button.connect("toggled", on_button_toggled)
                sub_divs[numeric_value & 1].pack_start(button, False, False, 0)
                button.show()
                prev = button
                return div