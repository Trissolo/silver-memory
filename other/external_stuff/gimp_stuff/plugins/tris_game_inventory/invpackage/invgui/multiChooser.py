import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# 
from .singleChooser import SingleChooser

class MultiChooser(Gtk.Box):
    def __init__(self, source_ary):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.set_name("vars")
        self.source = source_ary
        self.bnames = bnames = ["Bool", "Crumble", "Nibble", "Byte"]
        # stack
        stack = Gtk.Stack.new()
        stack.set_transition_type(Gtk.StackTransitionType.NONE)
        for idx, ary in enumerate(source_ary):
            #print(f"MULTI: [{idx}]:\n{ary}\n")
            c = SingleChooser(ary, idx)
            #c.idx = idx
            name = bnames[idx]
            c.set_name(name)
            #print(c.get_name())

            # condition stuff
            bits_amount = 1 << idx
            c.maximum = (1 << bits_amount) -1
            stack.add_titled(c, name, f"{name} (0-{(1<<bits_amount)-1})")
            #stack.add_named(c, name)
        
        #stack.add_titled(label, "label", "A label")

        stack_switcher = Gtk.StackSwitcher.new()
        stack_switcher.set_stack(stack)

        self.pack_start(stack_switcher, False, False, 0)
        self.pack_start(stack, True, True, 0)
        print(f"MultiChooser childrens:") # {self.get_children()[1].get_visible_child().idx}")
        [print(f"{i}) {c.get_name()}") for i, c in enumerate(self.get_children())]

        self.add_condition_widgets(stack_switcher)
        self.show_all()
        return
    def get_stack(self):
        return self.get_children()[1]
    def get_listboxes(self):
        return (sc.get_listbox() for sc in self.get_stack().get_children())
    
    def get_actual_visible(self):
        #return self.get_stack().get_visible_child()
        return self.get_children()[1].get_visible_child()
    def get_bottom_box(self):
         return self.get_children()[2]
    def deduce_bottom_box_visibility_by_size(self, size):
        #print(f'Receiving {size}, so the bottom box visibility will be set to {size==3}')
        self.get_bottom_box().set_visible(size==3)
        return self
    def get_spinbutton(self):
        #print("HARDCODED Accessing:", self.get_bottom_box().get_children()[1].get_name())
        return self.get_bottom_box().get_children()[1]
    def get_confirm_button(self):
        return self.get_bottom_box().get_children()[2]
    def get_condition_preview_label(self):
        return self.get_bottom_box().get_children()[0]
    # def get_kind_from_child(self):
    #         return self.get_actual_visible().idx
    def radiobutton_on_changed(self, radiobutton):
            if radiobutton.get_active():
                spinbutton = self.get_spinbutton()
                #print(f"Funziona? {spinbutton.get_value_as_int()}")
                spinbutton.set_value(0)
                spinbutton.set_range(0, self.get_actual_visible().maximum)
    def on_confirm_clicked(self, button):
        retrieved_spinbutton = button.get_parent().get_children()[1]
        print(f"{button.get_parent() is self.get_bottom_box()=}")
        value = retrieved_spinbutton.get_value_as_int()
        print(f"Confirming: {value}")
        label, spin_button, confirm_button = button.get_parent().get_children()
        print("Relative children 👀 2")
        print(label.get_name())
        print(spin_button.get_name())
        # test hiding entire widget:
        # if value == 99: 
        #     button.get_parent().get_parent().hide()
        #     fr = button.get_name()
        #     wid = button
        #     while not wid.get_name() == "az":
        #         wid = wid.get_parent()
        #     print(f"From: {fr}")
        #     wid.greet()
    def get_readable(self, arr, size):
        print("get_readable", arr)
        zero = arr[0]
        uno = arr[1]
        res = f"{self.source[zero][uno]} ({self.bnames[zero]})"
        return res
    def add_condition_widgets(self, stack_switcher):
        spinbutton = Gtk.SpinButton.new(Gtk.Adjustment.new(0, 0, 1, 1, 0, 0), 1, 0)
        spinbutton.set_name("SPIN BUTTON")
        spinbutton.set_width_chars(3)
        spinbutton.set_valign(Gtk.Align.START)
        conf_button = Gtk.Button.new_with_label("🔸")
        conf_button.set_valign(Gtk.Align.START)
        conf_button.set_name("CONFIRM COND. Button")
        #conf_button.connect('clicked', self.on_confirm_clicked)

        cond_label = Gtk.Label.new("[ 1, 3, None]")
        cond_label.set_valign(Gtk.Align.START)

        bottom_div = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)
        bottom_div.pack_start(cond_label, False, False, 0)
        bottom_div.pack_start(spinbutton, False, False, 0)
        bottom_div.pack_start(conf_button, False, False, 0)

        self.pack_start(bottom_div, True, True, 0)
        bottom_div.show_all()
        print("🔁 AFTER")
        [print(f"{i}) {c.get_name()} - {c.__class__.__name__}") for i, c in enumerate(bottom_div.get_children())]
        print("Ri. 🔄 ")
        [print(f"{i}) {c.get_name()} - {c.__class__.__name__}") for i, c in enumerate(self.get_children())]


        #self.pack_start(spinbutton, True, True, 0)
        for b in stack_switcher.get_children():
            b.connect('clicked', self.radiobutton_on_changed)