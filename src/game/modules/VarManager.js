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
     * Core Function: Handles reading, writing and toggle with pure bitwise logic.
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

        // ACTION: Writing (3 arguments)
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

        // ACTION: Toggle (4 arguments, only for BOOLs)
        if (toggle && kind === 0)
        {
            typedArray[y] ^= (1 << bitOffset);
        }

        // ACTION: Reading (Always done if it is not a pure writing)
        return (typedArray[y] >>> bitOffset) & bitmask;
    }

    // static _summary()
    // {
    //     const kindMap = ['Bools', 'Crumble', 'Nibble', 'Bytes'];
    //     for (const [cidx, container] of this.varContainers.entries())
    //     {
    //         const currRes = [kindMap[cidx]];
    //         for (const elem of container.typedArray)
    //         {
    //             currRes.push(elem.toString(2).padStart(this.BITS_PER_ELEMENT, '0'));
    //         }
    //         console.log(currRes.join(' | '));
    //     }    
    // }

    static _summary()
    {
        const names = ["BOOL", "CRUMBLE", "NIBBLE", "BYTE"];
        console.log("--- VAR MANAGER DEBUG SUMMARY ---");
        this.varContainers.forEach(c => {
            console.log(`%c Kind ${c.kind} (${names[c.kind]}):`, "background-color: gray;");
            c.typedArray.forEach((val, i) => {
                // Converte in binario, aggiunge gli zeri iniziali fino a 32 e separa ogni 8 bit per leggibilità
                const binary = val.toString(2).padStart(32, '0').match(/.{1,8}/g).join(' ');
                console.log(`  [${i}] ${binary}`);
            });
        });
    }
}

VarManager.initialize([bool_json, crumble_json, nibble_json, byte_json]);


const varsMixin = {

    varsGetValue(vcoords)
    {
        return VarManager.handle(vcoords & 3, vcoords >>> 2);
    },

    varsSetValue(vcoords, newValue)
    {
        return VarManager.handle(vcoords & 3, vcoords >>> 2, newValue);
    },

    varsToggleBit(vcoords)
    {
        return VarManager.handle(vcoords & 3, vcoords >>> 2, undefined, true);
    },

    varsMatch(conditionArray)
    {
        return this.varsGetValue(conditionArray[0]) === conditionArray[1];
    },

    varsSummary()
    {
        console.clear();
        return VarManager._summary();
    }
    
}

for (const key of Object.keys(varsMixin))
{
    console.log(`%c varsMixin: ${key}; `, "background-color: gray;");
}

export default varsMixin;
