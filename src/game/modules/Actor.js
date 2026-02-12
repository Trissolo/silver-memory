export default class Actor extends Phaser.GameObjects.Sprite
{
    costume;
    id;
    inventory;

    constructor(scene, costume, id)
    {
        super(scene, 0, 0, 'atlasbase', 'pixelA');
        this
        .setActive(false)
        .setVisible(false)
        //.addToUpdateList()
        .addToDisplayList();
        this.setOrigin(0.5, 1);
        this.costume = costume;
        this.id = id;

        // console.log("🇮🇹 SUPER", this.scene.sys.updateList)
    }

    preUpdate(time, delta)
    {
        super.preUpdate(time, delta);
    }
    destroy()
    {
        super.destroy();
    }
}