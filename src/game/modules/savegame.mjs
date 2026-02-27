export default class SaveGame
{
    currentActor = 0;
    _defaults = [{room: 0, x: 200, y: 68, facing: "SE", polygonalMap: 0, visible: true}, {room: 3, x: 135, y: 120, facing: "SE", polygonalMap: 0, visible: true}];
    locations = [];

    constructor(scene)
    {
        this.scene = scene;
        
        for (const elem of this._defaults)
        {
            this.locations.push(Object.assign({}, elem));
        }
    }

    setActor(id, gotoRoom = true)
    {
        const {scene} = this;

        if (this.scene.player.id === id)
        {
            return;
        }

        this.currentActor = id;

        // return gotoRoom? scene.drawRoom() : scene;
    }

    _setActorLocation(id, room, x, y, facing, polygonalMap, visible)
    {
        const pendingPlacement = this.locations[id];
        const actor = this.scene.actors[id];

        pendingPlacement.room = room;
        pendingPlacement.x = x === undefined? actor.x : x;
        pendingPlacement.y = y === undefined? actor.y : y;
        pendingPlacement.facing = facing === undefined? actor.frame.name.split("_")[2]: facing;
        pendingPlacement.polygonalMap = polygonalMap === undefined? actor.polygonalMap : polygonalMap;
        pendingPlacement.visible = visible === undefined? actor.visible : visible;
    }
}