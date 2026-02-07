import { Scene } from 'phaser';

export class Preloader extends Scene
{
    tempx = 8;
    tempy = 14;
    constructor ()
    {
        super('Preloader');
    }

    init ()
    {
        console.log("🥚 PRELOADER SCENE");
        // this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-atlas0`, this.preliminary, this);
        this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-atlasbase`, this.onatlasbase, this);
        this.anims.on(Phaser.Animations.Events.ADD_ANIMATION, this.testAnim, this);
        // this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-ref_font`, this.makeRetroFont, this)

        this.maxLength = 53;
        //this.percent = 0;
        this.bar = this.add.bitmapText(22, 80, 'bootm', `\n${"a".repeat(this.maxLength)}`);
        this.redrawBar();
        this.load.on('progress', this.redrawBar, this);
        
    }

    redrawBar(val)
    {
        // console.log(val);
        // const val = 0.75
        this.bar.setText(`${Math.floor(val*100)}%\n${"a".repeat(Math.floor(this.maxLength * val))}`.padEnd(this.maxLength, "b"));
    }

    preload ()
    {
        //  Load the assets for the game - Replace with your own assets
        this.load.setPath('assets');

        this.load.atlas('atlasbase', 'atlasbase.png', 'atlasbase.json');
        this.load.atlas('atlas0', 'atlas0.png', 'atlas0.json');
    
        const maxRooms = 2;

        for (let i = 0; i < maxRooms; i++)
        {
            this.load.json(`room${i}`, `jsons/room${i}.json`)
        }
        
    }

    create()
    {
        this.load.off('progress', this.redrawBar, this);
        this.bar.destroy();

         this.input.keyboard.once('keydown-Z', ()=> {
            this.anims.off(Phaser.Animations.Events.ADD_ANIMATION);
            this.scene.start('Controller');
        });
        //this.scene.start('Controller');
    }

    onatlasbase()
    {
        
        console.log("atlasbase Loaded!");
        this.makeRetroFont();
        this.generateAnimations();

        const t =  this.textures.get('atlasbase');
        t.add(`pixel${String.fromCharCode(65)}`, 0, 56, 118, 1, 1);
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
        const {cutX, cutY, x, y} = this.textures.get('atlasbase').get('monospaced-font-eng');
        
        console.log("...making retro font...");
        const mainfont_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÈÌÒÙàèìòù 0123456789,.:;"!?+-*/=^<>%()[]{}`_#';
        const config = {
            image: 'atlasbase',
            width: 4,
            height: 6,
            chars: mainfont_chars,
            charsPerRow: 26
            // 'offset.x': cutX,
            // 'offset.y': cutY  
        };

        this.cache.bitmapFont.add('font0', Phaser.GameObjects.RetroFont.Parse(this, config));
        
        // hardcode add the ' character:
        const newfont = this.cache.bitmapFont.get('font0');

        newfont.data.chars[39] = newfont.data.chars[96];
        //console.log(newfont.data.chars, typeof newfont.data.chars)
    }

    generateAnimations()
    {
        const {anims} = this;
        const tempMap = new Map();
        tempMap.set('robot', [0, 1, 2, 3]);
        tempMap.set('guy', [0, 1, 2, 3]);
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

        console.log("ANIMS:", anims);
    }

    testAnim(key, animation)
    {
      //const {Between} = Phaser.Math
      const qqq = this.add.sprite(this.tempx, this.tempy).play(key).setOrigin(0); //Between(20, 240), Between(30, 100)).play(key)
      this.tempx += 30;
      if (this.tempx > 250)
      {
        this.tempx = 8;
        this.tempy += 28;
      }
      console.log(`Playing: ${key}`, qqq.x-8);
    }
}
