import VarManager from '../modules/VarManager.js';
import RoomScripts from '../roomscripts/roomscripts.js';
import { NONE, Scene } from 'phaser';
import PMStroll from '../modules/actorStuff/pmStroll/PMStroll.mjs';

// specials
import RoomBackground from '../modules/RoomBackground.js';
import Shield from '../modules/Shield.js';
import Actor from '../modules/Actor.js';
import RoomEvents from './RoomEvents/genericRoomEvents.js'
import TriggerZoneManager from '../modules/triggerZoneManager.mjs';

export class Viewport extends Scene
{
    roomEmitter;
    roomId;
    roomJson;
    thingsJson;
    roomsData;
    thingsContainer;
    triggerZone;
    roomscript;
    bg;
    shield;
    player;
    actors = [];
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
                roundPixels: true,
                backgroundColor: "#008777" //,
                //y: 11, // 136,
                //height: 64
            }
        });
    } //end constructor

    init(data)
    {
        // Registry, not cache
        this.roomsData = this.registry.get('roomData');
        //this.events.once('create', this.scene.get('Controller')._installScene, this.scene.get('Controller'))//, sce.scene.key));
        // this.events.once(Phaser.Scenes.Events.CREATE, () => console.log("🔮 Viewport CREATE (not READY) called"));
        console.log(`🍰 Running Viewport 'init'`)//, this);
        // console.log("Vars", VarManager)
        this.debuCounter = 0;
        this.events.once('destroy', this.onDestroy, this);
    }

    create ()
    {
        // random preliminary stuff:
        this.cameras.main.setBackgroundColor(0x00ff00);
        // console.log(this.cameras.main, this.cameras.main.setRoundPixels(true));
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
                .setVisible(false)
                .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, thing.scene.onThingDown)
                .rdata = null;
            }
        });

        // 2b) Room's triggerzones
        this.triggerZone = new TriggerZoneManager(this);

        // 2c) container for 'things'
        this.thingsContainer = new Map();

        // player
        for (const [idx, costume] of ["robot", "guy"].entries())
        {
            this.actors.push(new Actor(this, idx, costume));
        }
            
        this.player = this.actors[0];

        this.pmstroll = PMStroll.useDebug(this);

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
        //console.clear();
        //this.player.turnAndStayStill("N");
        // console.log("Player legal", this.player.inAllowedPosition());
        //this.player.walkTo(this.player.x + 1, this.player.y);
        //const {x} = this.player;
        
        //this.player.setState(1);
        //this.bg.benchmarkRotation();
    }

    pressedZ(eve)
    {
        //this.clear_room();

        this.debuCounter = this.nextIntInRange(this.debuCounter, 0, 4, false);
        
        this.drawRoom(this.debuCounter);
    }

    pressedX(eve)
    {
        console.log("Pressed 'X'");

        // VarManager._debug();
    }

    onDestroy()
    {
        console.log('Destroy called');
        this.thingsContainer.clear();
        this.roomEmitter = null;
        this.bg.destroy();
        this.bg = null;
        this.shield.destroy();
        this.shield = null;
        this.thingsGroup.getChildren().forEach(el => el.destroy());
        this.thingsGroup.destroy();
        this.thingsGroup = null;
        this.player = this.actors.forEach(elem => elem.destroy());
        this.actors.length = 0;
        PMStroll.debug.graphics.destroy();
        PMStroll.debug = undefined;
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

        this.player.hide().walk.stopAndClear();

        this.cameras.main.stopFollow();

        this.disable_group_things();
    }

    set_fonsEtOrigo(roomId)
    {
        this.clear_room();
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

        let roomThing;

        for (const [idx, thingData] of this.roomJson.things.entries())
        {
            if (thingData.kind === 1)
            {
                //continue;
                roomThing = this.triggerZone.get();
                roomThing.input.hitArea.setTo(...thingData.rect);
                console.log("Rect hitArea:", roomThing.input.hitArea);
            }
            else
            {
                roomThing = this.thingsGroup.get(thingData.x, thingData.y);
                // set the frame, and, if needed, the texture
                const assembledFrameName = `${thingData.frame}${thingData.suffix? this.getVarValue(thingData.suffix): ""}`;
                roomThing.texture.key === atlasKey? roomThing.setFrame(assembledFrameName): roomThing.setTexture(atlasKey, assembledFrameName);
            }
                                
            
            roomThing
                .setDepth(thingData.kind)
                .setActive(true)
                .setState(idx) // Unique ID of the thing among all the things in the room
                .rdata = thingData;
            
            // let's keep this thing in its container
            this.thingsContainer.set(idx, roomThing);
            
            // console.log("eventNames()", roomThing.eventNames(), "pointerdown amount:", roomThing.listenerCount('pointerdown'));

            // deepthsorted?
            if (thingData.kind === 4)
            {
                roomThing.setOrigin(0.5, 1);
                this.varyingDepthSprites.add(roomThing);
            }
            else
            {
                roomThing.setOrigin(0, 0);
            }
            
            if (thingData.noInteraction)
            {
                roomThing.disableInteractive(false);

                // do we really have to continue?
                continue;
            }
            else
            {
                roomThing.setInteractive();
            }
            
            if (thingData.skipCond && this.conditionIsSatisfied(thingData.skipCond))
            {
                console.log("Skipping",thingData);
                continue;
            }
            else
            {
                roomThing.setVisible(true);
            }
        }
    }

    drawRoom(id)
    {
        this.input.enabled = false;
        this.set_fonsEtOrigo(id);
        
        this.render_things();
        //this.roomEmitter.emit(RoomEvents.THINGSREADY, this);

        this.bg.assignTexture(id).show();

        this.handleActors();

        // this.roomEmitter.emit(RoomEvents.READY, this);

        // optional Room script
        this.roomscript.onRoomReady?.call(this);

        this.input.enabled = true;

        // this.roomscript[2]?.call(this, this.bg);
    }

    //the scope is the GameObject
    onThingDown(pointer) //, localX, localY, event)
    {
        const scene = this.scene;

        console.log(`Clicked thing`, this.type, /*this.frame.name,*/ "pointer:", pointer);

        scene.roomscript[this.state].call(scene, this, pointer);
    }

    // varsvars
    getVarValue(vcoords)
    {
        if (Array.isArray(vcoords))
        {
            console.warn(`'getVarValue' received an array, then attempted to consider the value at position [0]`, ary);

            vcoords = vcoords[0];
        }
        return VarManager.newHandleAny(vcoords & 3, vcoords >>> 2);
    }

    conditionIsSatisfied(ary)
    {
        return VarManager.newHandleAny(ary[0] & 3, ary[0] >>> 2) === ary[1];
    }

    setVariable(vcoords, newValue)
    {
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
    getThingsJson(roomId)
    {
        return roomId === undefined? this.thingsJson : this.getRoomJson(roomId).things;
    }

    getJson(roomId)
    {
        // console.log(`Getting JSON for room: ${roomId}`);
        // return roomId === undefined? this.roomJson : this.roomsData.get(roomId);
        return this.roomsData.get(roomId);
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

        // Place at the center of the room texture
        player.setPosition(this.bg.input.hitArea.width >> 1, this.bg.input.hitArea.height >> 1);

        this.player
        .setPolygonalMapByIndex()
        .show()
        .setFrame(Phaser.Utils.Array.GetRandom([...this.player.rotFrames.values()]).textureFrame);

        // camera follow
        
        this.cameras.main.startFollow(this.player, true);

        // Deepth Sort!
        this.varyingDepthSprites.add(this.player);
    }

    sortByHeight()
    {
        for (const elem of this.varyingDepthSprites)
        {
            elem.setDepth(elem.y);
        }

        //this.children.depthSort();
    }

    // update(time, delta)
    // {
    //     if (this.player.walk.aTargetExists)
    //     {
    //         console.log("Walking...");
    //         this.pmstroll.debug.lineFromVecs(this.player.walk.startCoords, this.player.walk.endCoords, 0xffffff);
    //     }
    // }
}
