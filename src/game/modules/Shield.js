export default class Shield extends Phaser.GameObjects.Image
{
  constructor(scene)
  {
    super(scene, 0, 0, 'atlas0', 'pixelB');

    this
        .setScale(scene.cameras.main.width, scene.cameras.main.height)
        .setAlpha(0.5)
        .setDepth(Number.MAX_SAFE_INTEGER)
        .setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'})
        .setScrollFactor(0)
        .on("pointerdown", this.clicked)
        .setOrigin(0)
        .addToDisplayList();
  }

  raise()
  {
    this.setInteractive()
        .setActive(true)
        .setVisible(true);
        // .scene.igEvents.emit(ShieldEvents.RAISE, this.scene)
        //.emit(ShieldEvents.RAISE, this)
  }

  lower()
  {
    this.disableInteractive()
        .setActive(false)
        .setVisible(false);
        //.emit(ShieldEvents.LOWER, this)
  }

  clicked(pointer, sx, sy, stopProp)
  {
    console.log("Shield clicked!");
    stopProp.stopPropagation();
  }
}
