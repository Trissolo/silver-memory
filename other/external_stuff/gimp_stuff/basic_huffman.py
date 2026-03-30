import os
import timeit
import array


class Node:  # HEAP NODE CLASS
    def __init__(self, value=None, char=None, left=None, right=None):
        self.value = value
        self.char = char
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def get_value(self):
        return self.value

    def get_char(self):
        return self.char


cwd = os.getcwd()

encoding_map = ('utf-8', 'windows-1252')
encoding_idx = 1

def compress(path, mode=0):  # COMPRESS FILE DATA
    if mode == 0:
        name = str(os.path.splitext(path)[0])
        data = str(read_file(path), 'utf-8')
        freq_map = frequency_map(data)
        language_map, compressed_header = huffman_coding(freq_map)
        output = encode(data, language_map, compressed_header, mode=mode)
        output = bytes(output, 'UTF-8')
        size = create_output(output, name + ".bin", 0)
    elif mode == 1:
        os.chdir(path)
        data = bytes()
        for file in os.listdir(path):
            if file.endswith(".txt"):
                data += read_file(file, mode=0) + b'\x11\x22\x33'
        data = str(data, 'utf-8')
        freq_map = frequency_map(data)
        language_map, compressed_header = huffman_coding(freq_map)
        output = encode(data, language_map, compressed_header, mode=mode)
        output = bytes(output, 'UTF-8')
        os.chdir('..')
        size = create_output(output, os.path.basename(path) + "_compressed.bin", 0)
        os.chdir(cwd)
    return size


def frequency_map(data):  # FREQUENCY MAP GENERATOR
    frequency = {}
    for character in data:
        if character not in frequency:
            frequency[character] = 1
        else:
            frequency[character] += 1
    return frequency


def huffman_coding(freq_map):  # HUFFMAN CODING ALGORITHM
    freq_map = sorted(freq_map.items(), key=lambda x: x[1])
    nodes = []
    for key, value in freq_map:
        node = Node(value, key)
        nodes.append(node)
    while len(nodes) > 1:
        node1 = nodes[0]
        node2 = nodes[1]
        nodes = nodes[2:]
        sum_node = node1.get_value() + node2.get_value()
        node = Node(sum_node, left=node1, right=node2)
        i = 0
        while i < len(nodes) and node.get_value() > nodes[i].get_value():
            i += 1
        nodes[i:i] = [node]
    compressed_tree = encode_tree(nodes[0], "")
    d = assign_code(nodes[0], '')
    print("Byte\tCode\t\tNew code")
    for key in d.keys():
        print(str(ord(key)) + "\t\t" + f'{(ord(key)):08b}' + "\t" + str(d[key]))
    return d, compressed_tree


def encode_tree(node, code):  # ENCODE TREE FOR HEADER
    if node.is_leaf():
        code += "1"
        code += f"{ord(node.get_char()):08b}"
    else:
        code += "0"
        code = encode_tree(node.left, code)
        code = encode_tree(node.right, code)
    return code


def assign_code(node, code=''):  # ASSIGN CODES TO A HUFFMAN TREE
    if not node.left and not node.right:
        return {node.get_char(): code}
    d = dict()
    d.update(assign_code(node.left, code + '0'))
    d.update(assign_code(node.right, code + '1'))
    return d


def encode(data, language_map, compressed_header, mode=0):  # ENCODE FILE DATA INTO THEIR EQUIVALENT CODES
    compressed_header = str(mode) + compressed_header
    output = ""
    bits = ""
    for char in data:
        bits += language_map[char]
    num = 8 - (len(bits) + len(compressed_header)) % 8
    if num != 0:
        output = num * "0" + bits
    output = f"{compressed_header}{num:08b}{output}"
    return output


def create_output(data, name, mode=0):  # CREATE OUTPUT FILE
    if mode == 0:
        b_arr = bytearray()
        for i in range(0, len(data), 8):
            b_arr.append(int(data[i:i + 8], 2))
        try:
            output_path = open(name, "wb")
            output_path.write(b_arr)
            print("Success, data saved at: " + name)
            return os.stat(name).st_size
        except IOError:
            print("Something went wrong")
            exit(-1)
    else:
        try:
            output_path = open(name, "w", encoding='utf-8', newline='\n')
            output_path.write(data)
            print("Success, data saved at: " + name)
            return os.stat(name).st_size
        except IOError:
            print("Something went wrong")
            exit(-1)


def decompress(path):  # DECOMPRESS FILE DATA
    data = read_file(path, mode=1)
    data = list(data)

    mode = int(data[0])
    del data[0]

    node = decode_tree(data)
    d = assign_code(node)
    reversed_tree = {v: k for k, v in d.items()}

    n_padding = data[:8]
    n_padding = int("".join(n_padding), 2)
    data = data[8:]
    data = data[n_padding:]

    data = decode(data, reversed_tree)

    name = str(os.path.splitext(path)[0])

    if mode == 0:
        output = ""
        for num in data:
            output += format(num, '08b')

        b_arr = bytearray()

        for i in range(0, len(output), 8):
            b_arr.append(int(output[i:i + 8], 2))

        create_output(str(b_arr, 'utf-8'), name + '.txt', mode=1)
    else:
        op_files = array.array('B', data).tobytes().split(b'\x11\x22\x33')
        for i, file in enumerate(op_files[0:len(op_files) - 1]):
            create_output(str(op_files[i][:len(op_files[i])], 'utf-8'), name + str(i) + '.txt', mode=1)


def decode_tree(data):  # DECODE TREE FROM HEADER
    char = data[0]
    del data[0]

    if char == "1":
        byte = ""
        for _ in range(8):
            byte += data[0]
            del data[0]

        return Node(char=int(byte, 2))
    else:
        left = decode_tree(data)
        right = decode_tree(data)

        return Node(None, left=left, right=right)


def decode(data, language_map):  # DECODE FILE DATA FROM THEIR EQUIVALENT CODES
    code = ""
    output = []
    for bit in data:
        code += bit
        if code in language_map:
            output.append(language_map[code])
            code = ""
    return output


def read_file(path, mode=0):  # READ FILE DATA
    f = open(path, 'rb')
    if mode == 0:
        return f.read()
    else:
        data = ""
        byte = f.read(1)
        while len(byte) > 0:
            data += f"{bin(ord(byte))[2:]:0>8}"
            byte = f.read(1)
        return data

def current_encoding(idx = None):
    print(encoding_map, encoding_idx)
    return encoding_map[encoding_idx]


if __name__ == '__main__':
    run = True
    print("Enter operation type:")

    while run:
        original_size = 0
        new_size = 0
        # GET OPERATION FROM USER

        while True:
            op = input("Compression of a File (0) | Compression of a Folder (1) | Decompression (2) ")
            if op is None or op == '':
                continue
            else:
                try:
                    op = int(op)
                    if op > 2 or op < 0:
                        print("Please enter one of the mentioned options")
                        continue
                    else:
                        break
                except TypeError:
                    print("Please enter one of the mentioned options")

        if op == 0:  # COMPRESSION OF A FILE
            p = str(input(f"Enter a file name in the current directory ({os.getcwd()}{os.sep})"))
            while True:
                file_path = f'{os.getcwd()}{os.sep}{p}'
                if os.path.exists(file_path) and p != '':
                    break
                else:
                    p = input("Enter a valid file name in the current directory")
                    if p is not None or p != '':
                        p = str(p)
                    else:
                        continue
            file_stats = os.stat(p)
            original_size = file_stats.st_size
            start = timeit.timeit()
            new_size = compress(p, op)
            end = timeit.timeit()
        elif op == 1:  # COMPRESSION OF A FOLDER
            p = str(input("Enter path to the directory "))
            while True:
                if os.path.exists(p):
                    break
                else:
                    p = str(input("Enter a valid path to the directory "))
            os.chdir(p)
            for f_d in os.listdir(p):
                if f_d.endswith(".txt"):
                    original_size += os.stat(f_d).st_size
            os.chdir(cwd)
            start = timeit.timeit()
            new_size = compress(p, op)
            end = timeit.timeit()
        elif op == 2:  # DECOMPRESSION
            p = str(input("Enter a file name in the current directory "))
            while True:
                file_path = f'{os.getcwd()}{os.sep}{p}'
                if os.path.exists(file_path):
                    break
                else:
                    p = str(input("Enter a valid file name in the current directory "))
            start = timeit.timeit()
            decompress(p)
            end = timeit.timeit()
        else:
            print("Enter a valid operation type")
            continue
        print("Execution time of the program is ", (str('{:.4f}'.format(abs(end - start))) + " seconds"))
        if op != 2:
            print("Compression rate is ", str('{:.2f}'.format((100 - (new_size / original_size) * 100))) + " %")
        x = int(input("Do you want to compress or decompress more files? (0 for NO | 1 for YES) "))
        run = (x == 1)


'''
class Node
{
    constructor(char=null, value=null, left=null, right=null)
    {
        this.value = value
        this.char = char
        this.left = left
        this.right = right
    }

    is_leaf()
    {
        return this.left === null; // && this.right === null;
    }

    get_value()
    {
        return this.value;
    }

    get_char()
    {
        return this.char;    
    }
}

class TestScene extends Phaser.Scene
{
  constructor ()
  {
    super({ key: 'TestScene' });
  }

  preload ()
  {
    //this.load.binary('mio', 'assets/mio.bin', Uint8Array);
    this.load.binary('mio', 'assets/lorem.bin', Uint8Array)
    //this.load.binary('mio', 'assets/large_text.bin', Uint8Array)
  }
  
  create()
  {
    this.file = this.cache.binary.get('mio');
    
    const {byteLength} = this.file;
    
    // testing file is loaded
    for (let i = 0; i < 3; i++)
    {
	  this.printByte(this.file[i], typeof this.file[i]);
    }
    
    // SETUP:
    
    //this.src = 0;
    //this.mask = 0;
    //this.byte = 0;
    
    this.reset();
    
    // initialised:
    this.debugStatus();
     
    
    // real start
    this.reset();
    this.getBits(1);
    
    
	// tree    
    const root = this.decode_tree();
    
    // rebuild frequencies dict
    const dictionary = this.assign_code(root, '')
   
    console.log(dictionary);
     
    
    
    console.log("From here");
    
    // hmmmm b
    console.log("Before");
    this.debugStatus();
    
    const padding = this.getBits(8);
    console.log(`Padding value: ${padding}`);
    
    // hmmmm a
    console.log("After");
    this.debugStatus();
    
    this.getBits(padding);

    
    let code = "";
    const output = []
    while (this.src < byteLength)
    {
      code += this.getBits();
      const currletter = dictionary[code]
      if (currletter)
      {
        output.push(dictionary[code]);
        //console.log(currletter);
        code = "";
      }
    }
    
    console.log(output.join(""));
  }
  
  printByte(num, ...args)
  {
    console.log(`${num} ${num.toString(2).padStart(8, '0')}`, ...args);
  }
  
  reset()
  {
    this.src = 0;
    this.mask = 0;
    this.byte = 0;
  }
  
  debugStatus()
  {
    console.log(`src: ${this.src}, mask: ${this.mask}, byte: ${this.byte}`);
  }
  
  getBits(numbits = 1)
  {
	let i;
    let bits = 0;

	for (i = 0; i < numbits; i++)
	{
		if (this.mask === 0)
        {
			this.byte = this.file[this.src++];
			this.mask = 0x80;
		}
		bits <<= 1;
		bits |= this.byte & this.mask ? 1 : 0;
		this.mask >>= 1;
	}

	return bits;
  }
  
  decode_tree() //# DECODE TREE FROM HEADER
  {
    const char = this.getBits()

    if (char == 1)
    {
      const gag = this.getBits(8);
      // console.log(gag, String.fromCharCode(gag))
        return new Node(String.fromCharCode(gag));
    }
    else
    {
        const left = this.decode_tree();
        const right = this.decode_tree();
        return new Node(null, null, left, right);
    }
  }
  
  assign_code(node, code='')//:  # ASSIGN CODES TO A HUFFMAN TREE
  {
    if (node.is_leaf())
    {
      const temp = {}
      temp[code] = node.get_char();
      return temp;
        //return ({node.get_char(): code})
    }
    const d = {};
    Object.assign(d, this.assign_code(node.left, code + '0'));
    Object.assign(d, this.assign_code(node.right, code + '1'));
    //d.update(assign_code(node.left, code + '0'))
    //d.update(assign_code(node.right, code + '1'))
    return d;
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
