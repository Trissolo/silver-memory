export default class TriggerZone extends Phaser.GameObjects.Zone
{
    isThing = true;
    isTriggerArea = true;
    rdata = null;
    thingIdx = null
    isOccupied = false;


    constructor(scene, x, y)
    {
        super(scene, 0, 0);
        this
            .setActive(true)
            .setOrigin(0, 0)
            .setDepth(1)
            .setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'})
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, this.scene.onThingDown)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OVER, this.scene.onThingOver)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OUT, this.scene.onThingOut)
            .setSize(0, 0)
            .addToDisplayList();

        this.scene.cameras.cameras[1].ignore(this);
    }


    setOwnData(thingData)
    {
        this.rdata = thingData;
        
        return this;
    }

    getOwnData()
    {
        return this.rdata;
    }

    setThingIdx(idx)
    {
        this.thingIdx = idx;

        return this;
    }

    getThingIdx()
    {
        return this.thingIdx;
    }

    getHitArea()
    {
        return this.input.hitArea;
    }

    containsVector(vector)
    {
        return this.getHitArea().contains(vector.x, vector.y);
    }
}
