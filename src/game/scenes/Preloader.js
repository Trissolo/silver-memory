import { Scene } from 'phaser';

export class Preloader extends Scene
{
    constructor ()
    {
        super('Preloader');
    }

    init ()
    {
        console.log("🥚 PRELOADER SCENE");
        this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-atlas0`, this.preliminary, this);
        this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-atlasbase`, this.onatlasbase, this);
        // this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-ref_font`, this.makeRetroFont, this)

        this.maxLength = 53;
        this.percent =         
        this.bar = this.add.bitmapText(22, 80, 'bootm', `\n${"a".repeat(this.maxLength)}`);
        this.redrawBar();
        this.load.on('progress', this.redrawBar, this);
        //this.load.once(Phaser.Loader.Events.COMPLETE, this.complete, this); //() => console.log("LOAD COMPLETE"));
    
        //  We loaded this image in our Boot Scene, so we can display it here
        //this.add.image(512, 384, 'background');

        //  A simple progress bar. This is the outline of the bar.
        //this.add.rectangle(11, 22, 168, 32).setStrokeStyle(1, 0xffffff).setOrigin(0);

        //  This is the progress bar itself. It will increase in size from the left based on the % of progress.
        //const bar = this.add.rectangle(11+1, 22+2, 4, 28, 0xffffff).setOrigin(0);

        //  Use the 'progress' event emitted by the LoaderPlugin to update the loading bar
        //this.load.on('progress', (progress) => {

            //  Update the progress bar (our bar is 464px wide, so 100% = 464px)
            //bar.width = 4 + (160 * progress);

        //});
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
        this.load.image('ref_font', 'monospaced_font_eng.png');

        const maxRooms = 2;

        for (let i = 0; i < maxRooms; i++)
        {
            this.load.json(`room${i}`, `jsons/room${i}.json`)
        }
        
    }

    create()
    {
        //this.add.bitmapText(80, 80, 'bootm', "123456R%a7890b");

        //  When all the assets have loaded, it's often worth creating global objects here that the rest of the game can use.
        //  For example, you can define global animations here, so we can use them in other scenes.

        //  Move to the MainMenu. You could also swap this for a Scene Transition, such as a camera fade.
        //this.redrawBar(0.666);
        this.load.off('progress', this.redrawBar, this);
        this.bar.destroy();

        //this.input.keyboard.once('keydown-Z', ()=> this.scene.start('Controller'));
        this.scene.start('Controller');
    }

    onatlasbase()
    {
        
        console.log("atlasbase Loaded!");
        this.makeRetroFont();
    }


    preliminary(a,b,c)
    {
        // console.log("******************Preliminary called");
        const t =  this.textures.get('atlas0');
        const hardcodedCoords = [
                [400, 0],
                [438, 132]
            ];

        for (const [idx, [x, y]] of hardcodedCoords.entries())
        {
            // console.log(idx, x, y);
            t.add(`pixel${String.fromCharCode(idx + 65)}`, 0, x, y, 1, 1);
        }
    }

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
}
