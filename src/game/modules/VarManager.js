console.log("CLASS VarManager");
const bool_json = require('../gamedata/bool.json');
const crumble_json = require('../gamedata/crumble.json');
const nibble_json = require('../gamedata/nibble.json')
const byte_json = require('../gamedata/byte.json')

class VarManager
{
    // Contenitori per le variabili
    static varContainers = [];
    static BITS_PER_ELEMENT = 32;

    /**
     * Crea un contenitore ottimizzato per un tipo di variabile (Kind).
     */
    static createByKind(kind, arrayLength = 2)
    {
        const varSize = 1 << kind; // 1, 2, 4, 8 bits
        const varsPerElement = this.BITS_PER_ELEMENT / varSize;
        
        // Calcolo shift e mask per evitare Math.floor e %
        // Se varsPerElement è 32, shift è 5 (2^5). Se è 8, shift è 3 (2^3).
        const vpeShift = Math.log2(varsPerElement);
        const vpeMask = varsPerElement - 1;
        const bitmask = (1 << varSize) - 1;

        let lastIdxAllowed;
        let actualArraySize = arrayLength;

        // Gestione input array (da JSON) o numero diretto
        if (Array.isArray(arrayLength)) {
            lastIdxAllowed = arrayLength[kind].length;
            actualArraySize = Math.ceil((lastIdxAllowed * varSize) / this.BITS_PER_ELEMENT);
        }
        else
        {
            lastIdxAllowed = arrayLength * varsPerElement;
        }

        return {
            varSize,
            vpeShift,
            vpeMask,
            bitmask,
            typedArray: new Uint32Array(actualArraySize),
            lastIdxAllowed: lastIdxAllowed - 1,
            kind // memorizziamo il kind per comodità
        };
    }

    /**
     * Inizializza i 4 contenitori (Bool, Crumble, Nibble, Byte)
     */
    static initialize(dataArrays)
    {
        console.log("Variable Manager: INITIALIZING...");
        for (let kind = 0; kind < 4; kind++)
        {
            this.varContainers[kind] = this.createByKind(kind, dataArrays);
        }
    }

    /**
     * Funzione Core: Gestisce lettura, scrittura e toggle con logica bitwise pura.
     */
    static handle(kind, varIdx, newValue, toggle)
    {
        const container = this.varContainers[kind];

        if (varIdx > container.lastIdxAllowed)
        {
            console.error(`Variable OUT OF RANGE! Kind: ${kind}, Idx: ${varIdx}`);
            return 0;
        }

        // Calcolo coordinate bitwise (Niente Math.floor, niente %)
        const y = varIdx >>> container.vpeShift;     // Indice nell'Uint32Array
        const x = varIdx & container.vpeMask;        // Posizione "slot" nell'elemento
        const bitOffset = x << kind;                 // Offset reale del bit (x * varSize)

        const { typedArray, bitmask } = container;

        // AZIONE: Scrittura (3 argomenti)
        if (newValue !== undefined && toggle === undefined)
        {
            if (newValue < 0 || newValue > bitmask)
            {
                console.warn(`Value ${newValue} out of range for bitmask ${bitmask}`);
            }
            // Clear e Set
            typedArray[y] &= ~(bitmask << bitOffset);
            typedArray[y] |= (newValue & bitmask) << bitOffset;
            return newValue;
        }

        // AZIONE: Toggle (4 argomenti, solo per BOOL)
        if (toggle && kind === 0)
        {
            typedArray[y] ^= (1 << bitOffset);
        }

        // AZIONE: Lettura (Sempre eseguita se non è una scrittura pura)
        return (typedArray[y] >>> bitOffset) & bitmask;
    }

    /**
     * Recupera il valore usando le coordinate "fuse" (vcoords)
     */
    static getValue(vcoords)
    {
        return this.handle(vcoords & 3, vcoords >>> 2);
    }

    /**
     * Imposta il valore usando le coordinate "fuse" (vcoords)
     */
    static setValue(vcoords, newValue)
    {
        return this.handle(vcoords & 3, vcoords >>> 2, newValue);
    }

    /**
     * Verifica se una condizione [vcoords, expectedValue] è soddisfatta
     */
    static match(conditionArray)
    {
        // const {vcoords, expectedValue} = conditionArray;
        return this.getValue(conditionArray[0]) === conditionArray[1];
    }

    /**
     * Toggle a BOOL bit
     */
    static toggleBit(vcoords)
    {
        return this.handle(vcoords & 3, vcoords >>> 2, undefined, true);
    }

    /**
     * Restituisce una copia dei 4 array per il salvataggio su file/localStorage
     */
    static getState()
    {
        return this.varContainers.map(c => Array.from(c.typedArray));
    }

    static _summary()
    {
        const kindMap = ['Bools', 'Crumble', 'Nibble', 'Bytes'];
        for (const [cidx, container] of this.varContainers.entries())
        {
            const currRes = [kindMap[cidx]];
            for (const elem of container.typedArray)
            {
                currRes.push(elem.toString(2).padStart(this.BITS_PER_ELEMENT, '0'));
            }
            console.log(currRes.join(' | '));
        }

        // console.log(this.varContainers[0].typedArray[0].toString(2).padStart(this.BITS_PER_ELEMENT, '0'));
    }
}

VarManager.initialize([bool_json, crumble_json, nibble_json, byte_json]);

// export default VarManager;

const varsMixin = {

    varsGetValue(vcoords)
    {
        return VarManager.getValue(vcoords);
    },

    varsSetValue(vcoords, newValue)
    {
        return VarManager.setValue(vcoords, newValue);
    },

    varsToggleBit(vcoords)
    {
        return VarManager.toggleBit(vcoords);
    },

    varsMatch(conditionArray)
    {
        return VarManager.match(conditionArray);
    },

    varsSummary()
    {
        console.clear();
        return VarManager._summary();
    }
}

export default varsMixin;

//


// class VarManager
// {
//     // Variable containers
//     static varContainers = new Map();

//     static BITS_PER_TYPED_ARRAY_ELEMENT = 32;

//     static createByKind(kind, arrayLength = 2)
//     {
//         // we are using an Uint32Array
//         const {BITS_PER_TYPED_ARRAY_ELEMENT} = this;
        
//         // the size (in bits) of this kind of variable:
//         // BOOL = 1 bit [0-1],
//         // CRUMBLE = 2 bits [0-3],
//         // NIBBLE = 4 bits [0-15],
//         // BYTE = 8 bits [0-255]

//         const varSize = 1 << kind;

//         // amount of variables in each Typed Array element
//         const varsPerElement = BITS_PER_TYPED_ARRAY_ELEMENT / varSize;

//         // bitmask to extract/work on the variable
//         const bitmask = (1 << varSize) - 1;

//         let lastIdxAllowed; // = arrayLength;

//         if (Array.isArray(arrayLength))
//         {
//             lastIdxAllowed = arrayLength[kind].length;

//             arrayLength = Math.ceil(arrayLength[kind].length * varSize / BITS_PER_TYPED_ARRAY_ELEMENT);

//         }
//         else
//         {
//             lastIdxAllowed = arrayLength * varsPerElement;
//         }

//         const typedArray = new Uint32Array(arrayLength);

//         lastIdxAllowed -= 1;

//         return {varSize, varsPerElement, bitmask, typedArray, isBool: kind === 0, lastIdxAllowed}; // , maximumCapacity: varsPerElement * arrayLength*/ };
//     }

//     // sort of constructor
//     static initialize(arrayOfStringArray)
//     {      
//         console.log("Variable Manager: INITIALIZE VarManager");

//         // kind/key(containerIdx)|     varSize     |varsPerElement|bitmask
//         // ----------------------|-----------------|--------------|-------
//         //  0                    | 1 bit  (BOOL)   |      32      |   1   
//         //  1                    | 2 bits (CRUMBLE)|      16      |   3   
//         //  2                    | 4 bits (NIBBLE) |       8      |   15  
//         //  3                    | 8 bits (BYTE)   |       4      |   255 

//         for (let kind = 0; kind < 4; kind++)
//         {
//             this.varContainers.set(this.varContainers.size, this.createByKind(kind, arrayOfStringArray));
//         }
        
//     }  // end Initialize

//     static newHandleAny(kind, varIdx, newValue, varsToggleBit)
//     {
//         // console.log(`INSIDE HANDEL ARRAY, kind: ${kind}, varIDX: ${varIdx}, newValue: ${newValue}, varsToggleBit: ${varsToggleBit}`);
//         const container = this.varContainers.get(kind);

//         // Quick check

//         if (container.lastIdxAllowed < varIdx) // || varIdx < 0)
//         {
//             return console.error(`Variable OUT OF RANGE! [Trying to write at idx ${varIdx}, but lastIdxAllowed is ${container.lastIdxAllowed}.`);
//         }

//         // calc coords:
//         const {varsPerElement, typedArray} = container;
//         let x = 0;
//         let y = 0;

//             if (varIdx < varsPerElement)
//             {
//                 x = varIdx;
//             }
//             else
//             {
//                 y = Math.floor(varIdx / varsPerElement);
//                 x = varIdx - (y * varsPerElement);
//             }

//         // Now we have our x/y coords!

//         // MEMO: we canl use the amount of arguments to determine the action to take (maybe for calling mapped functions):
//         //
//         // this[arguments.lengt]();
//         // 2 = read variable,
//         // 3 = set variable,
//         // 4 = toggle 1 bit (only in case of BOOL).

//         // hmmm :/
//         // const argLength = arguments.length;

//         // set the variable?

//         // if (typeof newValue === 'number')
//         if (arguments.length === 3)
//         {
//             // Do we need to check the validity of "newValue", here?
//             if (newValue < 0 || newValue > container.bitmask)
//             {
//                 console.warn(`Wrong value (attempting ${newValue}, but valdid values must be between 0 and ${container.bitmask})`);
//             }

//             // first: clear!
//             typedArray[y] &= ~(container.bitmask << x * container.varSize);
            
//             if (newValue === 0)
//             {
//                 return 0;
//             }
//             else
//             {
    
//                 typedArray[y] |= (newValue << x * container.varSize);
    
//                 return newValue;
//             }
//         }

//         // toggle bit?
//         if (varsToggleBit && container.isBool)  // if (argLength === 4 && container.isBool)
//         {
//             typedArray[y] ^= (1 << x);
//         }

//         // read any var
//         return container.isBool? (typedArray[y] >>> x) & 1 :  (typedArray[y] >>> x * container.varSize) & container.bitmask;
//     }

//     // readVar(kind, varIdx)
//     // {
//     //     return this.vars.newHandleAny(kind, varIdx);
//     // }

//     // setVar(kind, varIdx, newValue)
//     // {
//     //     return this.vars.newHandleAny(kind, varIdx, newValue);
//     // }

//     // varsToggleBit(varIdx, kind = 0)
//     // {
//     //   return this.vars.newHandleAny(kind, varIdx, null, true);
//     // }

//     // not yet used
//     static betterGetXY(kind, varIdx)
//     {
//         const container = this.varContainers.get(kind);

//         const {varsPerElement} = container;

//         if (container.lastIdxAllowed < varIdx)
//         {
//             return console.error(`Variable index is OUT OF RANGE! [Trying to write at idx ${varIdx}, but lastIdxAllowed is ${container.lastIdxAllowed}.`);
//         }

//         let x = 0;
//         let y = 0;

//         if (varIdx < varsPerElement)
//         {
//             x = varIdx;
//         }
//         else
//         {
//             y = Math.floor(varIdx / varsPerElement);
//             x = varIdx - (y * varsPerElement);
//         }

//         return {x, y, container};
        
//     }

//     static _debug()
//     {
//         for (const elem of this.varContainers.values())
//         {
//             console.log("%c Vars per element: ", "background-color: gray;", elem.varsPerElement)
//             for (const value of elem.typedArray)
//             {
//                 console.log(`Dec: ${value}, Hex: ${value.toString(16)}`);
//                 // console.log(Number.parseInt(value.toString(16), 16));
//             }
//         }
//     }

    
// }

// VarManager.initialize([bool_json, crumble_json, nibble_json, byte_json]);

// export default VarManager;




// ///////////Ottimizzato

