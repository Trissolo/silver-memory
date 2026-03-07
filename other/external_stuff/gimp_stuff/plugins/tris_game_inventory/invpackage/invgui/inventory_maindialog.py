import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .imagestuff import ImageStuff
from .guibargenerator import GuiBarGenerator

class InventoryDialog(GimpUi.Dialog, GuiBarGenerator, ImageStuff):
    def __init__(self, image, *args):
        # First of all
        super().__init__(*args)
        
        #0 the Dialog chores:
        self.set_title("Tris Inventory generator")
        self.set_keep_above(True)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.connect("destroy", self._on_destroy)
        self.set_name("Inv. Dialog")

        #1 Set the Image and Current Layer:
        self.image = image
        self.layer = None

        #2 the containers!
        # results = [value for num in numbers if (value := slow(num)) > 0]
        #top_bar, middle_bar = ary = [(p := Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)) for _ in range(3) if p.set_name(f'box_#{_}') is None]
        #top_bar, middle_bar = [p for name in ["Top Bar", "Middle Bar"] if (p := Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 2)) and p.set_name(name) == self.get_content_area().pack_start(p, False, True, 2)]

        #3 Populate the Top Bar
        self.generate_top_bar()

        #4 Populate the Middle Bar
        self.generate_middle_bar()

        #5 the core widgets!
        # ...

        #6 Set the Layer!
        #self.update_layer()
        # test:
        for child in self.get_content_area().get_children():
            print(child.get_name())

        #self.generate_json()
        #self.summary_debug()
    
    def set_current_prop(self):
        #self.attach_array_to_current_layer()
        return

    def _on_destroy(self, widget):
        self.remove_image_references()
        self._top_label = None
        print("Inventory plugin destroyed!")


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
