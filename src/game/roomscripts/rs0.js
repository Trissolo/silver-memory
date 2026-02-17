import { Viewport } from "../scenes/Viewport";
export default class rs0
{
    // wrench
    static 0(thing)
    {
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
    static 3(thing)
    {
        // console.log(thing.frame.name);
        // console.log(`Thing.y ${thing.y} - Robot: ${this.player.y}`)
        // thing.setDepth(thing.y);
        // this.player.setDepth(this.player.y);

        const {scene} = thing;
        const {worldX, worldY} = scene.input.activePointer;
        console.log(`Before Thing y: ${thing.y}, Actor.y: ${thing.scene.player.y}`);
        console.log(worldX, worldY)
        scene.player.setPosition(worldX, worldY);
        console.log(`After Thing y: ${thing.y}, Actor.y: ${thing.scene.player.y}`);
    }

    // AREA
    static 4(thing){console.log(thing.frame.name);}

    // AREA
    static 5(thing){console.log(thing.frame.name);}

    // crepa
    static 6(thing){console.log(thing.frame.name);}

    // button
    static 7(thing)
    {
        console.log("This ROOMSCRIPT", "RoomId:", this.roomId);

        this.player.assignMission(this.getScript(this.roomId).pressButton);
        this.player.walkTo(161, 68);
    }

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

    static pressButton()
    {
        const {player} = this;
        const buttonSprite = this.getExistentThing(7);

        this.prepareRoomEvent([
            {
                    at: 0,
                    target: this,
                    run: this.userInteractionOff
                },
                {
                    at: 400,
                    // target: player,
                    run: () => player.turnAndStayStill("NE")
                },
                {
                    at: 800,
                    run: () => {console.log("SETTING INTERACT FRAME");player.setFrame(`${player.costume}_interactCenter_NE_0`)}
                },
                {
                    at: 900,
                    run: () => {
                        this.toggleBit(buttonSprite.rdata.suffix);
                        this.refreshSpriteFrame(buttonSprite);
                    }
                    
                },
                {
                    at: 1500,
                    run: () => {console.log("SETTING IDLE FRAME"); player.setFrame(`${player.costume}_walk_NE_0`)}
                }
        ], /*raiseshield =*/ true, /*immediatePlay =*/ true);  //, onceComplete, scope)
    
    }
}
