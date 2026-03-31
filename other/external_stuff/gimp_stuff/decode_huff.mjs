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
    bitstream;
  
    constructor(file)
    {
        this.bitstream = this.bitGenerator(file);

        // skips the control bit set by the compression algorithm
        this.getBit();

        // Reconstruct the Huffman tree
        const root = this.decodeTree();

        // Get the character-code map back
        const dictionary = this.assign_code(root, '');

        console.log(dictionary);

        const padding = this.getAdjacentBits(8);

        this.getAdjacentBits(padding);

        const output = [];

        let code = "";

        let position = {done: false};

        while (!position.done)
        {
            position = this.getBit();

            code += position.value;
            
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
        const char = this.getBit().value

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
        this.load.binary('mio', 'assets/mio.bin', Uint8Array);
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
