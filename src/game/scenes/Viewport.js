import VarManager from '../modules/VarManager.js';
import RoomScripts from '../roomscripts/roomscripts.js';
import { Scene } from 'phaser';

const mySignals = {THING_CLICKED: Symbol()}

export class Viewport extends Scene
{
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
        })
    } //end constructor

    init(data)
    {
        // console.log("INIIIIT", VarManager);
        this.debuCounter = 0;
        /*
        for (const elem of VarManager.varContainers.values())
        {
            // console.log("EKEM:", elem.typedArray)
        }*/
       /*
       // console.log("SET VALUESTOCA", VarManager.newHandleAny(0,2, 1))
       // console.log("SET VALUESTOCA", VarManager.newHandleAny(0,2, 0))
       // console.log("VALUESTOCA GET", VarManager.newHandleAny(0,2))
       */
    }

    create ()
    {
        this.cameras.main.setBackgroundColor(0x00ff00);
        this.input.setDefaultCursor('url("/assets/cursors/cross3.cur"), pointer');

        this.curr_room_id = null;
        this.currentThings = null;

        this.bg = this.add.image(0, 0, 'atlas0')
        .setDepth(-5)
        .setOrigin(0)

        this.thingsGroup = this.add.group({createCallback: function (thing)
            {
                thing.setInteractive({cursor: 'url("/assets/cursors/cover3.cur"), pointer', pixelPerfect: true})
                //console.log("GROUP MAMBER!", thing, thing.eventNames());
                //thing.on('pointerdown', thing.scene.onthingdown);
            }
        })

        this.visible_things = new Set();

        this.drawRoom(0);


        this.input.keyboard.on('keydown-Z', event => {

            this.disableGroupChildren(this.visible_things);
            this.debuCounter += 1;
            this.drawRoom(this.debuCounter & 1);

            //const hardcoded_test = VarManager.varContainers.get(0).typedArray;
            //hardcoded_test[0] = (this.debuCounter & 2)? 0: 255;

        });
    }

    disableGroupChildren(group = this.thingsGroup)
    {
        console.log("this.visible_things:", this.visible_things)
        
        for (const thing of group)//group.children.entries)
        {
            thing.disableInteractive()
              .setActive(false)
              .setVisible(false)
              //  .off('pointerover')//, thing.scene.thingOvered)
              //  .off('pointerout')//, thing.scene.thingOut)
              //.off('pointerdown')
              .rid = null

        }

        this.visible_things.clear();
    
    } //end disableGroupChildren

    drawRoom(curr_room_id)
    {
        console.log(`** Drawing room: ${curr_room_id}`)
        const currAtlasName = `atlas${Math.floor(curr_room_id / 3) }`
        this.roomscript = RoomScripts[curr_room_id];
        console.dir(`RS[${curr_room_id}]`, this.roomscript);
        
        const roomdata = this.cache.json.get(`room${curr_room_id}`)
        this.curr_room_id = curr_room_id;
        console.log("Roomdata", roomdata, "curr_room_id", curr_room_id);
        //return false;
        this.currentThings = roomdata.things;
        this.bg.setTexture(currAtlasName, roomdata.bg)
        //const palltextures = this.textures;
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
            this.visible_things.add(immy);
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
    }

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
