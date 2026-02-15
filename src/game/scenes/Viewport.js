import VarManager from '../modules/VarManager.js';
import RoomScripts from '../roomscripts/roomscripts.js';
import { NONE, Scene } from 'phaser';

// specials
import RoomBackground from '../modules/RoomBackground.js';
import Shield from '../modules/Shield.js';
import Actor from '../modules/Actor.js';
import RoomEvents from './RoomEvents/genericRoomEvents.js'

export class Viewport extends Scene
{
    roomEmitter;
    roomId;
    roomJson;
    thingsJson;
    thingsContainer;
    roomscript;
    bg;
    shield;
    player;
    varyingDepthSprites = new Set();
    Rnd = Phaser.Math.RND

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
                //'Loader',  //this.load
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
        //this.events.once('create', this.scene.get('Controller')._installScene, this.scene.get('Controller'))//, sce.scene.key));
        // this.events.once(Phaser.Scenes.Events.CREATE, () => console.log("🔮 Viewport CREATE (not READY) called"));
        console.log(`🍰 Running Vievport 'init'`)//, this);
        // console.log("Vars", VarManager)
        this.debuCounter = 0;
        this.events.once('destroy', this.onDestroy, this);
    }

    create ()
    {
        // random preliminary stuff:
        this.cameras.main.setBackgroundColor(0x00ff00);
        this.input.setDefaultCursor('url("/assets/cursors/cross3.cur"), pointer');

        // 1) background image
        this.bg = new RoomBackground(this);

        //scriptedAction
        this.roomEmitter = this.add.timeline();
        this.roomEmitter.on(Phaser.Time.Events.COMPLETE, this.userInteractionOn, this);

        // 2) Room 'things'
        this.thingsGroup = this.add.group({createCallback: function (thing)
            {
                thing.setInteractive({cursor: 'url("/assets/cursors/cover3.cur"), pointer', pixelPerfect: true})
                thing.setVisible(false);
                thing.rdata = null;
            }
        })

        // 2b) container for 'things'
        this.thingsContainer = new Map();

        // player
        this.player = new Actor(this, 0, 'robot');

        // shield
        this.shield = new Shield(this);

        //test text
        //this.text = this.add.bitmapText(8, 8, "font0", "+[Test SomEthinG]-! .1 (Ecche)").setDepth(1e9).setOrigin(0);

        // Depth sorting
        this.events.on('prerender', this.sortByHeight, this);

        // code for test
        this.input.keyboard.on('keydown-Z', this.pressedZ, this);

        this.input.keyboard.on('keydown-X', this.pressedX, this);

        this.input.keyboard.on('keydown-C', this.pressedC, this);

        // START
        this.drawRoom(0);
        ;
    }

    pressedC()
    {
        console.clear();
        this.player.turnAndStayStill("N")
        //this.player.setState(1);
        //this.bg.benchmarkRotation();
    }

    pressedZ(eve)
    {
        this.clear_room();
        this.debuCounter = this.nextIntInRange(this.debuCounter, 0, 4, false); //+= 1;
        if (this.debuCounter === 3)
        {
            this.debuCounter = 4;
        }
        this.drawRoom(this.debuCounter); // & 1);
    }

    pressedX(eve)
    {
        //this.scene.get('Controller').text.setText(`${Math.random()} Moscagain`);
        //this.scene.switch('Controller');
        this.player.testRot();
        /*
        console.log("roomId is:", this.roomId);
        VarManager._debug();
        this.shield.active? this.shield.lower(): this.shield.raise();
        this.cameras.main.shake(650, 0.01);
        console.log("TEST_this.getVarValue");
        console.log(`${this.getVarValue()} <---`)
        */
    }

    onDestroy()
    {
        super.destroy();
        this.thingsContainer.clear();
        this.roomEmitter = null;
        this.bg.destroy();
        this.bg = null;
        this.shield.destroy();
        this.shield = null;
        this.thingsGroup.destroy();
        this.thingsGroup = null;
    }

    getScript(roomId)
    {
        return RoomScripts[roomId];
    }

    disable_group_things()
    {      
        for (const thing of this.thingsContainer.values())
        {
            thing.disableInteractive()
              .setActive(false)
              .setVisible(false)
              .setState(null)
              .rdata = null;
              //.rid = null
        }

        this.thingsContainer.clear();
    
    } //end disable_group_things

    clear_room()
    {
        this.roomJson = null;
        this.roomscript = null;
        this.thingsJson  = null;
        this.roomId = null;

        this.varyingDepthSprites.clear();

        this.bg.hide() //setVisible(false);

        this.player.hide();

        this.disable_group_things();
    }

    set_fonsEtOrigo(roomId)
    {
        this.input.enabled = false;
        this.roomJson = this.getJson(roomId);
        this.roomscript = this.getScript(roomId); ////RoomScripts[roomId];

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
            
            console.log("🫓 Super imp", "Active", tsprite.active, "Visible:", tsprite.visible, "State (ex .rid):", tsprite.state);
            
            // set the frame, or, if needed, the texture
            const assembledFrameName = `${thingData.frame}${thingData.suffix? this.getVarValue(thingData.suffix): ""}`;
            //console.log(`AtlasKey: ${atlasKey}\nCurrent sprite texture: ${tsprite.texture.key}`)
            tsprite.texture.key === atlasKey? tsprite.setFrame(assembledFrameName): tsprite.setTexture(atlasKey, assembledFrameName);
            
            // Room ID!
            //tsprite.rid = idx;
            tsprite.setState(idx);
            tsprite.rdata = thingData;
            
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
                this.varyingDepthSprites.add(tsprite);
            }
            else
            {
                tsprite.setOrigin(0, 0);
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
        this.input.enabled = false;
        this.set_fonsEtOrigo(id);
        
        this.render_things();
        this.roomEmitter.emit(RoomEvents.THINGSREADY, this);

        this.bg.assignTexture(id);
        console.log(this.bg.show().name);

        this.handleActors();

        this.roomEmitter.emit(RoomEvents.READY, this);
        this.input.enabled = true;
        //console.log("pollRate", this.input.pollRate)
    }

    //the scope is the GameObject
    onThingDown(a,b)
    {
        const scene = this.scene;
        console.log(`Clicked thing`,this.frame.name);
        scene.roomscript[this.state].call(scene, this);

    }

    // varsvars
    getVarValue(vcoords)
    {
        if (Array.isArray(vcoords))
        {
            console.warn(`'getVarValue' received an array, then attempted to consider the value at position [0]`, ary)
            vcoords = vcoords[0];
        }
        return VarManager.newHandleAny(vcoords & 3, vcoords >>> 2);
    }

    conditionIsSatisfied(ary)
    {
        console.log(`'conditionIsSatisfied' param length: ${ary.length}`);
        return VarManager.newHandleAny(ary[0] & 3, ary[0] >>> 2) === ary[1];
    }

    setVariable(vcoords, newValue)
    {
        // if (Array.isArray(ary))
        // {
        //    ary = ary[0];
        // }
        console.log("'setVariable' Param is array?", Array.isArray(vcoords));
        // console.log(`Writing the value: ${newValue} to var identified with kind: ${ary&3}, idx: ${ary>>>2}`);
        VarManager.newHandleAny(vcoords & 3, vcoords >>> 2, newValue);
    }

    setAsCondition(condition_ary)
    {
        this.setVariable(condition_ary[0], condition_ary[1]);
    }

    toggleBit(vcoords)
    {
        //console.log("Toggle param is array? (An INTEGER is required)", Array.isArray(vcoords));
        if (Array.isArray(vcoords))
        {
            vcoords = vcoords[0];
        }
        return VarManager.newHandleAny(vcoords & 3, vcoords >>> 2, null, true);
    }

    // end varsvars

    // unused
    getRoomJson(roomId)
    {
        return roomId === undefined? this.roomJson : this.cache.json.get(`room${roomId}`)
    }

    // unused
    getThingsJson(roomId)
    {
        return roomId === undefined? this.thingsJson : this.getRoomJson(roomId).things;
    }

    getJson(roomId)
    {
        // console.log(`Getting JSON for room: ${roomId}`);
        return this.cache.json.get(`room${roomId}`);
    }

    // used
    getExistentThing(rid)
    {
        if (!this.thingsContainer.has(rid))
        {
            console.warn(`Current room (${this.roomId}) does not contains any Thing with rid ${rid}`);
            return false
        }
        return this.thingsContainer.get(rid);
    }

    // unused
    // setThingNotVisible(thing)
    // {
    //     //rid = typeof thing === "number"? rid : thing.rid;
    //     gameObject = null
    //     const varAry = this.thingsJson[rid]
    // }

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

    refreshSpriteFrame(go)
    {
        //console.log("Number.isInteger", Number.isInteger(quickValue));
        return go.setFrame(`${go.rdata.frame}${this.getVarValue(go.rdata.suffix)}`);
    }

    scrollSpriteFrame(go, maxLimit = 1, backwards = false)
    {
        const vcoord = go.rdata.suffix;
        const value = this.getVarValue(vcoord);
        this.setVariable(vcoord, this.nextIntInRange(value, 0, maxLimit, backwards));
        this.refreshSpriteFrame(go);
    }

    _message(m = "Some message")
    {
        console.log(m, "THIS:", this);
    }

    userInteractionOff()
    {
        this.shield.raise();
    }

    userInteractionOn()
    {
        this.roomEmitter.clear().events.length = 0;
        this.shield.lower();
        this.input.setDefaultCursor('url("/assets/cursors/cross3.cur"), pointer');
    }

    prepareRoomEvent(ary, raiseshield = true, immediatePlay = true, onceComplete, scope)
    {
        const {roomEmitter} = this;
        if (roomEmitter.events.length)
        {
            console.log("Clearing 'roomEmitter");
            roomEmitter.clear().events.length = 0;
        }

        if (raiseshield)
        {
            roomEmitter.add(
                {at: 0, target: this, run: this.userInteractionOff});            
        }

        roomEmitter.add(ary);

        if (roomEmitter.listenerCount('complete') === 1)
        {
            console.log("No pending 'complete' events");
        }
        else
        {
            console.warn("RoomEmitter still has pending 'complete' events!");
            console.warn(roomEmitter.listenerCount('complete'))
        }

        if (onceComplete)
        {
            roomEmitter.once(Phaser.Time.Events.COMPLETE, onceComplete, scope)
        }

        if (immediatePlay)
        {
            roomEmitter.play();
        }

        return roomEmitter;
    }

    handleActors()
    {
        const {player} = this;
        // player.setPosition(165, 125);
        player.setPosition(180, 76);
        const animName = `${this.player.costume}_rotate`;
        this.player.show()
        .setFrame(Phaser.Utils.Array.GetRandom([...this.player.rotFrames.values()]).textureFrame);
        //.play(animName)
        //.setFrame('robot_walk_NE_0')
        this.varyingDepthSprites.add(this.player);

        //console.log(this.anims.anims.entries)
        // this.tweens.add({
        //     targets: player,
        //     y: 118,
        //     yoyo: true,
        //     duration: 3000,
        //     repeat: -1
        // });
    }

    sortByHeight()
    {
        for (const elem of this.varyingDepthSprites)
        {
            elem.setDepth(elem.y);
        }
        //this.children.depthSort();
    }
}
