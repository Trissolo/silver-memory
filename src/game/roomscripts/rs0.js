export default class rs0
{
    // wrench
    static 0(sprite)
    {
        const aryvar = this.thingsJson[sprite.rid]?.skipCond;
        this.setVariable(aryvar, 1);
        sprite.setVisible(false);
    }

    // coperchio
    static 1(sprite){console.log(sprite.frame.name)}

    // crate
    static 2(sprite){console.log(sprite.frame.name)}

    // coso_dietro
    static 3(sprite){console.log(sprite.frame.name)}

    // AREA
    static 4(sprite){console.log(sprite.frame.name)}

    // AREA
    static 5(sprite){console.log(sprite.frame.name)}

    // crepa
    static 6(sprite){console.log(sprite.frame.name)}

    // button
    static 7(sprite)
    {
        //console.log(sprite.frame.name);
        // this.visible_things.get(3).setVisible(false);
    }

    // mensole
    static 8(sprite){console.log(sprite.frame.name)}

    // striscia
    static 9(sprite){console.log(sprite.frame.name)}

    // porta
    static 10(sprite)
    {
        console.log(sprite.frame.name)
        const thing_json_data = this.roomJson.things[sprite.rid];
        console.log("thing_json_data:", thing_json_data.suffix);
        this.toggleBit(thing_json_data.suffix);
        sprite.setFrame(`${thing_json_data.frame}${this.getVarFromArray(thing_json_data.suffix)}`);
    }

    // vasca
    static 11(sprite)
    {
        //const wrenchSkipVar = [...this.thingsJson[0].skipCond];
        //wrenchSkipVar.pop();
        //const variable = 
        const {skipCond} = this.thingsJson[0]
        console.log(sprite.frame.name, `WrenchStatus: ${skipCond} (${this.getVarFromArray(skipCond)})`)
    }

    // tubo
    static 12(sprite){console.log(sprite.frame.name)}

}
