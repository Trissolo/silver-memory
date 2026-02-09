export default class RoomBackground extends Phaser.GameObjects.Image
{
  clickVector = new Phaser.Math.Vector2();
  game_basesize_width;
  game_basesize_height;
  _floorVec = Phaser.Geom.Point.Floor;

  constructor(scene)
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

        this.game_basesize_width = this.scene.scale.baseSize.width;
        this.game_basesize_height = this.scene.scale.baseSize.height;
  }
  hide()
  {
    return this.setVisible(false);  
  }
  show()
  {
    // console.log(this.input);
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

    // set Frame and/or Texture:
    this.texture.key === atlasKey? this.setFrame(frameName): this.setTexture(atlasKey, frameName);

    //set hitArea:
    const {width, height} = this.frame;
    this.input.hitArea.setSize(width, height);

    // experimental set Scroll (will change when the Player will exist)
    // console.log("Setting camera Scroll coords based on background size", "(Current camera scrollX):", this.scene.cameras.main.scrollX);
    if (width < this.game_basesize_width)
    {
      this.scene.cameras.main.setScroll( (width - this.game_basesize_width) >> 1, 0 );
    }
    else
    {
      this.scene.cameras.main.setScroll(0, 0);
    }

  }
  clickOnBg(pointer, screenX, screenY, {stopPropagation})
  {
    this._floorVec(this.clickVector.setTo(pointer.worldX, pointer.worldY));
    console.log(`Clicked BG! World coords: ${this.clickVector.x}, ${this.clickVector.y}`); //, Phaser.Math.RND);
    // console.log(`Screen coords: ${screenX}, ${screenY}, original WorldCoords:`, pointer.worldX, pointer.worldY);
    
  }
  destroy()
  {
    super.destroy();
    this._floorVec = null;
  }
}
