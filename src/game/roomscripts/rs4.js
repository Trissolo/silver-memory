import { Viewport } from "../scenes/Viewport";

export default class rs4
{
    // platform
    /**
     * 
     * @param {Phaser.GameObjects.Sprite} thing 
     * @this {Viewport}
     */
    static 0(thing)
    {
        // console.log(thing.rdata, thing.y, thing.scene);
        const {scene} = thing;
        const {worldX, worldY} = scene.input.activePointer;
        if (this.input.activePointer.middleButtonDown())
        {
            console.log(`Clicked on ${worldX}, {worldY}`);
            console.log(`Before Thing y: ${thing.y}, Actor.y: ${thing.scene.player.y}`);
            scene.player.setPosition(worldX, worldY);
            console.log(`After Thing y: ${thing.y}, Actor.y: ${thing.scene.player.y}`);
        }

    }

    // panelb
    static 1(thing){console.log(thing.frame.name);}

    // panela
    static 2(thing){console.log(thing.frame.name);}

    // AREA
    static 3(thing){console.log(thing.frame.name);}
}
