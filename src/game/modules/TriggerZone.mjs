export default class TriggerZone extends Phaser.GameObjects.Zone
{
    isThing = true;
    isTriggerArea = true;
    hasPolygon = false;
    rdata = null;
    thingIdx = null
    isOccupied = false;


    constructor(scene, polyParams)
    {
        super(scene, 0, 0);
        
        if (polyParams)
        {
            this.hasPolygon = true;
            this.setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer', hitArea: new Phaser.Geom.Polygon(polyParams), hitAreaCallback: Phaser.Geom.Polygon.Contains})
        }
        else
        {        
            this.setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'});
        }

        this
            .setActive(true)
            .setOrigin(0, 0)
            .setDepth(1)
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
