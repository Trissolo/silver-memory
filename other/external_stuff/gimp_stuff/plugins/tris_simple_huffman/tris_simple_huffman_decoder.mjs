console.clear();
// Memo: the string 'abcdefggggabc' has padding === 0

class Node
{
    constructor(char = null, left = null, right = null)
    {
        this.char = char;

        this.left = left;

        this.right = right;
    }

    // is_leaf()
    // {
    //     return this.left === null;
    // }

    // get_char()
    // {
    //     return this.char;
    // }
}

class DecodeHuffman
{
    processedBytes = 0;

    bitstream;

    allNodes = new Set();

    constructor(file)
    {
        this.bitstream = this.bitGenerator(file);

        const fileLength = file.length;

        let padding = this.getAdjacentBits(8);

        // console.log("padding", padding, fileLength)

        // Reconstruct the Huffman tree
        const root = this.decodeTree();




        // Debug: Get the character-code map back
        {
            const dictionary = this.obtainCodesFromTree(root, '');

            console.log(dictionary);
        }

        

        // Decode!
        const output = [];

        // current node
        let node = root;

        const process = () => {

            node = this.getBit().value? node.right : node.left;

            if (node.char)
            {
                output.push(node.char);

                node = root;
            }
        }

        // console.time("p");

        while (this.processedBytes < fileLength)
        {
            process();
        }

        // console.timeEnd('p');

        // if (padding)
        // {
        while (padding--)
        {
            process();
        }
        // }

        // destroy
        this.bitstream.return();

        this.bitstream = undefined;

        // console.log('allNodes', allNodes);
        // {
            // this.allNodes.forEach(n => {
            //     console.log(n.left === null()? `has char: ${n.char}`:'BRANCH');
            //     n.left = n.right = undefined;
            // });
        // }


        // manage the output in any way:

        console.log(output.join(''));

        // console.log(JSON.parse(output.join('')));

        console.log('(End Processing.)');
    }

    *bitGenerator(typedArray)
    {
        for (const byte of typedArray)
        {
            // increment HERE becaused the first byte (that contains the padding) has already been skipped
            this.processedBytes += 1;

            // Iterate bits from Most Significant to Least Significant
            for (let i = 7; i >= 0; i--)
            {
                yield(byte >> i) & 1;
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
        const bit = this.getBit().value;

        if (bit === 1)
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

    // This function is not used in decoding, it exists only for debugging
    obtainCodesFromTree(node, code = '', allNodes = this.allNodes)
    {
        allNodes.add(node);

        if (node.left === null)// node.is_leaf())
        {
            return new Map().set(code, node.char);
        }

        return new Map([...this.obtainCodesFromTree(node.left, code + '0', allNodes), ...this.obtainCodesFromTree(node.right, code + '1', allNodes)]);
    }

} // End DecodeHuffman

class TestScene extends Phaser.Scene {

    constructor()
    {
        super({key: 'TestScene'});
    }

    preload()
    {
        // this.load.binary('mio', 'assets/default.thf', Uint8Array);
        this.load.binary('mio', 'assets/text_fixed_counter.thf', Uint8Array);
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
