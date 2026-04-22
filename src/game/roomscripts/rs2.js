import TriggerZone from "../modules/TriggerZone.mjs";

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
        console.log(`Ponte suffix: ${this.varsGetValue(vcoords)}`, vcoords);
        this.varsToggleBit(ponte.rdata.skipCond);
        console.log(`Ponte suffix: ${this.varsGetValue(vcoords)}`);
        ponte.setVisible(!!this.varsGetValue(ponte.rdata.skipCond[0]));
    }

    // portafake
    static 1(thing){console.log(thing.frame.name);}

    // ponte
    static 2(thing)
    {
        console.log(thing.frame.name);
        this.emulateBgClick();
    }

    // siglight
    static 3(thing)
    {
        this.scrollSpriteFrame(thing, 2);
    }

    // AREA
    static 4(ta, pointer)
    {
        console.log("AREA4, uscita sud");
        this.toAnotherRoom(ta, 0, 227, 44, "S", 0);
    }

    // AREA
    static 5(ta, pointer)
    {
        console.log(arguments.length === 3? "Triggered callback":"Click on zone");
        console.log("TRigger 5");
        this.toAnotherRoom(ta, 4, 221, 124, "W", 0);
        //console.log(thing, pointer);
    }

    // muro
    static 6()
    {
        console.log("Muro", arguments.length);
    }

    // AREA
    /**
     * @this {Viewport}
     * @param {TriggerZone} ta
     * @param {*} actor 
     * @param {*} boolInside 
     */
    static 7(ta, actor, boolInside)
    {
        if (typeof boolInside === 'boolean')
        {
            console.log(ta.getOwnData())
            // spec. value
            const bridgeStatus = this.varsGetValue(this.getExistentThing(2).getOwnData().skipCond[0]);
            if (bridgeStatus === 0)
            {
                const hitArea = ta.hasPolygon? Phaser.Geom.Polygon.GetAABB(ta.getHitArea()): ta.getHitArea();
                actor.walkTo(hitArea.centerX > actor.x? 42:145, actor.y);
            }
        }
        console.log("Boolinside:", typeof boolInside, boolInside)
        console.log(arguments.length === 3? "Triggered callback":"Click on zone");
            
        this.cameras.main.setBackgroundColor(Phaser.Math.Between(255, 0xbababa));

        console.log(`${boolInside? "Crossing": "Leaving" } the bridge in: AREA 7`, arguments.length);

        console.log(ta, actor, boolInside);

        // this.triggerZone.clearAll();
    }

}
