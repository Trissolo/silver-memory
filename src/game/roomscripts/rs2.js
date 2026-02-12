export default class rs2
{
    // button
    static 0(thing)
    {
        //this.cameras.main.startFollow(new Phaser.Math.Vector2(250, 85));
        
        const ponte = this.getExistentThing(2);
        console.log(thing.frame.name, ponte.frame.name);
        const vcoords = ponte.rdata.skipCond[0];
        console.log(`Ponte suffix: ${this.getVarValue(vcoords)}`, vcoords);
        this.toggleBit(ponte.rdata.skipCond);
        console.log(`Ponte suffix: ${this.getVarValue(vcoords)}`);
        ponte.setVisible(!!this.getVarValue(ponte.rdata.skipCond[0]));
    }

    // portafake
    static 1(thing){console.log(thing.frame.name);}

    // ponte
    static 2(thing){console.log(thing.frame.name);}

    // siglight
    static 3(thing)
    {
        this.scrollSpriteFrame(thing, 2);
    }

    // AREA
    static 4(thing){console.log(thing.frame.name);}

    // AREA
    static 5(thing){console.log(thing.frame.name);}

    // muro
    static 6(thing){console.log(thing.frame.name);}

    // AREA
    static 7(thing){console.log(thing.frame.name);}

}
