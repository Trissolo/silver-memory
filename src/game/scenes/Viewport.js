import VarManager from '../modules/VarManager.js';
import RoomScripts from '../roomscripts/roomscripts.js';
import { NONE, Scene } from 'phaser';

export class Viewport extends Scene
{
    roomId;
    roomJson;
    thingsJson;
    thingsContainer;
    roomscript;
    bg;
    shield;

    constructor ()
    {
        super(
        {
            key: 'Viewport',
            active: false,
            visible: false,
            plugins: [
                'Clock',  //this.time
                //'DataManagerPlugin',  //this.data
                'InputPlugin',  //this.input
                'Loader',  //this.load
                'TweenManager',  //this.tweens
                //'LightsPlugin'  //this.lights
                ],
            cameras:
            {
                backgroundColor: "#008777" //,
                //y: 11, // 136,
                //height: 64
            }
        });
    } //end constructor

    init(data)
    {
        console.dir("INIT", this);
        console.log("Vars", VarManager)
        this.debuCounter = 0;
    }

    create ()
    {
        // random preliminary stuff:
        this.cameras.main.setBackgroundColor(0x00ff00);
        this.input.setDefaultCursor('url("/assets/cursors/cross3.cur"), pointer');

        // 1) background image
        this.bg = this.add.image(0, 0, 'atlas0')
        .setDepth(-5)
        .setOrigin(0)

        // 2) Room 'things'
        this.thingsGroup = this.add.group({createCallback: function (thing)
            {
                thing.setInteractive({cursor: 'url("/assets/cursors/cover3.cur"), pointer', pixelPerfect: true})
                thing.setVisible(false);
            }
        })

        // 2b) container for 'things'
        this.thingsContainer = new Map();


        // player
        //this.player = null;

        // shield
        //this.shield = null


        // START
        this.drawRoom(0);



        // code for test
        this.input.keyboard.on('keydown-Z', this.pressedZ, this);

        this.input.keyboard.on('keydown-X', this.pressedX, this);
    }

    pressedZ(eve)
    {
        this.clear_room();
        this.debuCounter += 1;
        this.drawRoom(this.debuCounter & 1);
    }

    pressedX(eve)
    {
        console.log("roomId is:", this.roomId);
    }

    disable_group_things()
    {      
        for (const thing of this.thingsContainer.values())
        {
            thing.disableInteractive()
              .setActive(false)
              .setVisible(false)
              .rid = null
        }

        this.thingsContainer.clear();
    
    } //end disable_group_things

    clear_room()
    {
        this.roomJson = null;
        this.roomscript = null;
        this.thingsJson  = null;
        this.roomId = null;

        this.bg.setVisible(false);
        this.disable_group_things();
    }

    set_fonsEtOrigo(roomId)
    {
        this.roomJson = this.getJson(roomId);
        this.roomscript = RoomScripts[roomId];

        // maybe too redundant
        this.thingsJson  = this.roomJson.things;
        this.roomId = roomId;
    }

    render_things()
    {
        const atlasKey = `atlas${Math.floor(this.roomId / 3)}`;

        for (const [idx, thingData] of this.roomJson.things.entries())
        {
            if (thingData.kind === 1)
            {
                continue;
            }
                                
            const tsprite = this.thingsGroup.get(thingData.x, thingData.y);
            
            console.log("🫓 Super imp", "Active", tsprite.active, "Visible", tsprite.visible);
            
            // set the frame, or, if needed, the texture
            const assembledFrameName = `${thingData.frame}${thingData.suffix? this.getVarFromArray(thingData.suffix): ""}`;
            //console.log(`AtlasKey: ${atlasKey}\nCurrent sprite texture: ${tsprite.texture.key}`)
            tsprite.texture.key === atlasKey? tsprite.setFrame(assembledFrameName): tsprite.setTexture(atlasKey, assembledFrameName);
            
            // Room ID!
            tsprite.rid = idx;
            
            // let's keep this thing in its container
            this.thingsContainer.set(idx, tsprite);
            
            tsprite.setDepth(thingData.kind);//.setActive(true).setVisible(true);
            tsprite.setActive(true);
            //tsprite.setVisible(true)
            
            // if it's a new member, let's associate the listener for user interaction
            if (!tsprite.listenerCount(Phaser.Input.Events.POINTER_DOWN))
            {
                tsprite.on(Phaser.Input.Events.POINTER_DOWN, this.onThingDown);
            }
            else
            {
                console.log("Thing already has input listeners");
            }
            
            // console.log("eventNames()", tsprite.eventNames(), "pointerdown amount:", tsprite.listenerCount('pointerdown'));

            // deepthsorted?
            if (thingData.kind === 4)
            {
                tsprite.setOrigin(0.5, 1);
            }
            else
            {
                tsprite.setOrigin(0);
            }
            
            if (thingData.noInteraction)
            {
                console.log("...but is input disabled");
                tsprite.disableInteractive(false);
                continue;
            }
            else
            {
                //tsprite.on('pointerdown', this.onThingDown)//RoomScripts[thingData_roomId][idx], this);
                tsprite.setInteractive();
            }
            
            if (thingData.skipCond && this.conditionIsSatisfied(thingData.skipCond))
            {
                console.log("Skipping",thingData);
                continue;
            }
            else
            {
                tsprite.setVisible(true);
            }
        }
    }

    drawRoom(id)
    {
        console.log("NEW draw room");
        this.set_fonsEtOrigo(id);
        this.render_things();

        // hardcoded for now
        this.bg.setTexture(`atlas${Math.floor(this.roomId / 3)}`, this.roomJson.bg);
        this.bg.setVisible(true);
    }

    onThingDown(a,b)
    {
        const scene = this.scene;
        console.log(`Clicked thing`,this.frame.name);// Math.random());
        scene.roomscript[this.rid].call(scene, this);

    }

    getVarFromArray(ary)
    {
        return VarManager.newHandleAny(ary[0], ary[1]);
    }

    conditionIsSatisfied(ary)
    {
        return VarManager.newHandleAny(ary[0], ary[1]) === ary[2];
    }

    setVariable(ary, newValue)
    {
        VarManager.newHandleAny(ary[0], ary[1], newValue);
    }

    toggleBit(ary)
    {
        return VarManager.newHandleAny(ary[0], ary[1], null, true);
    }
    // unused
    getRoomJson(roomId)
    {
        return roomId === undefined? this.roomJson : this.cache.json.get(`room${roomId}`)
    }
     //unused
    getThingsJson(roomId)
    {
        return roomId === undefined? this.thingsJson : this.getRoomJson(roomId).things;
    }

    getJson(roomId)
    {
        console.log(`Getting JSON for room: ${roomId}`);
        return this.cache.json.get(`room${roomId}`);
    }

    getExistentThing(rid)
    {
        if (!this.thingsContainer.has(rid))
        {
            console.warn(`Current room (${this.roomId}) does not contains any Thing with rid ${rid}`);
            return false
        }
        return this.thingsContainer.get(rid);
    }

    setThingNotVisible(thing)
    {
        //rid = typeof thing === "number"? rid : thing.rid;
        gameObject = null
        const varAry = this.thingsJson[rid]
    }

    nextIntInRange(val, minValue = 0, maxAllowed = 9, decrease = false)
    {
        if (val < minValue || val > maxAllowed)
        {
            console.warn(`nextIntInRange: val (${val}) is out of range ${minValue}-${maxAllowed}`);
            return false;
        }
        if (decrease)
        {
            return val === 0? maxAllowed:val-1;
        }
        else
        {
            return val === maxAllowed?0: val+1;
        }
    }
}
