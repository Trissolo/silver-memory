import { Viewport } from "../scenes/Viewport";

// export default class rs4
const rs4 = {
    // platform
    /**
     * 
     * @param {Phaser.GameObjects.Sprite} thing 
     * @this {Viewport}
     */
    0(thing)
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

    },

    // panelb
    1(thing){console.log(thing.frame.name);},

    // panela
    2(thing){console.log(thing.frame.name);},

    // AREA
    3(ta)
    {
        console.log("Not a CLass ;) But a Method!");
        this.toAnotherRoom(ta, 3, 22, 67, "E", 0);
    }
}

export default rs4
