import { Scene } from 'phaser';
import PMStroll from '../modules/actorStuff/pmStroll/PMStroll.mjs';

export class Preloader extends Scene
{
    // 53 character for the loading bar
    maxLength = 53;

    // Precalculated room amount:
    roomAmount = 5;

    tempTasks = [];

    //shared Map with room data:
    roomDataMap;

    tempx = 2;
    tempy = 0;
    constructor ()
    {
        super('Preloader');
    }

    init ()
    {
        console.log("🥚 PRELOADER SCENE");

        // the progress bar
        this.bar = this.add.bitmapText(22, 80, 'bootm', `\n${"a".repeat(this.maxLength)}`);

        this.redrawBar();

        // Some event
        this.load
            .once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-atlasbase`, this.onatlasbase, this)
            .once(Phaser.Loader.Events.COMPLETE, this.listenerAllLoaded, this)
            .on(Phaser.Loader.Events.PROGRESS, this.redrawBar, this);
            // .on(Phaser.Loader.Events.FILE_COMPLETE, this.listenerOnFileComplete, this);
        
        this.anims.on(Phaser.Animations.Events.ADD_ANIMATION, this.testAnim, this); 
        
        // 'global RoomData'
        this.roomDataMap = this.registry.get('roomData');
        // console.log("RoomData", this.roomDataMap, this.roomDataMap.size)
    }

    preload ()
    {
        // Load the assets for the game - Replace with your own assets
        this.load.setPath('assets');

        this.load.atlas('atlasbase', 'atlasbase_tp.png', 'atlasbase_tp.json');
        this.load.atlas('atlas0', 'atlas0.png', 'atlas0.json');
        this.load.atlas('atlas1', 'atlas1.png', 'atlas1.json');
    
        for (let i = 0; i < this.roomAmount; i++)
        {
            const roomJsonKey = `room${i}`
            this.load
                .json(roomJsonKey, `jsons/room${i}.json`)
                .once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}json-${roomJsonKey}`, this.singleJsonLoaded, this)
        }
        
    }

    singleJsonLoaded(key, type, data)
    {
        console.log(`🟢 (singleJsonLoaded) Room .${type}: ${key}`, "Is correct?", Object.hasOwn(data, "id"));

        // Store the data in the Map in Registry:
        this.roomDataMap.set(data.id, data);

        // Da this room has some VisibilityMaps?
        if (data.polys_params && data.polys_params.length)
        {
            const {polys_params} = data;

            // const {length: totalVisibilityMapPerRoom} = polys_params;

            const visMaps = [];

            // Build each Visibility Map!

            for (const [idx, visibilityMapParam] of polys_params.entries())
            {
                // const {length: polygonsPerMap} = visibilityMapParam;

                visMaps.push(PMStroll.addVisibilityMap(visibilityMapParam));

                // console.log(`   🟣 Room [${data.id}] VisMap: ${idx+1}/${totalVisibilityMapPerRoom} contains ${polygonsPerMap} poly.`); //, visibilityMapParam);
            }

            // Add the VisMap directly on the roomData:
            data.visMaps = visMaps;

            // Remove the params:
            delete data.polys_params;

            // console.dir(data);
        }
        
    } // end singleJsonLoaded

    create()
    {
        this.load.off(Phaser.Loader.Events.PROGRESS, this.redrawBar, this);

        this.bar.destroy();

        // this.anims.off(Phaser.Loader.Events.ADD_ANIMATION, this.testAnim, this, false);

        // temporary stuff
        console.log("Registry:", this.registry, "Cache is Registry?", this.registry === this.cache);

        this.input.keyboard.once('keydown-Z', this.allTasksDone, this);
    }

    checkTasks()
    {

    }

    allTasksDone()
    {
        this.anims.off(Phaser.Animations.Events.ADD_ANIMATION);

        //console.log("Cache:", this.cache.json.getKeys(), this.cache.json);
        // do not use the Cache:
        for (const key of this.cache.json.getKeys())
        {
            console.log(`Removing: ${key}`);

            this.cache.json.remove(key);
        }

        console.log("Registry:", this.roomDataMap);

        this.scene.start('Controller');
    }

    listenerAllLoaded(loader, totalComplete, totalFailed)
    {
        console.log(`Loaded: ${totalComplete} files. ${totalFailed === 0}`);//? "All files loaded!": "Something wrong happens."}`);
    }

    // listenerOnFileComplete(key, type, data)
    // {
    //     console.log(`File Complete: ${key}, type: ${type}`);
    // }

    redrawBar(val)
    {
        this.bar.setText(`${Math.floor(val*100)}%\n${"a".repeat(Math.floor(this.maxLength * val))}`.padEnd(this.maxLength, "b"));
    }

    onatlasbase()
    {
        // console.log("atlasbase Loaded!");

        this.makeRetroFont();

        this.generateAnimations();

        const t =  this.textures.get('atlasbase');

        //hardcoded coords: x:24, y: 5
        t.add(`pixel${String.fromCharCode(65)}`, 0, 24, 5, 1, 1);
        // this.add.bitmapText(50, 50, 'font0', "ESFT£");
    }


    // preliminary(a,b,c)
    // {
    //     console.log("******************Preliminary called");
    //     const t =  this.textures.get('atlas0');
    //     const hardcodedCoords = [
    //             [400, 0],
    //             [438, 132]
    //         ];

    //     for (const [idx, [x, y]] of hardcodedCoords.entries())
    //     {
    //         // console.log(idx, x, y);
    //         t.add(`pixel${String.fromCharCode(idx + 65)}`, 0, x, y, 1, 1);
    //     }
    //     // button animation just for test
    //         /* this.anims.create({
    //             key: 'blinkingButton',
    //             defaultTextureKey: 'atlas0',
    //             frames: [550, 222].map( (el, idx) => ({frame: `button${idx}`, duration: el})  ),
    //             repeat: -1//,
    //             //frameRate:10
    //         }); */
    // }

    makeRetroFont()
    {
        const fontFrame = this.textures.get('atlasbase').get('monospaced_font_eng');
        
        const {cutX, cutY} = fontFrame;

        // console.dir("DOUBT:", fontFrame,`cutX: ${cutX}, cutY: ${cutY}`);

        // console.log("...Making retro font...");
        const mainfont_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÈÌÒÙàèìòù 0123456789,.:;"!?+-*/=^<>%()[]{}`_#';
        const config = {
            image: 'atlasbase',
            width: 4,
            height: 6,
            chars: mainfont_chars,
            charsPerRow: 26,
            'offset.x': cutX - 1,
            'offset.y': cutY - 1  
        };

        this.cache.bitmapFont.add('font0', Phaser.GameObjects.RetroFont.Parse(this, config));
        
        // hardcode add the ' character:
        const newfont = this.cache.bitmapFont.get('font0');

        newfont.data.chars[39] = newfont.data.chars[96];
    }

    generateAnimations()
    {
        const {anims} = this;
        const tempMap = new Map();
        tempMap.set('robot', [1, 2, 3]);
        tempMap.set('guy', [1, 2, 3, 0]);
        const cardinalsPoints = ["W", "NW", "N", "NE", "E", "SE", "S", "SW"];

        let isRobot = true
        for (const [costume, frameNumbers] of tempMap)
        {
            // walk animations:
            for (const direction of cardinalsPoints)
            {
                const animkey = `${costume}_walk_${direction}`;

                anims.create(
                    {
                        key: animkey,
                        defaultTextureKey: 'atlasbase',
                        frames :  frameNumbers.map(  el => ({frame: `${animkey}_${el}`})  ),
                        skipMissedFrames: false,
                        repeat: -1,
                        frameRate: isRobot? 8: 6
                    });

                // interact animation (Not sure if is needed in game - maybe a simple 'setFrame'?)
                anims.create({
                    key: `${costume}_interact_${direction}`,
                    frames: ['interactCenter', 'walk'].map((action, idx) => ({frame: `${costume}_${action}_${direction}_0`, duration: idx===0?960:80})),
                    defaultTextureKey: 'atlasbase',
                    skipMissedFrames: false,
                    repeat: 0 //,
                    //frameRate: 10
                    });
                    
            }

            // rotation clockwise
            anims.create({
                        key: `${costume}_rotate`,
                        defaultTextureKey: 'atlasbase',
                        frames: cardinalsPoints.map(  el => ({ frame: `${costume}_walk_${el}_${isRobot?0:3}` })  ),
                        skipMissedFrames: false,
                        repeat: -1,
                        frameRate: 10
                    });

            isRobot = false
        }

        // console.log("ANIMS:", anims);
        // console.log(framename.slice(0, framename.at(-4) === "_"? -3:-4));
    }

    testAnim(key, animation)
    {
        // if (key.startsWith('guy'))
        // {
            //const {Between} = Phaser.Math
            const qqq = this.add.sprite(this.tempx, this.tempy).play(key).setOrigin(0); //Between(20, 240), Between(30, 100)).play(key)
            this.tempx += 30;
            if (this.tempx > 240)
            {
                this.tempx = 2;
                this.tempy += 26;
            }
        //}

        //console.log(`Playing: ${key}`, animation);
    }
}
