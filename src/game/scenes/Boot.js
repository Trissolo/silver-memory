import { Scene } from 'phaser';

export class Boot extends Scene
{
    constructor ()
    {
        super('Boot');
    }
    
    init(data)
    {
        // console.log("qqq", Phaser.Loader.Events.FILE_KEY_COMPLETE);
        this.load.once(`${Phaser.Loader.Events.FILE_KEY_COMPLETE}image-atlas0`, this.preliminary, this)
        this.load.once(Phaser.Loader.Events.COMPLETE, this.complete, this); //() => console.log("LOAD COMPLETE"));
    }

    preload ()
    {
        //  The Boot Scene is typically used to load in any assets you require for your Preloader, such as a game logo or background.
        //  The smaller the file size of the assets, the better, as the Boot Scene itself has no preloader.

        this.load.atlas('atlas0', 'assets/atlas0.png', 'assets/atlas0.json');

        const maxRooms = 2;

        for (let i = 0; i < maxRooms; i++)
        {
            this.load.json(`room${i}`, `assets/jsons/room${i}.json`)
        }
    }

    complete()
    {
        this.scene.start('Preloader');
    }

    preliminary(a,b,c)
    {
        const t =  this.textures.get('atlas0');
        const hardcodedCoords = [
                [400, 0],
                [438, 132]
            ];

        for (const [idx, [x, y]] of hardcodedCoords.entries())
        {
            console.log(idx, x, y);
            t.add(`pixel${String.fromCharCode(idx + 65)}`, 0, x, y, 1, 1);
        }
    }
}
