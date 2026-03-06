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
        super().__init__(*args)
        
        #0 the Dialog button:
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.connect("destroy", self._on_destroy)

        #1 Set the Image and Current Layer:
        self.infuse_image(image)
        #self.update_layer()

        #2 Generate the Top Bar
        self.generate_top()
        #self.top_bar_write(f"Done! ({self.layer.get_name()})")

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
