import ThingDataHelper from "./mixins/thingDataHelper.mjs";

/**
 * @mixes ThingDataHelper
 */

class Thing extends Phaser.GameObjects.Sprite
{
    isThing = true;
    isTriggerArea = false;
    rdata = null;
    thingIdx = null

    constructor(scene, x, y)
    {
        super(scene, x, y)
        this
        .setActive(false)
        .setVisible(false)
        //.setState(null)
        .setInteractive({cursor: 'url("/assets/cursors/cover3.cur"), pointer', pixelPerfect: true})
        .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, this.scene.onThingDown)
        .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OVER, this.scene.onThingOver)
        .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OUT, this.scene.labelManager.hideLabel, this.scene.labelManager)
        .on(Phaser.Input.Events.GAMEOBJECT_POINTER_MOVE, this.scene.labelManager.setLabelPosition, this.scene.labelManager)
        
        .addToDisplayList();

        this.scene.cameras.cameras[1].ignore(this);
        console.log(`Thing: ${this} typeof Thing: ${typeof this}`);
    }

    // setOwnData(thingData)
    // {
    //     this.rdata = thingData;

    //     return this;
    // }

    // getOwnData()
    // {
    //     return this.rdata;
    // }

    setThingIdx(idx)
    {
        this.thingIdx = idx;

        return this;
    }

    getThingIdx()
    {
        return this.thingIdx;
    }
}

{
    const descriptors = Object.getOwnPropertyDescriptors(ThingDataHelper);
    for (const elem in descriptors)
    {
        descriptors[elem].enumerable = false;
    }
            
    // // Remove the constructor from the mixin so we don't overwrite the base class one
    delete descriptors.constructor;
    Object.defineProperties(Thing.prototype, descriptors);
    // Object.assign(Thing.prototype, ThingDataHelper);
}

export default Thing;

/*
thing.setInteractive({cursor: 'url("/assets/cursors/cover3.cur"), pointer', pixelPerfect: true})
                .setVisible(false)
                .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, thing.scene.onThingDown)
                .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OVER, thing.scene.onThingOver)
                .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OUT, thing.scene.onThingOut)
                .rdata = null;

                thing.isThing = true;
                thing.isTriggerArea = false;
                thing.scene.cameras.cameras[1].ignore(thing);
*/