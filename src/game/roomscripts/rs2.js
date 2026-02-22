export default class rs2
{
    static onRoomReady()
    {
        // this.cameras.main.setBackgroundColor(0xff0000);
        this.triggerZone.supervise(this.thingsContainer.get(7), this.player, true);
    }
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
    static 4(thing, pointer)
    {
        console.log("AREA4, uscita sud");
        
    }

    // AREA
    static 5(thing)
    {
        console.log("TRigger 5");
        console.log(thing, pointer);
    }

    // muro
    static 6(thing){console.log(thing.frame.name);}

    // AREA
    static 7(ta, actor, boolInside)
    {
        this.cameras.main.setBackgroundColor(0x90fdfd);

        console.log("Crossing the bridge in: AREA 7");

        console.log(typeof boolInside, boolInside);

        this.triggerZone.clearAll();
    }

}
