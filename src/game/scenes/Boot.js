import { Scene } from 'phaser';

export class Boot extends Scene
{
    constructor ()
    {
        super('Boot');
    }
    
    init(data)
    {
        console.log("🧁 BOOT SCENE");
    }
       

    preload ()
    {
        this.load.setPath('assets');
        
        this.load.bitmapFont('bootm', 'bootnc.png', 'bootnc.xml');
    }

    create()
    {
        this.registry.set("roomData", new Map());

        this.scene.start('Preloader');
    }

}
