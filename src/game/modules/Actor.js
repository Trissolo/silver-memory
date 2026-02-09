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
        .addToDisplayList();
        this.costume = costume;
        this.id = id;
    }

    preUpdate(time, delta)
    {
        super.preUpdate(time, delta)
    }
    destroy()
    {
        super.destroy();
    }
}