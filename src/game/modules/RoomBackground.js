export default class RoomBackground extends Phaser.GameObjects.Image
{
  clickVector = new Phaser.Math.Vector2();
  constructor(scene, costume, idx)
  {
    super(scene, 0, 0, 'atlasbase', 'pixelA');

    this
        .setDepth(-5)
        .setOrigin(0)
        .setName("Room background")
        .setVisible(false)
        .addToDisplayList()
        .setInteractive({cursor: 'url("/assets/cursors/cover3.cur"), pointer', hitAreaCallback: Phaser.Geom.Rectangle.Contains, hitArea: new Phaser.Geom.Rectangle(0, 0, 1, 2)}
        )
        .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, this.clickOnBg);
  }
  hide()
  {
    return this.setVisible(false);  
  }
  show()
  {
    console.log(this.input);
    return this.setVisible(true);
  }
  assignTexture(roomId)//frame, atlasKey)
  {
    console.log(`Old BG key: ${this.texture.key}`);
    if (!Number.isInteger(roomId))
    {
      roomId = this.scene.roomId;
    }
    const atlasKey = `atlas${Math.floor(roomId / 3)}`;
    const frameName = this.scene.getJson(roomId).bg;
    console.log(`NEW BG key: ${atlasKey} | frame: ${frameName}`);
    this.texture.key === atlasKey? this.setFrame(frameName): this.setTexture(atlasKey, frameName);
    const frameGO =  this.scene.textures.getFrame(atlasKey, frameName);
    console.log("BG FRAME", frameGO);
    const {width, height} = frameGO;
    this.input.hitArea.setSize(width, height);
    console.dir(this.input.hitArea);

  }
  clickOnBg(a, screenX, screenY, {stopPropagation})
  {
    console.log("Clicked BG,", a, screenX, screenY, stopPropagation);
  }
}
