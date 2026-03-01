export default class rs2
{
    static onRoomReady()
    {
        // this.cameras.main.setBackgroundColor(0xff0000);
        this.triggerZones.supervise(this.thingsContainer.get(7), this.player, true);
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
    static 5(thing, pointer)
    {
        console.log(arguments.length === 3? "Triggered callback":"Click on zone");
        console.log("TRigger 5");
        //console.log(thing, pointer);
    }

    // muro
    static 6()
    {
        console.log("Muro", arguments.length);
    }

    // AREA
    static 7(ta, actor, boolInside)
    {
        console.log(arguments.length === 3? "Triggered callback":"Click on zone");
            
        this.cameras.main.setBackgroundColor(Phaser.Math.Between(255, 0xbababa));

        console.log(`${boolInside? "Crossing": "Leaving" } the bridge in: AREA 7`, arguments.length);

        console.log(ta, actor, boolInside);

        // this.triggerZone.clearAll();
    }

}
