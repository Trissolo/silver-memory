export default class rs0
{
    // wrench
    static 0(sprite){console.log(sprite.frame.name)}

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
    static 7(sprite){console.log(sprite.frame.name)}

    // mensole
    static 8(sprite){console.log(sprite.frame.name)}

    // striscia
    static 9(sprite){console.log(sprite.frame.name)}

    // porta
    static 10(sprite)
    {
        console.log(sprite.frame.name)
        const thing_json_data = this.currentThings[sprite.rid];
        console.log("thing_json_data:", thing_json_data.suffix);
        this.toggleBit(thing_json_data.suffix);
        sprite.setFrame(`${thing_json_data.frame}${this.getVarFromArray(thing_json_data.suffix)}`);
    }

    // vasca
    static 11(sprite){console.log(sprite.frame.name)}

    // tubo
    static 12(sprite){console.log(sprite.frame.name)}

}
