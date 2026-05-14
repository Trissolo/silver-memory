import {GameObjects} from "phaser";

export default class Shield extends GameObjects.Stamp
{
  constructor(scene)
  {
    super(scene, 0, 0, 'atlasbase', 'pixelJ');

    const {width, height} =  scene.cameras.main; // this.scene.scale.baseSize;
    scene.renderedRoomLayer.add(this);

    this
      .setScale(width, height)
      .setAlpha(0.5)
      .setDepth(1e8) //Number.MAX_SAFE_INTEGER)
      .setInteractive({cursor: 'url("/assets/cursors/bubbly3.cur"), pointer'})
      .on("pointerdown", this.clicked)
      .setOrigin(0)
      //.addToDisplayList()
      .lower();


      //console.log('Scene Scale', this.scene.scale.baseSize);
      //console.log('Main camera size', this.scene.cameras.main.width, this.scene.cameras.main.height);
      
      // console.log("The 'cameraFilter' property has a value of '0' if a game object is drawn by each camera ->", this.cameraFilter);
      // this.raise();
      // this.scene.cameras.cameras[1].ignore(this);
      // console.log("However, if the second camera does not draw an object, its 'cameraFilter' property has a value of '2' ->", this.cameraFilter);
  }

  raise()
  {
    this.setInteractive()
        .setActive(true)
        .setVisible(true);
        // .scene.igEvents.emit(ShieldEvents.RAISE, this.scene)
        //.emit(ShieldEvents.RAISE, this)
        //console.log("Shield cursor:", this.input.cursor);
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
