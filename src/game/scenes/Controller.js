import { Scene } from 'phaser';
import RoomEvents from './RoomEvents/genericRoomEvents.js'
import DataBaseList from '../modules/DataBaseList.mjs';

export class Controller extends Scene
{
    roomEmitter;
    // _container = new Set();

    dbsList;

    constructor ()
    {
        super('Controller');
    }

    init(data)
    {
        console.log("🥝 Controller Scene");
    }

    create ()
    {
        // console.log("CONTROLLER") //, this.roomEmitter);

        this.prepareBase();

        this.dbsList.setList(); // ['Exit to Main', 'Cryptology 1.0', 'CopTalk 4.0']);

        this.input.keyboard.once('keydown-C', this.prezzed_c_cont, this);

        this.input.keyboard.on('keydown-M', this.pressedM, this);

        // this.scene.start('Viewport');
    }

    prezzed_c_cont()
    {
        this.scene.switch('Viewport');
    }

    pressedM()
    {
        console.log('Controller: pressed M-key');

        this.dbsList.forceSelection(2);
    }

    prepareBase()
    {
        this.dbsSelectionRect = this.add.image(16, 6, 'atlasbase', 'pixelA')
            .setOrigin(0)
            .setVisible(false)
            .setScale(190, 6);

        this.dbsList = new DataBaseList(this);

        this.dbsTitle = this.add.bitmapText(8, 98, "font0", "Press 'C'")
            .setDepth(1e9)
            .setOrigin(0);
    }

    

    // _installScene(recScene)
    // {
    //     console.log(`🪺 Controller receiving: ${recScene.scene.key}`);
    //     recScene.roomEmitter = this.roomEmitter;
    //     console.log(recScene.shield, recScene.roomEmitter)
    //     this._container.add(recScene);
    //     if (this._container.size === 1)
    //     {
    //         const [vp, co] = this.get_important_scenes();
    //         vp.drawRoom(0);
    //     }
    // }

    
    // get_important_scenes()
    // {
    //     const res = [];
    //     for (const name of ['Viewport', 'Controller'])
    //     {
    //         res.push(this.scene.get(name))
    //     }
    //     return res;
    // }

    // _test_ready(viewport)
    // {
    //     console.log(`Room has be rendered.\nParams: ${viewport.scene.key}`)
    // }
}
