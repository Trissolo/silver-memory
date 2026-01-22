import { Scene } from 'phaser';

export class Boot extends Scene
{
    constructor ()
    {
        super('Boot');
    }

    preload ()
    {
        //  The Boot Scene is typically used to load in any assets you require for your Preloader, such as a game logo or background.
        //  The smaller the file size of the assets, the better, as the Boot Scene itself has no preloader.

        //this.load.image('background', 'assets/bg.png');
        this.load.atlas('atlas0', 'assets/atlas0.png', 'assets/atlas0.json');
        //this.load.json("roomdata", 'assets/jsons/roomdata.json',)
        for (let i = 0; i < 2; i++)
        {
            this.load.json(`room${i}`, `assets/jsons/room${i}.json`)
        }
    }

    create ()
    {
        this.scene.start('Preloader');
    }
}
