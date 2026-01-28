import VarManager from '../modules/VarManager.js';
import RoomScripts from '../roomscripts/roomscripts.js';
import { NONE, Scene } from 'phaser';

export class Viewport extends Scene
{
    room_id;
    roomJson;
    thingJson;
    things_container;
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
        this.things_container = new Map();


        // player
        //this.player = null;

        // shield
        //this.shield = null


        // START
        this.drawRoom(1);



        // code for test
        this.input.keyboard.on('keydown-Z', this.pressedZ, this);

        this.input.keyboard.on('keydown-Y', this.pressedY, this);
    }

    pressedZ(e)
    {
        this.clear_room();
        this.debuCounter += 1;
        this.drawRoom(this.debuCounter & 1);
    }

    pressedY(eve)
    {

    }

    disable_group_things()
    {
        /*
        for (const [a,b] of this.things_container)
        {
            console.log(a,b);
        }*/
        
        for (const thing of this.things_container.values())
        {
            thing.disableInteractive()
              .setActive(false)
              .setVisible(false)
              .rid = null
        }

        this.things_container.clear();
    
    } //end disable_group_things

    clear_room()
    {
        this.roomJson = null;
        this.roomscript = null;
        this.thingJson  = null;
        this.room_id = null;

        this.bg.setVisible(false);
        this.disable_group_things();
    }

    set_fonsEtOrigo(room_id)
    {
        this.roomJson = this.cache.json.get(`room${room_id}`);
        this.roomscript = RoomScripts[room_id];

        // maybe too redundant
        this.thingJson  = this.roomJson.things;
        this.room_id = room_id;
    }

    render_things()
    {
        const atlasKey = `atlas${Math.floor(this.room_id / 3)}`;

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
            this.things_container.set(idx, tsprite);
            
            tsprite.setDepth(thingData.kind);//.setActive(true).setVisible(true);
            tsprite.setActive(true);
            tsprite.setVisible(true)
            
            // if it's a new member, let's associate the listener for user interaction
            if (!tsprite.listenerCount(Phaser.Input.Events.POINTER_DOWN))
            {
                tsprite.on(Phaser.Input.Events.POINTER_DOWN, this.onthingdown);
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
                //tsprite.on('pointerdown', this.onthingdown)//RoomScripts[thingData_room_id][idx], this);
                tsprite.setInteractive();
            }
            
            if (thingData.skipCond && this.conditionIsSatisfied(thingData.skipCond))
            {
                console.log("Skipping",thingData);
                continue;
            }
        }
    }

    drawRoom(id)
    {
        console.log("NEW draw room");
        this.set_fonsEtOrigo(id);
        this.render_things();

        // hardcoded for now
        this.bg.setTexture(`atlas${Math.floor(this.room_id / 3)}`, this.roomJson.bg);
        this.bg.setVisible(true);
    }
/*
    drawRoomOLD(curr_room_id)
    {
        console.log(`** Drawing room: ${curr_room_id}`)
        const currAtlasName = `atlas${Math.floor(curr_room_id / 3) }`
        this.roomscript = RoomScripts[curr_room_id];
        
        const roomJson = this.cache.json.get(`room${curr_room_id}`)
        this.curr_room_id = curr_room_id;
        this.currentThings = roomJson.things;
        this.bg.setTexture(currAtlasName, roomJson.bg)

        for (const [index, curr] of this.currentThings.entries())
        {
            if (curr.skipCond && this.conditionIsSatisfied(curr.skipCond))
            {
                console.log("Skipping",curr);
                continue;
            }

            if (curr.kind === 1)
            {
                continue;
            }
                                
            const frameuffa = `${curr.frame}${curr.suffix? this.getVarFromArray(curr.suffix): ""}`
            const immy = this.thingsGroup.get(curr.x, curr.y, currAtlasName, frameuffa, true)
            immy.setDepth(curr.kind);//.setActive(true).setVisible(true);
            immy.texture.key === currAtlasName? immy.setFrame(frameuffa): immy.setTexture(currAtlasName, frameuffa);
            immy.setActive(true);
            immy.setVisible(true)
            this.things_container.set(index, immy);
            immy.rid = index;
            //console.log("immy.texture.key", immy.texture.key, "index", index);
            
            if (!immy.listenerCount(Phaser.Input.Events.POINTER_DOWN))
            {
                console.log("Attaching input listeners", Phaser.Input.Events.POINTER_DOWN)
                immy.on(Phaser.Input.Events.POINTER_DOWN, this.onthingdown);
            }
            else
            {
                console.log("Thing already has input listeners");
            }
            console.log("eventNames()", immy.eventNames(), "pointerdown amount:", immy.listenerCount('pointerdown'));

            if (curr.kind === 4)
            {
                immy.setOrigin(0.5, 1);
            }
            else
            {
                immy.setOrigin(0);
            }
            
            if (curr.noInteraction)
            {
                console.log("...but is input disabled");
                immy.disableInteractive(false);
                continue;
            }
            else
            {
                //immy.on('pointerdown', this.onthingdown)//RoomScripts[curr_room_id][index], this);
                immy.setInteractive();
            }
            
        }
    }*/

    onthingdown(a,b)
    {
        const scene = this.scene;
        console.log(`Clicked thing`,this.frame.name);// Math.random());
        //RoomScripts[scene.curr_room_id][this.rid].call(scene, this);
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

    toggleBit(ary)
    {
        return VarManager.newHandleAny(ary[0], ary[1], null, true);
    }
}
