console.log("CLASS VarMmanager")
const bool_json = require('../gamedata/bool.json');
const crumble_json = require('../gamedata/crumble.json');
const nibble_json = require('../gamedata/nibble.json')
const byte_json = require('../gamedata/byte.json')

//const testdata = require('../gamedata/bool.json');
//console.log(testdata);
class VarManager
{
    // Variable containers
    static varContainers = new Map();

    static BITS_PER_TYPED_ARRAY_ELEMENT = 32;

    static createByKind(kind, arrayLength = 2)
    {
        // we are using an Uint32Array
        const {BITS_PER_TYPED_ARRAY_ELEMENT} = this;
        
        // the size (in bits) of this kind of variable:
        // BOOL = 1 bit [0-1],
        // CRUMBLE = 2 bits [0-3],
        // NIBBLE = 4 bits [0-15],
        // BYTE = 8 bits [0-255]

        const varSize = 1 << kind;

        // amount of variables in each Typed Array element
        const varsPerElement = BITS_PER_TYPED_ARRAY_ELEMENT / varSize;

        // bitmask to extract/work on the variable
        const bitmask = (1 << varSize) - 1;

        let lastIdxAllowed; // = arrayLength;

        if (Array.isArray(arrayLength))
        {
            lastIdxAllowed = arrayLength[kind].length;

            arrayLength = Math.ceil(arrayLength[kind].length * varSize / BITS_PER_TYPED_ARRAY_ELEMENT);

        }
        else
        {
            lastIdxAllowed = arrayLength * varsPerElement;
        }

        const typedArray = new Uint32Array(arrayLength);

        lastIdxAllowed -= 1;

        return {varSize, varsPerElement, bitmask, typedArray, isBool: kind === 0, lastIdxAllowed}; // , maximumCapacity: varsPerElement * arrayLength*/ };
    }

    // sort of constructor
    static initialize(arrayOfStringArray)
    {      
        console.log("Variable Manager: INITIALIZE VarManager");

        // kind/key(containerIdx)|     varSize     |varsPerElement|bitmask
        // ----------------------|-----------------|--------------|-------
        //  0                    | 1 bit  (BOOL)   |      32      |   1   
        //  1                    | 2 bits (CRUMBLE)|      16      |   3   
        //  2                    | 4 bits (NIBBLE) |       8      |   15  
        //  3                    | 8 bits (BYTE)   |       4      |   255 

        for (let kind = 0; kind < 4; kind++)
        {
            this.varContainers.set(this.varContainers.size, this.createByKind(kind, arrayOfStringArray));
        }
        
    }  // end Initialize

    static newHandleAny(kind, varIdx, newValue, toggleBit)
    {
        // console.log(`INSIDE HANDEL ARRAY, kind: ${kind}, varIDX: ${varIdx}, newValue: ${newValue}, toggleBit: ${toggleBit}`);
        const container = this.varContainers.get(kind);

        // Quick check

        if (container.lastIdxAllowed < varIdx) // || varIdx < 0)
        {
            return console.error(`Variable OUT OF RANGE! [Trying to write at idx ${varIdx}, but lastIdxAllowed is ${container.lastIdxAllowed}.`);
        }

        // calc coords:
        const {varsPerElement, typedArray} = container;
        let x = 0;
        let y = 0;

            if (varIdx < varsPerElement)
            {
                x = varIdx;
            }
            else
            {
                y = Math.floor(varIdx / varsPerElement);
                x = varIdx - (y * varsPerElement);
            }

        // Now we have our x/y coords!

        // MEMO: we canl use the amount of arguments to determine the action to take (maybe for calling mapped functions):
        //
        // this[arguments.lengt]();
        // 2 = read variable,
        // 3 = set variable,
        // 4 = toggle 1 bit (only in case of BOOL).

        // hmmm :/
        // const argLength = arguments.length;

        // set the variable?

        // if (typeof newValue === 'number')
        if (arguments.length === 3)
        {
            // Do we need to check the validity of "newValue", here?
            if (newValue < 0 || newValue > container.bitmask)
            {
                console.warn(`Wrong value (attempting ${newValue}, but valdid values must be between 0 and ${container.bitmask})`);
            }

            // first: clear!
            typedArray[y] &= ~(container.bitmask << x * container.varSize);
            
            if (newValue === 0)
            {
                return 0;
            }
            else
            {
    
                typedArray[y] |= (newValue << x * container.varSize);
    
                return newValue;
            }
        }

        // toggle bit?
        if (toggleBit && container.isBool)  // if (argLength === 4 && container.isBool)
        {
            typedArray[y] ^= (1 << x);
        }

        // read any var
        return container.isBool? (typedArray[y] >>> x) & 1 :  (typedArray[y] >>> x * container.varSize) & container.bitmask;
    }

    // readVar(kind, varIdx)
    // {
    //     return this.vars.newHandleAny(kind, varIdx);
    // }

    // setVar(kind, varIdx, newValue)
    // {
    //     return this.vars.newHandleAny(kind, varIdx, newValue);
    // }

    // toggleBit(varIdx, kind = 0)
    // {
    //   return this.vars.newHandleAny(kind, varIdx, null, true);
    // }

    // not yet used
    static betterGetXY(kind, varIdx)
    {
        const container = this.varContainers.get(kind);

        const {varsPerElement} = container;

        if (container.lastIdxAllowed < varIdx)
        {
            return console.error(`Variable index is OUT OF RANGE! [Trying to write at idx ${varIdx}, but lastIdxAllowed is ${container.lastIdxAllowed}.`);
        }

        let x = 0;
        let y = 0;

        if (varIdx < varsPerElement)
        {
            x = varIdx;
        }
        else
        {
            y = Math.floor(varIdx / varsPerElement);
            x = varIdx - (y * varsPerElement);
        }

        return {x, y, container};
        
    }

    static _debug()
    {
        for (const elem of this.varContainers.values())
        {
            console.log("%c Vars per element: ", "background-color: gray;", elem.varsPerElement)
            for (const value of elem.typedArray)
            {
                console.log(`Dec: ${value}, Hex: ${value.toString(16)}`);
                // console.log(Number.parseInt(value.toString(16), 16));
            }
        }
    }

    
}

VarManager.initialize([bool_json, crumble_json, nibble_json, byte_json]);

export default VarManager;
