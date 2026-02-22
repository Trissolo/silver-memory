export default class TriggerZoneManager
{
    
    scene;
    children = new Set();
    toBeChecked = new Map();
    timeEvent;

    constructor(scene)
    {
        this.scene = scene;
        this.timeEvent = this.scene.time.addEvent({ paused: true, delay: 500, callback: this.check, callbackScope: this, loop: true });
    }

    get()
    {
        for (const zone of this.children)
        {
            if (!zone.active)
            {
                console.log("Returning existing TZone");
                return zone;
            }
        }

        const zone = new Phaser.GameObjects.Zone(this.scene);
        zone
            .setActive(true)
            .setOrigin(0)
            .setDepth(1)
            .setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'})
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, this.scene.onThingDown)
            .addToDisplayList()
            .setSize(0, 0)
            .rdata = null;
            
        console.log("Returning NEW TZone");
        return zone;
    }

    supervise(triggerArea, effectuators, startImmediately)
    {
        console.log("supervise", triggerArea, effectuators)
        if (!Array.isArray(effectuators))
        {
            effectuators = [effectuators];
        }

        let isOccupied = false;

        for (const actor of effectuators)
        {
            if (triggerArea.input.hitArea.contains(actor.x, actor.y))
            {
                isOccupied = true;
                break;
            }
        }
                
        triggerArea.isOccupied = isOccupied;

        this.toBeChecked.set(triggerArea, effectuators);

        if (startImmediately)
        {
            return this.startChecking();
        }

        return this;
    }

    check()
    {
        console.log("Checking...", this.toBeChecked.size);
        if (this.toBeChecked.size === 0)
        {
            return;
        }
        for (const [triggerArea, actors] of this.toBeChecked.entries())
        {
            console.log("hitArea:", triggerArea.input.hitArea);
            for (const actor of actors)
            {
                const inside = triggerArea.input.hitArea.contains(actor.x, actor.y);
                console.log(inside, actor.x,actor.y)
                
                if (!triggerArea.isOccupied && inside)
                {
                    this.scene.roomscript[triggerArea.state].call(this.scene, triggerArea, actor, true);
                }
                else
                    if (triggerArea.isOccupied && !inside)
                    {
                        this.scene.roomscript[triggerArea.state].call(this.scene, triggerArea, actor, false);
                    }
            }
        }
    }

    startChecking()
    {
        this.timeEvent.paused = false;

        return this;
    }

    stopChecking()
    {
        this.timeEvent.paused = true;
        
        return this;
    }

    clearAll()
    {
        this.stopChecking();

        this.toBeChecked.clear()

        return this;
    }
}
