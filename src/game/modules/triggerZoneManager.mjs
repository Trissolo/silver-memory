export default class TriggerZoneManager
{
    
    scene;
    children = new Set();

    constructor(scene)
    {
        this.scene = scene;
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
            .rdata = null;

        console.log("Returning NEW TZone");
        return zone;
    }
}
