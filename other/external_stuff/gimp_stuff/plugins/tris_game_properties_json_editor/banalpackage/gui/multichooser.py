import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .singlechooser import SingleChooser

class MultiChooser(Gtk.Box):
    def __new__(cls, fake_a, fake_b):
        return super(MultiChooser, cls).__new__(cls)
    def __init__(self, source_ary, names):
        super().__init__(homogeneous=False, spacing=2)
        self.set_orientation(1)
        #self.lettererichieste = ""
        stack = Gtk.Stack.new()
        stack.set_transition_type(Gtk.StackTransitionType.NONE)
        for idx, ary in enumerate(source_ary):
            print(f"MULTI: [{idx}]:\n{ary}\n")
            c = SingleChooser(ary)
            c.idx = idx
            name = names[idx]
            c.set_name(name)
            print(c.get_name())
            bits_amount = 1<<idx
            c.maximum = (1<<bits_amount)-1
            stack.add_titled(c, name, f"{name} (0-{(1<<bits_amount)-1})")
            #stack.add_named(c, name)
        
        #stack.add_titled(label, "label", "A label")

        stack_switcher = Gtk.StackSwitcher.new()
        stack_switcher.set_stack(stack)

        self.pack_start(stack_switcher, False, False, 0)
        self.pack_start(stack, True, True, 0)
        print(f"MultiChooser childrens: {self.get_children()[1].get_visible_child().idx}")
        self.show_all()

        spinbutton = Gtk.SpinButton.new(Gtk.Adjustment.new(0, 0, 1, 1, 0, 0), 1, 0)
        spinbutton.set_name("SPIN BUTTON")
        spinbutton.set_width_chars(3)
        spinbutton.set_valign(Gtk.Align.START)
        #spinbutton.show()
        conf_button = Gtk.Button.new_with_label("🔸")#Accept")
        conf_button.set_valign(Gtk.Align.START)
        conf_button.connect('clicked', self.on_confirm_clicked)
        bottom_div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        bottom_div.pack_start(spinbutton, False, False, 0)
        bottom_div.pack_start(conf_button, False, False, 0)
        bottom_div.show_all()

        #self.pack_start(spinbutton, True, True, 0)
        self.pack_start(bottom_div, True, True, 0)
        for b in stack_switcher.get_children():
            #b.connect('group-changed', self.radiobutton_on_changed)
            b.connect('clicked', self.radiobutton_on_changed)
    def get_actual_visible(self):
        return self.get_children()[1].get_visible_child()
    def get_bottom_box(self):
         return self.get_children()[2]
    def get_spinbutton(self):
         print("Accessing:", self.get_bottom_box().get_children()[0].get_name())
         return self.get_bottom_box().get_children()[0]
    def get_kind_from_child(self):
            return self.get_actual_visible().idx
    def radiobutton_on_changed(self, radiobutton):
            if radiobutton.get_active():
                spinbutton = self.get_spinbutton()
                #print(f"Funziona? {spinbutton.get_value_as_int()}")
                spinbutton.set_value(0)
                spinbutton.set_range(0, self.get_actual_visible().maximum)
    def on_confirm_clicked(self, button):
         retrieved_spinbutton = button.get_parent().get_children()[0]
         value = retrieved_spinbutton.get_value_as_int()
         print(f"Confirming: {value}")
         # test hiding entire widget:
         if value == 100:
              button.get_parent().get_parent().hide()
