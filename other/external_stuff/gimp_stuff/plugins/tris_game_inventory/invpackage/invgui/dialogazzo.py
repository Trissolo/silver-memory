import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

gi.require_version("GimpUi", "3.0")
from gi.repository import GimpUi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class PixelBitstream():
    def __init__(self, layer):
        self.layer = layer
        self.x = 0
        self.y = 0
        self.width = layer.get_width()
        self.end = False
        self.bitstream = []
    def advance(self):
        self.x += 1
        if self.x == self.width:
            self.x = 0
            self.y += 1
    def get_byte(self):
        byte = 0
        for i in range(8):
            value = self.layer.get_pixel(self.x, self.y)
            byte <<= 1
            if value is None and not self.end:
                self.end = True
            if value and value.get_rgba().red == 1.0:
                byte |= 1
            #byte |= 0 if (self.end is True or value.get_rgba().red) == 0.0 else 1
            self.advance()
        return self.bitstream.append(byte)
    def start(self):
        while not self.end:
            self.get_byte()
        self._result(self.bitstream)
        return self.bitstream
    def destroy(self):
        self.layer = None
        self.bitstream = self.bitstream.clear()
        return None
    def _result(self, res):
        str_stream = "".join([f"{elem:0>8b}" for elem in res])
        k = self.width
        chunks = [str_stream[i:i+k] for i in range(0, len(str_stream), k)]
        for elem in chunks:
            print(elem)
        return str_stream
        

'''
class Example extends Phaser.Scene
{
    base = [255, 129, 185, 165, 165, 185, 129, 255, 0];
    oriX = 8;
    oriY = 8;

    create ()
    {
        console.log(this.base.length)// === this.oriX * this.oriY)
        
        const buffer = new Uint8Array(this.oriX * this.oriY*4);//this.base.length * 4); //this.cache.binary.get('mod');
        let idx = 0
        for (const elem of this.base)
        {
            //console.log(elem.toString(2))
            for (const char of elem.toString(2).padStart(8, "0"))
            {
                //console.log(char)
                
                const val = char === "1"? 255 : 0
                //console.log(elem, idx++)
                buffer[idx++] = val;
                buffer[idx++] = val;
                buffer[idx++] = val;
                buffer[idx++] = val;
            }
        }

        //console.log(idx, buffer.byteLength)
        
        console.log(this.textures.addUint8Array("test", buffer, this.oriX, this.oriY));

        this.add.image(20,20,'test').setOrigin(0).setScale(8);

        return false;
        
        const config = {
            image: 'test',
            width: 8,
            height: 8,
            chars: '0123456789%ab',
            charsPerRow: 13
        }
            

        this.cache.bitmapFont.add('font0', Phaser.GameObjects.RetroFont.Parse(this, config));
        
        
        this.add.bitmapText(10, 10, 'font0', "50%aaab").setScale(3).setOrigin(0);
    } 
}


const config = {
    type: Phaser.WEBGL,
    width: 800,
    height: 600,
    backgroundColor: '#2d2d2d',
    parent: 'phaser-example',
    scene: Example
};

const game = new Phaser.Game(config);
'''


'''
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


class Dialogazzo(GimpUi.Dialog):
    def __init__(self, *args):
        # First of all
        super().__init__(title="Tris Inventory Generator", *args)
        self.add_buttons( "Ok (Close)", Gtk.ResponseType.OK)
        self.connect("destroy", self._on_destroy)
        self.row_infos = []
        self.curr_sel = None
        self.build_schemino()
        self.show_all()
    def _on_destroy(self, widget):
        print("Checking row_info:", self.row_infos[0])
        for elem in self.row_infos:
            elem.clear()
        self.row_infos = self.row_infos.clear()
        self.destroy()
        print('Calling "super().destroy()"')
        super().destroy()
    def build_schemino(self):
        # self.get_content_area().pack_start(tw, False, False, 1)

        row_infos = self.row_infos

        properties_size = {
            "kind": 1,
            "hoverName": 1,
            "suffix": 2,
            "skipCond": 3,
            "noInteraction": 1,
            "roomStatus": 2,
            "roomVariable": 2
        }
        column_headers = ["Prop", "Readable", "Effective"]

        column_amount = len(column_headers)

        id_for_others = column_amount + 1

        mytypes = [str] * len(column_headers)

        cell_types = [*mytypes, str, str]

        # the Store/Model!
        store = Gtk.ListStore.new(cell_types)

        # the TreeView
        tw = Gtk.TreeView.new()

        tw.set_model(store)

        # constants AS!
        tw.text_empty = "---"
        tw.color_empty = "#343434"
        tw.color_selected = "#ff0"
        tw.color_set = "#66a"

        # populate the store:
        for idx, (prop, size) in enumerate(properties_size.items()):
            store.append([prop, tw.text_empty, tw.text_empty, tw.color_empty, tw.color_empty])
            row_infos.append(SelectionInfo(prop, size, idx, None))
        
        cell = Gtk.CellRendererText.new()

        for idx, name in enumerate(column_headers):
            col = Gtk.TreeViewColumn(name, cell, text=idx, background=3 if idx==0 else 4)
            tw.append_column(col)
        
        tw.set_activate_on_single_click(True)
        tw.connect('row-activated', self.on_active_row)
        self.get_content_area().pack_start(tw, False, False, 1)
    def on_active_row(self, liststore, row_idx, colu):
        print("On Active Row!")
        index_as_int = row_idx.get_indices()[0]
        liststore.get_selection().unselect_all()
        model = liststore.get_model()
        if self.curr_sel is not None:
            model[self.curr_sel.row_idx][3] = model[self.curr_sel.row_idx][4]
        model[index_as_int][3] = liststore.color_selected
        model[index_as_int][4] = liststore.color_empty
        self.curr_sel = self.row_infos[index_as_int]
        print(f"CurrSel: {self.curr_sel}")
        print(f"Analogies? {index_as_int=} -> {self.curr_sel.row_idx} -*- {model[row_idx][0]=} -> {self.curr_sel.prop} {model[row_idx][0]}")


dialogazzo = Dialogazzo()
#dialogazzo.destroy()
'''
