import { Scene } from 'phaser';

export class Boot extends Scene
{
    constructor ()
    {
        super('Boot');
    }
    
    init(data)
    {
        console.log("🧁 BOOT SCENE");//, Phaser.Loader.Events.FILE_KEY_COMPLETE);
    }
       

    preload ()
    {
        this.load.setPath('assets');
        //  The Boot Scene is typically used to load in any assets you require for your Preloader, such as a game logo or background.
        //  The smaller the file size of the assets, the better, as the Boot Scene itself has no preloader.
        /*
        this.load.atlas('atlas0', 'assets/atlas0.png', 'assets/atlas0.json');

        const maxRooms = 2;

        for (let i = 0; i < maxRooms; i++)
        {
            this.load.json(`room${i}`, `assets/jsons/room${i}.json`)
        }
        this.add.bitmapText(80, 80, 'bootm', "123456R%a7890b");
        */
        this.load.bitmapFont('bootm', 'bootnc.png', 'bootn.xml');
    }

    create()
    {
        //this.add.bitmapText(80, 80, 'bootm', "123456R%a7890b");
        this.scene.start('Preloader');
    }

}
