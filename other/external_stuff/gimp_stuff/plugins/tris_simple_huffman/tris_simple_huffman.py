#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio

import heapq
from collections import Counter

# 1. The Bit reader/writer class
class StreamGen():
    def __init__(self):
        self.byte = 0
        self.idx = 0
        self.res = []
        self._allowed = {0, 1, '0', '1'}
        self.usable = dict()
        [self.usable.update({chr(n): f'{n:08b}'}) for n in range(8, 256)]
    def reset(self):
        self.byte = 0
        self.idx = 0
    def clearAll(self):
        self.reset()
        self.res.clear()
    @staticmethod
    def _integer_to_string(num):
        return f'{num:08b}'
    def addBit(self, bit = 0):
        if bit not in self._allowed:
            return
        if type(bit) is str:
            bit = 0 if bit == '0' else 1
        self.byte <<= 1
        self.idx +=1
        if bit:
            self.byte |= 1
        if self.idx == 8:
            self.res.append(self.byte)
            self.reset()
    def addChar(self, c):
        if c in self.usable:
            # print(f'{c=}')
            for bas in self.usable.get(c):
                self.addBit(bas)
        else:
            print(f"ERROR! :( char: {c}")
    def get_output(self):
        self.finalize()
        # for i, byte in enumerate(self.res):
        #     print(f'{i} {byte:08b} {byte:>3}')
        return self.res
    def finalize(self):
        if self.idx != 0:
            i = self.idx
            print(f'Last bit is incomplete. Idx = {i}')
            self.byte <<= (8 - i)
            self.res.append(self.byte)
            self.res.insert(0, i)

# 2. the node class
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq
    
    def is_leaf(self):
        return self.left is None # and self.right is None

    def get_char(self):
        return self.char


# 3. the Encoder Class


class HufEncoder:
    def __init__(self, file):
        self._file = file
        self._decode_list = ['utf-8', 'windows-1252']
        self.decode_idx = 1
        #self.text = text
        self.root = self.build_huffman_tree(self.text)
        self.huffman_dict = {}
        self.writer = StreamGen()

    @property
    def text(self):
        return self._file_content() 
       
    def _file_content(self):
        success, content, etag = self._file.load_contents(None)
        for char in content.decode(self._decode_list[self.decode_idx]):
            yield char
      
    def _file_length(complete_path):
        count = 0
        for row in open(complete_path, "r"):
            count += len(row)
        return count

    def build_huffman_tree(self, text):
        frequency = Counter(text)
        heap = [Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        return heap[0]

    def generate_codes(self, node, prefix, huffman_dict):
        if node:
            if node.char is not None:
                huffman_dict[node.char] = prefix
            self.generate_codes(node.left, prefix + "0", huffman_dict)
            self.generate_codes(node.right, prefix + "1", huffman_dict)
    
    def preorder_traversal(self, node, writer):  # ENCODE TREE FOR HEADER
        if node.is_leaf():
            writer.addBit(1)
            writer.addChar(node.get_char())
        else:
            writer.addBit(0)
            self.preorder_traversal(node.left, writer)
            self.preorder_traversal(node.right, writer)

        if not node:
            return
        
    def huffman_encoding(self):
        text = self.text
        huffman_dict = self.huffman_dict
        self.generate_codes(self.root, "", huffman_dict)
        encoded_text = ''.join(huffman_dict[char] for char in text)
        return encoded_text
                
    

# 4. the Plugin class
class TrisHuffman(Gimp.PlugIn):
    ARGU_DEST_FOLDER = 'dest-folder'
    ARGU_FILE_TO_COMPRESS = 'file-to-compress'
    def do_query_procedures(self):
        return [ "tris-simple-huffman" ]
    def do_set_i18n (self, name):
        return False
    def do_create_procedure(self, name="tris-simple-huffman"):
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)
        #procedure.set_image_types("*")
        procedure.set_menu_label("[Tris] 🗜️ Simple Huffman Encoder")
        procedure.add_menu_path( '<Image>/Filters/[[Tris]]/' )
        procedure.set_documentation("Simple Huffman Encoder", "A simple Huffman Encoder fortext files", name)
        procedure.set_attribution("Tris", "att_name", "2026")
        procedure.add_file_argument(
            # GimpProcedure* procedure,
            self.ARGU_DEST_FOLDER,  # const gchar* name,
            "Destination folder for the compressed file",  # const gchar* nick,
            None,  # const gchar* blurb,
            Gimp.FileChooserAction.SELECT_FOLDER,  # GimpFileChooserAction action,
            True,  # gboolean none_ok,
            None,  # GFile* default_file,
            GObject.ParamFlags.READWRITE,  # GParamFlags flags
        )
        procedure.add_file_argument(
            # GimpProcedure* procedure,
            self.ARGU_FILE_TO_COMPRESS,  # const gchar* name,
            "The text file to compress",  # const gchar* nick,
            None,  # const gchar* blurb,
            Gimp.FileChooserAction.OPEN,  # GimpFileChooserAction action,
            True,  # gboolean none_ok,
            None,  # GFile* default_file,
            GObject.ParamFlags.READWRITE #READABLE,  # GParamFlags flags
        )
        return procedure
    
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # initialize Gtk!
        GimpUi.init(GLib.path_get_basename(__file__).removesuffix(".py"))
        
        print("*** Simple Huffman Encoder Plugin ***")
        options_dialog = GimpUi.ProcedureDialog.new(procedure, config, "title_test")
        options_dialog.fill()
        options_dialog.run()
        options_dialog.destroy()

        folder = config.get_property(self.ARGU_DEST_FOLDER)
        source_file = config.get_property(self.ARGU_FILE_TO_COMPRESS)
                

        #from HERE!
        test_huff = HufEncoder(source_file)

        test_huff.generate_codes(test_huff.root, "", test_huff.huffman_dict)
        
        test_huff.preorder_traversal(test_huff.root, test_huff.writer)

        encoded_text = ''.join(test_huff.huffman_dict[char] for char in test_huff.text)

        for char in encoded_text:
            test_huff.writer.addBit(char)
        
        print(f'{folder.get_path()}]\n{source_file.get_basename()[:-4]}')

        res = test_huff.writer.get_output()

        with open(f'{folder.get_path()}{GLib.DIR_SEPARATOR_S}{source_file.get_basename()[:-4]}.thf', "wb") as binary_file:
            binary_file.write(bytes(res))
        
        Gimp.message(f"{res}")



        # do what you want to do, then, in case of success, return:
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    
    # def read_text(self, file):
    #     try:
    #         # Carica il contenuto. Restituisce (successo, byte_content, etag)
    #         success, content, etag = file.load_contents(None)
            
    #         if success:
    #             # Il contenuto viene restituito come byte, quindi va decodificato in stringa
    #             text_content = content.decode('utf-8')
    #             print(text_content)
    #     except Exception as e:
    #         print(f"Errore durante la lettura del file: {e}")
    #def get_content(self, file):
        success, content, etag = file.load_contents(None)

        # Qui il file è già chiuso lato sistema operativo.
        # Puoi elaborare 'content' senza preoccuparti di altro.
        # ['utf-8', 'windows-1252']
        # print(content.decode('utf-8'))
    # def cheppa(self, file):
    #     try:
    #         # 2. Apri lo stream di lettura (FileInputStream)
    #         input_stream = file.read(None)
            
    #         # 3. Avvolgi lo stream in un DataInputStream per leggere le righe
    #         data_stream = Gio.DataInputStream.new(input_stream)
            
    #         while True:
    #             # 4. Leggi la riga. Restituisce (linea_in_byte, lunghezza)
    #             line_bytes, length = data_stream.read_line(None)
                
    #             # Se line_bytes è None, abbiamo raggiunto la fine del file (EOF)
    #             if line_bytes is None:
    #                 break
                    
    #             # Decodifica i byte in stringa (rimuovendo eventuali spazi/newline extra se necessario)
    #             line_text = line_bytes.decode('utf-8')
    #             print(line_text)

    #         # Chiudi lo stream una volta finito
    #         input_stream.close(None)

    #     except Exception as e:
    #         print(f"Errore durante la lettura: {e}")

Gimp.main(TrisHuffman.__gtype__, sys.argv)



'''
const {clear, log, dir} = console;

class Node
{
    constructor(char = null, left = null, right = null)
    {
        this.char = char;
        this.left = left;
        this.right = right;
    }

    is_leaf()
    {
        return this.left === null;
    }

    get_char()
    {
        return this.char;
    }
}

class DecodeHuffman
{
    processedBytes = 0;
    bitstream;
  
    constructor(file)
    {
        this.bitstream = this.bitGenerator(file);
        const total_len = file.length;
        const padding = file[0]
        this.getAdjacentBits(8)
        console.log("padding", padding, total_len)

        // skips the control bit set by the compression algorithm
        //this.getBit();

        // Reconstruct the Huffman tree
        const root = this.decodeTree();

        // Get the character-code map back
        const dictionary = this.assign_code(root, '');

        console.log(dictionary);
   		
        //const padding = this.getAdjacentBits(8);

        //this.getAdjacentBits(padding);

        const output = [];

        let code = "";

        //let position = {done: false};

        while (this.processedBytes < total_len)
        {
            
            code += this.getBit().value;
            
            if (dictionary.has(code))
            {
                output.push(dictionary.get(code));

                code = "";
            }
        }
      
        for (let i = 0; i < padding; i++)
        {
          code += this.getBit().value;
            
            if (dictionary.has(code))
            {
                output.push(dictionary.get(code));

                code = "";
            }
        }

        // destroy
        this.bitstream.return();
        this.bitstream = undefined;
        
        console.log(output.join(''));
        
    }

    *bitGenerator(typedArray)
    {
        for (const byte of typedArray)
        {
          this.processedBytes += 1;
          //console.log(this.processedBytes);
            // console.log("Byte", byte);
            // Iterate bits from Most Significant to Least Significant
            for (let i = 7; i >= 0; i--)
            {
                yield (byte >> i) & 1;
            }
          
        }
    }

    getBit() 
    {
        return this.bitstream.next();
    }
    getAdjacentBits(amount)
    {
        let bits = 0;

        for (let i = 0; i < amount; i++)
        {
            bits <<= 1;

            bits |= this.getBit().value;
        }

        return bits;
    }

    decodeTree()
    {
        const char = this.getBit().value;

        if (char == 1)
        {
            return new Node(String.fromCharCode(this.getAdjacentBits(8)));
        }

        else
        {
            const left = this.decodeTree();
            const right = this.decodeTree();
            return new Node(null, left, right);
        }
    }

    assign_code(node, code = '')
    {
        if (node.is_leaf())
        {
            return new Map().set(code, node.get_char());
        }

        return new Map([...this.assign_code(node.left, code + '0'), ...this.assign_code(node.right, code + '1')]);
        
    }
}
class TestScene extends Phaser.Scene
{
 
  constructor ()
  {
    super({ key: 'TestScene' });
  }

preload()
    {
        this.load.binary('mio', 'assets/promessi.thf', Uint8Array);
        // this.load.binary('mio', 'assets/lorem.bin', Uint8Array);
        // this.load.binary('mio', 'assets/large_text.bin', Uint8Array);
        // this.load.binary('mio', 'assets/commedia.bin', Uint8Array)
    }

    create()
    {
       new DecodeHuffman(this.cache.binary.get('mio'));
    }
} // end TestScene
    
const config = {
    type: Phaser.WEBGL,
    parent: "gameContainer",
    pixelArt: true,
    backgroundColor: '#320822',
    scale: {
        mode: Phaser.Scale.NONE,
        //autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 200,
        height: 200,
        zoom: 2
    },
    //loader: {
    //  baseURL: 'https://labs.phaser.io/',
    //  baseURL: 'https://i.ibb.co/YhGPn4S',
    //  crossOrigin: 'anonymous'
    //},
    scene: [TestScene]
};

window.game = new Phaser.Game(config)

'''
