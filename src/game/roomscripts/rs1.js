import { Viewport } from "../scenes/Viewport";

export default class rs1
{
    // porta0
    static 0(thing)
    {
        console.log(thing.frame.name, "GAG!");

        // this.prepareRoomEvent(
        //     [
        //         {
        //             at: 0,
        //             target: this,
        //             run: this.userInteractionOff
        //         },
        //         {
        //             at: 500,
        //             run: () => {
        //                 this.varsToggleBit(thing.rdata.suffix);
        //                 this.refreshSpriteFrame(thing);
        //             }
        //         },
        //         {
        //             at: 800,
        //             run: () => {
        //                 this.varsToggleBit(thing.rdata.suffix);
        //                 this.refreshSpriteFrame(thing);
        //             }
        //         },
        //         {
        //             at: 1200,
        //             run: () => {
        //                 this.varsToggleBit(thing.rdata.suffix);
        //                 this.refreshSpriteFrame(thing);
        //             }
        //         },
        //         {
        //             at: 1500,
        //             run: console.log("RAZZUS", this)
        //         }
        //     ], true, true, this.roomscript.uffa, this);
    }
    
    // passaggio
    static 1(thing)
    {
        console.log("Passaggio", this.player.getPolygonalMapIdx());
        if (this.player.getPolygonalMapIdx() === 1)
        {
            this.emulateBgClick();
        }
    }
    
    // exitEst
    static 2(ta, actor, boolInside)
    {
        console.log(ta);
        // this.toAnotherRoom(ta, 1, 33, 82, "NE", 1);
        this.toAnotherRoom(ta, 0, 23, this.input.activePointer.worldY, "E", 0);
    }
    
    // ITcardA
    static 3(thing)
    {
        console.log(thing);
    }
    
    // r1cabinetDoors1
    static 4(thing)
    {
        const {suffix} = thing.rdata;
        this.varsToggleBit(suffix);
        this.refreshSpriteFrame(thing);
    }
    
    // cabinet
    static 5(thing)
    {
        console.log(thing);
    }
    
    // r1_walk_behind
    static 6(thing)
    {
        console.log(thing);
    }
    
    // westCover
    static 7(thing)
    {
        console.log(thing);
    }
    
    // r1_exitWest
    static 8(ta, actor, boolInside)
    {
        console.log(ta);
        this.emulateBgClick();
    }
    
    // otherRoomFloor
    static 10(thing)
    {
        console.log(thing);
    }
    
    static uffa()
    {
        console.log("🩺 E questo era pending");
        this.cameras.main.setBackgroundColor(0);
    }
}

/*
export default class rs1
{
    // porta
    static 0(thing)
    {
        console.log(thing.frame.name, "GAG!");

        this.prepareRoomEvent(
            [
                {
                    at: 0,
                    target: this,
                    run: this.userInteractionOff
                },
                {
                    at: 500,
                    run: () => {
                        this.varsToggleBit(thing.rdata.suffix);
                        this.refreshSpriteFrame(thing);
                    }
                },
                {
                    at: 800,
                    run: () => {
                        this.varsToggleBit(thing.rdata.suffix);
                        this.refreshSpriteFrame(thing);
                    }
                },
                {
                    at: 1200,
                    run: () => {
                        this.varsToggleBit(thing.rdata.suffix);
                        this.refreshSpriteFrame(thing);
                    }
                },
                {
                    at: 1500,
                    run: console.log("RAZZUS", this)
                }
            ], true, true, this.roomscript.uffa, this);
        

        //this.roomEmitter.once('complete', this.roomscript.uffa, this);

    }

    // passaggio
    static 1(thing)
    {
        console.log(thing.frame.name);     
    }

    // AREA
    static 2(thing){console.log(thing.frame.name);}

    // AREA
    static 3(thing){console.log(thing.frame.name);}

    // ITcardA
    static 4(thing){console.log(thing.frame.name);}

    // r1cabinetDoors
    static 5(thing)
    {
        const {suffix} = thing.rdata;
        this.varsToggleBit(suffix);
        this.refreshSpriteFrame(thing);

    }

    // cabinet
    static 6(thing){console.log(thing.frame.name);}

    static uffa()
    {
        console.log("🩺 E questo era pending");
        this.cameras.main.setBackgroundColor(0);
    }

}

*/
