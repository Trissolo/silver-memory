import ThingDataHelper from "./mixins/thingDataHelper.mjs";
import {GameObjects, Input, Geom} from "phaser";
const {GAMEOBJECT_POINTER_DOWN, GAMEOBJECT_POINTER_OVER, GAMEOBJECT_POINTER_OUT, GAMEOBJECT_POINTER_MOVE} = Input.Events;

class TriggerZone extends GameObjects.Zone
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
            
            this.setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer', hitArea: new Geom.Polygon(polyParams), hitAreaCallback: Geom.Polygon.Contains})
        }
        else
        {        
            this.setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'});
        }

        this
            .setActive(true)
            .setOrigin(0, 0)
            .setDepth(1)
            .on(GAMEOBJECT_POINTER_DOWN, this.scene.onThingDown)
            .on(GAMEOBJECT_POINTER_OVER, this.scene.onThingOver)
            .on(GAMEOBJECT_POINTER_OUT, this.scene.labelManager.hideLabel, this.scene.labelManager)
            .on(GAMEOBJECT_POINTER_MOVE, this.scene.labelManager.setLabelPosition, this.scene.labelManager)
            .setSize(0, 0)
            // .addToDisplayList();

        // this.scene.cameras.cameras[1].ignore(this);
        scene.renderedRoomLayer.add(this);
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

{
    const descriptors = Object.getOwnPropertyDescriptors(ThingDataHelper);
    for (const elem in descriptors)
    {
        descriptors[elem].enumerable = false;
    }
            
    // Remove the constructor from the mixin so we don't overwrite the base class one
    delete descriptors.constructor;

    Object.defineProperties(TriggerZone.prototype, descriptors);

    // Object.assign(TriggerZone.prototype, ThingDataHelper);
}

export default TriggerZone;
