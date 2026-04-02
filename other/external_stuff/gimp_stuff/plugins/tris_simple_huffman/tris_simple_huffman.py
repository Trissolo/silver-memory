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
            print(f'Last bit was incomplete (idx was {i}')
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
    
    def __repr__(self):
        return f'[Node] {{is_leaf: {self.is_leaf()}{f", char: {self.char}" if self.char else ""}}}'


# 3. the Encoder Class


class HufEncoder:
    def __init__(self, file, folder, user_string):
        self._file = file

        self._user_string = user_string

        file_name = "default" if len(user_string) != 0 else file.get_basename()[:-4]

        self.output_path = f'{folder.get_path()}{GLib.DIR_SEPARATOR_S}{file_name}.thf'

        # string encoding stuff
        self._decode_list = ['cp1252', 'windows-1252', 'ascii', 'raw_unicode_escape', 'utf-8']
        self.decode_idx = 0
        self.string_encoding = self._decode_list[self.decode_idx]

        #self.text now is a property

        # the Huffman tree (nodes containing nodea)
        self.root = self.build_huffman_tree(self.text)

        # the dictionary (key -> string of zeroes and ones, value -> a one sized string with the char)
        self.huffman_dict = {}

        # our Writer
        self.writer = StreamGen()

    @property
    def text(self):
        return self._file_content() 
       
    def _file_content(self):
        to_process = None
        if len(self._user_string) != 0:
            to_process = self._user_string
        else:
            success, content, etag = self._file.load_contents(None)
            to_process = content.decode(self.string_encoding)
        
        for char in to_process:
            yield char
      
    # def _file_length(complete_path):
    #     count = 0
    #     for row in open(complete_path, "r"):
    #         count += len(row)
    #     return count

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
        # print(f"🪝 {node}")
        # if not node:
        #     print("🏁 No node: returning")
        #     return
        if node.is_leaf():
            writer.addBit(1)
            writer.addChar(node.get_char())
        else:
            writer.addBit(0)
            self.preorder_traversal(node.left, writer)
            self.preorder_traversal(node.right, writer)

    def execute(self):
        self.generate_codes(self.root, "", self.huffman_dict)
        
        self.preorder_traversal(self.root, self.writer)

        for char in ''.join(self.huffman_dict[char] for char in self.text):
            self.writer.addBit(char)
        
        return self.writer.get_output()

        
        
    # def huffman_encoding(self):
    #     text = self.text
    #     huffman_dict = self.huffman_dict
    #     self.generate_codes(self.root, "", huffman_dict)
    #     encoded_text = ''.join(huffman_dict[char] for char in text)
    #     return encoded_text
                
    

# 4. the Plugin class
class TrisHuffman(Gimp.PlugIn):
    ARGU_DEST_FOLDER = 'dest-folder'
    ARGU_FILE_TO_COMPRESS = 'file-to-compress'
    ARGU_TEST_STRING = 'test-string'
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
            self.ARGU_FILE_TO_COMPRESS,  # const gchar* name,
            "The text file to compress",  # const gchar* nick,
            None,  # const gchar* blurb,
            Gimp.FileChooserAction.OPEN,  # GimpFileChooserAction action,
            True,  # gboolean none_ok,
            None,  # GFile* default_file,
            GObject.ParamFlags.READWRITE #READABLE,  # GParamFlags flags
        )

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

        procedure.add_string_argument (
            #GimpProcedure* procedure,
            self.ARGU_TEST_STRING, #const gchar* name,
            'The string to compress (the file will be ignored)',  #const gchar* nick,
            'blurb for test string', #const gchar* blurb,
            'ARGU_STRING_value',     #const gchar* value,
            GObject.ParamFlags.READWRITE #GParamFlags flags
        )

        return procedure
    
    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # initialize Gtk!
        GimpUi.init(GLib.path_get_basename(__file__).removesuffix(".py"))
        
        print("*** Simple Huffman Encoder Plugin ***")
        options_dialog = GimpUi.ProcedureDialog.new(procedure, config, "title_test")
        options_dialog.fill()
        user_action = options_dialog.run()
        
        folder = config.get_property(self.ARGU_DEST_FOLDER)
        source_file = config.get_property(self.ARGU_FILE_TO_COMPRESS)
        user_string = config.get_property(self.ARGU_TEST_STRING)
        options_dialog.destroy()

        # from HERE!
        if user_action:      
            test_huff = HufEncoder(source_file, folder, user_string)
        
            res = test_huff.execute()

            with open(test_huff.output_path, "wb") as binary_file:
                binary_file.write(bytes(res))
        
            Gimp.message(f'Done!\nWrote: {test_huff.output_path}')

        print('(Huffman Done)')
        # do what you want to do, then, in case of success, return:
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    

Gimp.main(TrisHuffman.__gtype__, sys.argv)


'''
console.clear();
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
      
        let padding = this.getAdjacentBits(8);
        
        console.log("padding", padding, total_len)

        // Reconstruct the Huffman tree
        const root = this.decodeTree();

        // Get the character-code map back
        const dictionary = this.assign_code(root, '');

        console.log(dictionary);
   		
		// Decode!
        const output = [];

        let code = "";

        const process = () => {
          
        	code += this.getBit().value;
            
            if (dictionary.has(code))
            {
                output.push(dictionary.get(code));

                code = "";
            }
        }

        while (this.processedBytes < total_len)
        {
            process()    
        }

        if (padding)
        {
            while (padding--)
            {
                process()
            }
        }
      
        // destroy
        this.bitstream.return();
      
        this.bitstream = undefined;
      
        // manage output
        console.log(output.join('')); 
    }

    *bitGenerator(typedArray)
    {
        for (const byte of typedArray)
        {
            this.processedBytes += 1;
          
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
}  // End DecodeHuffman

class TestScene extends Phaser.Scene
{
 
  constructor ()
  {
    super({ key: 'TestScene' });
  }

preload()
    {
        //this.load.binary('mio', 'assets/promessi.thf', Uint8Array);
        this.load.binary('mio', 'assets/coso.thf', Uint8Array);
        // this.load.binary('mio', 'assets/default.thf', Uint8Array);
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

window.game = new Phaser.Game(config);
'''