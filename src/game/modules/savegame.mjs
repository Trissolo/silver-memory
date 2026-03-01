export default class SaveGame
{
    currentActor = 0;
    _defaults = [{room: 0, x: 200, y: 68, facing: "SE", polygonalMapIdx: 0, visible: true}, {room: 4, x: 135, y: 120, facing: "SE", polygonalMapIdx: 0, visible: true}];
    locations = [];

    constructor(scene)
    {
        this.scene = scene;
        
        for (const elem of this._defaults)
        {
            this.locations.push(Object.assign({}, elem));
        }
    }

    setActor(id) //, gotoRoom = true)
    {
        const {scene} = this;

        if (this.scene.player.id === id)
        {
            return;
        }

        this.scene.player = this.scene.actors[id];

        // return gotoRoom? scene.drawRoom() : scene;
    }

    _setActorLocation(id, roomId, x, y, facing, polygonalMapIdx) //, visible)
    {
        console.log("Saving polymap", polygonalMapIdx)
        const pendingPlacement = this.locations[id];
        const actor = this.scene.actors[id];

        pendingPlacement.room = roomId;
        pendingPlacement.x = x ?? actor.x;
        pendingPlacement.y = y ?? actor.y;
        pendingPlacement.facing = facing ?? actor.frame.name.split("_")[2];
        pendingPlacement.polygonalMapIdx = polygonalMapIdx ?? actor.polygonalMapIdx;
        //pendingPlacement.visible = visible === undefined? actor.visible : visible;
    }
}