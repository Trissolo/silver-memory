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
                        this.toggleBit(thing.rdata.suffix);
                        this.refreshSpriteFrame(thing);
                    }
                },
                {
                    at: 800,
                    run: () => {
                        this.toggleBit(thing.rdata.suffix);
                        this.refreshSpriteFrame(thing);
                    }
                },
                {
                    at: 1200,
                    run: () => {
                        this.toggleBit(thing.rdata.suffix);
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
        this.toggleBit(suffix);
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
