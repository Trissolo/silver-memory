import TriggerZone from "./TriggerZone.mjs";

export default class TriggerZoneManager
{
    
    scene;
    children = new Set();
    polyChildren = new Set();
    scrutinizedOnes = new Map();
    timeEvent;

    constructor(scene)
    {
        this.scene = scene;
        this.timeEvent = this.scene.time.addEvent({ paused: true, delay: 90, callback: this.check, callbackScope: this, loop: true });
    }

    get(polyParams)
    {
        console.log("TZContainer SIZE:", this.polyChildren.size, this.children.size);
        const zoneContainer = polyParams? this.polyChildren: this.children
        for (const zone of zoneContainer)
        {
            if (!zone.active)
            {
                // console.log("Returning existing TZone");
                return zone;
            }
        }

        const zone = new TriggerZone(this.scene, polyParams);
        zoneContainer.add(zone);
        return zone;
    }

    supervise(triggerArea, effectuators, startImmediately) //, callIfIn, callIfOutside)
    {
        // console.log("supervise", triggerArea, effectuators)

        if (!Array.isArray(effectuators))
        {
            effectuators = [effectuators];
        }

        // let someoneInside;
        // let someoneOutside;

        //for (const actor of effectuators)
        //{
            this.scrutinizedOnes.set(triggerArea, [...effectuators]);

            // for now, let's assume no one is inside
            triggerArea.isOccupied = false;
        //}


        //     if (triggerArea.input.hitArea.contains(actor.x, actor.y))
        //     {
        //         someoneInside = actor;
        //     }
        //     else
        //     {
        //         someoneOutside = actor;
        //     }
        // }

        // if (someoneInside && callIfIn)
        // {
        //     this.scene.roomscript[triggerArea.state].call(this.scene, triggerArea, someoneInside, true);
        // }

        // if (someoneOutside && callIfOutside)
        // {
        //     this.scene.roomscript[triggerArea.state].call(this.scene, triggerArea, someoneOutside, false);
        // }
    
                
        // triggerArea.isOccupied = false;

        return startImmediately? this.startChecking() : this;
    }

    check()
    {
        // console.log("Checking...", this.scrutinizedOnes.size);
        if (this.scrutinizedOnes.size === 0)
        {
            return;
        }
        for (const [triggerArea, actors] of this.scrutinizedOnes.entries())
        {
            // console.log("hitArea:", triggerArea.input.hitArea);
            for (const actor of actors)
            {
                const inside = triggerArea.input.hitArea.contains(actor.x, actor.y);
                // console.log(inside, actor.x,actor.y)
                
                if (!triggerArea.isOccupied && inside)
                {
                    console.log("Just entered");

                    triggerArea.isOccupied = true;

                    return this.scene.roomscript[triggerArea.thingIdx].call(this.scene, triggerArea, actor, true);
                }
                else if (triggerArea.isOccupied && !inside)
                {
                    console.log("Gone away");

                    triggerArea.isOccupied = false;

                    this.scene.roomscript[triggerArea.thingIdx].call(this.scene, triggerArea, actor, false);
                }
            }
        }
    }

    startChecking()
    {
        this.timeEvent.paused = false;

        // console.log("TZ ckeck started");

        return this;
    }

    stopChecking()
    {
        this.timeEvent.paused = true;

        // console.log("TZ ckeck stopped");
        
        return this;
    }

    clearAll()
    {
        this.stopChecking();

        this.scrutinizedOnes.clear()

        // console.log("TZ check *CLEARED ALL*");

        return this;
    }
}
