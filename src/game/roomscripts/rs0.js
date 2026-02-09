export default class rs0
{
    // wrench
    static 0(thing){
        console.log(thing.frame.name);
        // const roomJson = this.getJson(this.roomId);
        // const tjson = roomJson.things[thing.state]
        // console.dir(tjson);
        // console.log("SKIPCOND", tjson.skipCond)
        this.setAsCondition(thing.rdata.skipCond);
        // ADD ITEM IN INV HERE;
        thing.setVisible(false);
    }

    // coperchio
    static 1(thing){
        console.log(thing.frame.name);
        const roomJson = this.getJson(0);
        const tjson = roomJson.things[thing.state]
        console.dir(tjson);
        console.log(`Suffix vcoords: ${tjson.suffix}\nSuffix value: ${this.getVarValue(tjson.suffix)}`)
        this.toggleBit(tjson.suffix);
        thing.setFrame(`${tjson.frame}${this.getVarValue(tjson.suffix)}`);
    }

    // crate
    static 2(thing){console.log(thing.frame.name);}

    // coso_dietro
    static 3(thing){console.log(thing.frame.name);}

    // AREA
    static 4(thing){console.log(thing.frame.name);}

    // AREA
    static 5(thing){console.log(thing.frame.name);}

    // crepa
    static 6(thing){console.log(thing.frame.name);}

    // button
    static 7(thing){console.log(thing.frame.name);}

    // mensole
    static 8(thing)
    {
        console.log(`SUFFIX: ${thing.rdata.suffix}`);
    }

    // striscia
    static 9(thing){console.log(thing.frame.name);}

    // porta
    static 10(thing)
    {
        console.log(thing.frame.name);
        //const roomJson = this.getJson(0);
        //const tjson = roomJson.things[thing.state];
        //const {suffix: vcoords_for_suffix} = tjson;
        const {suffix: vcoords_for_suffix} = thing.rdata;
        console.log(vcoords_for_suffix);
        const current_value = this.getVarValue(vcoords_for_suffix);
        if (current_value === 0)
        {
            this.setVariable(vcoords_for_suffix, 1);
        }
        else
        {
            this.setVariable(vcoords_for_suffix, 0);
        }
        console.log("Changed to:", this.getVarValue(vcoords_for_suffix));
        //refresh frame
        thing.setFrame(`${thing.rdata.frame}${this.getVarValue(vcoords_for_suffix)}`);

    }

    // vasca
    static 11(thing){console.log(thing.frame.name);}

    // tubo
    static 12(thing){console.log(thing.frame.name);}
}
