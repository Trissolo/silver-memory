export default class Shield extends Phaser.GameObjects.Image
{
  constructor(scene)
  {
    super(scene, 0, 0, 'atlasbase', 'pixelA');

    this
        .setScale(scene.cameras.main.width, scene.cameras.main.height)
        .setAlpha(0.5)
        .setDepth(1e8) //Number.MAX_SAFE_INTEGER)
        .setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'})
        .setScrollFactor(0)
        .on("pointerdown", this.clicked)
        .setOrigin(0)
        .addToDisplayList()
        .lower();
  }

  raise()
  {
    this.setInteractive()
        .setActive(true)
        .setVisible(true);
        // .scene.igEvents.emit(ShieldEvents.RAISE, this.scene)
        //.emit(ShieldEvents.RAISE, this)
        console.log("Shield cursor:", this.input.cursor);
        this.input.cursor =  'url("/assets/cursors/wait3.cur"), pointer'
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
