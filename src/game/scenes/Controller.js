import { Scene } from 'phaser';
import RoomEvents from './RoomEvents/genericRoomEvents.js'

export class Controller extends Scene
{
    roomEmitter;
    _container = new Set();

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
        // this.text = this.add.bitmapText(8, 8, "font0", "Press 'C'\n+[Test SomEthinG]-! .1 (Ecche)").setDepth(1e9).setOrigin(0);
        this.dbsSetList();
        this.input.keyboard.once('keydown-C', this.prezzed_c_cont, this);
        //this.scene.start('Viewport');
    }

    prezzed_c_cont()
    {
        this.scene.switch('Viewport');
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

    prepareBase()
    {
        this.dbsSelectionRect = this.add.image(6, 6, 'atlasbase', 'pixelA')
            .setOrigin(0)
            .setVisible(false)
            .setScale(190, 6);

        this.dbsList = this.add.bitmapText(8, 8, "font0", "Press 'x'")
            .setOrigin(0)
            .setVisible(false)
            .setInteractive()
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OVER, this.onListOver)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OUT, this.onListOut)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_MOVE, this.onListMove);

        this.dbsList.wordWrapCharCode = 160;
        this.dbsList.charColors.length = 0;

        this.dbsTitle = this.add.bitmapText(8, 98, "font0", "Press 'C'\n+[Test SomEthinG]-! .1 (Ecche)").setDepth(1e9).setOrigin(0);
    }

    dbsSetList(param)
    {
        if (param === undefined)
        {
            param = [
                'Exit',
                'Blammo 1.0',
                'ArmorAll 1.0',
                'BattleChess 2.0',
                'Hammer 2.0',
                'Logic Bomb 5.0',
                'DoorStop 4.0'
            ];
        }

        const list = [];

        const marker = 'X123456789';

        console.log(this.dbsList)

        for (const [idx, listItem] of param.entries())
        {
            list.push(`${marker.charAt(idx)}. ${listItem}`);
        }

        const {local} = this.dbsList.setText(list).getTextBounds();

        Phaser.Geom.Rectangle.CopyFrom(local, this.dbsList.input.hitArea);

        this.dbsList.setVisible(true);
    }

    onListOver()
    {
        this.scene.dbsSelectionRect.setVisible(true);
    }

    onListOut()
    {
        this.scene.dbsSelectionRect.setVisible(false);
        this.charColors.length = 0;
    }

    onListMove(pointer, locX, locY, event)
    {
        const {lineHeight} = this.fontData;
        this.scene.dbsSelectionRect.y = this.y + Math.floor(locY / lineHeight) * lineHeight;
        this.charColors.length = 0;
        const {word} = this.getTextBounds().words[Math.floor(locY / lineHeight)];
        //this.setCharacterTint()
        this.setWordTint(word, 1, true, this.scene.cameras.main.backgroundColor._color);
    }

    onListDown()
    {
        return;
    }

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
