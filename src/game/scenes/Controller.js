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
        //this.roomEmitter = this.add.timeline();
        //this.roomEmitter.on(RoomEvents.READY, this._test_ready, this);
        console.log("CONTROLLER", this.roomEmitter);
        this.text = this.add.bitmapText(8, 8, "font0", "+[Test SomEthinG]-! .1 (Ecche)").setDepth(1e9).setOrigin(0);
        this.input.keyboard.on('keydown-C', this.prezzed_c_cont, this);
        //this.scene.run('Viewport');
        //const temp_scene = this.scene.get('Viewport')
        //console.log("CONTROLLE FOUNF:", temp_scene.scene.key);
        //this.roomEmitter.on(Phaser.Time.Events.COMPLETE, temp_scene.userInteractionOn, temp_scene);
        //this.roomEmitter.on(Phaser.Time.Events.COMPLETE, () => console.log("TIMED EVENT STOCA ENDED OR NOT?"));
    }

    prezzed_c_cont()
    {
        this.scene.switch('Viewport');
    }

    _installScene(recScene)
    {
        console.log(`🪺 Controller receiving: ${recScene.scene.key}`);
        recScene.roomEmitter = this.roomEmitter;
        console.log(recScene.shield, recScene.roomEmitter)
        this._container.add(recScene);
        if (this._container.size === 1)
        {
            const [vp, co] = this.get_important_scenes();
            vp.drawRoom(0);
        }
    }

    get_important_scenes()
    {
        const res = [];
        for (const name of ['Viewport', 'Controller'])
        {
            res.push(this.scene.get(name))
        }
        return res;
    }

    _test_ready(viewport)
    {
        console.log(`Room has be rendered.\nParams: ${viewport.scene.key}`)
    }
}
