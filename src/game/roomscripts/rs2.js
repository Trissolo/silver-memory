const rs2 = {

    onRoomReady()
    {
        this.triggerZones.supervise(this.thingsContainer.get(7), this.player, true);
    },
    
    // button0
    0(thing, pointer)
    {
        console.log(thing, pointer);
        const ponte = this.getExistentThing(2);
        const vcoords = ponte.rdata.skipCond[0];
        const tempSataus = this.varsToggleBit(vcoords);
        console.log(`Ponte tempSataus: ${tempSataus}`);
        ponte.setVisible(!!tempSataus);
        console.log(thing.rdata, thing.frame.name, tempSataus);
        thing.setFrame(`${thing.rdata.frame}${tempSataus}`);
    },
    
    // portafake
    1(thing, pointer)
    {
        console.log(thing, pointer);
    },
    
    // ponte
    2(thing, pointer)
    {
        this.emulateBgClick(pointer);
    },
    
    // siglight0
    3(thing, pointer)
    {
        console.log(thing, pointer);
    },
    
    // r2exitbottom
    4(ta, pointer)
    {
        this.toAnotherRoom(ta, 0, 227, 44, "S", 0);
    },
    
    // ENTER ON r2exitbottom
    in4(ta, actor, boolInside)
    {
        console.log(ta, actor, boolInside);
    },
    
    // r2exitleft
    5(ta, pointer)
    {
        this.toAnotherRoom(ta, 4, 221, 124, "W", 0);
    },
    
    // ENTER ON r2exitleft
    in5(ta, actor, boolInside)
    {
        console.log(ta, actor, boolInside);
    },
    
    // muro
    6(thing, pointer)
    {
        this.emulateBgClick(pointer);
    },
    
    // arear2bridge
    7(ta, pointer)
    {
        console.log(ta, actor, boolInside);
    },
    
    // ENTER ON arear2bridge
    in7(ta, actor, boolInside)
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
    }
}

export default rs2;
