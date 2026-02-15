export default class RoomBackground extends Phaser.GameObjects.Image
{
  clickVector = new Phaser.Math.Vector2();
  game_basesize_width;
  game_basesize_height;
  floorVecUtility = Phaser.Geom.Point.Floor;

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
    this.floorVecUtility(this.clickVector.setTo(pointer.worldX, pointer.worldY));

    console.log(`Clicked BG! World Coords: x: ${this.clickVector.x}, y: ${this.clickVector.y}`); //, Phaser.Math.RND);

    const {player} = this.scene;
    player.setIdle();
    player.clearMission().walkTo([this.clickVector]);
    

    // console.log(`Screen coords: ${screenX}, ${screenY}, original WorldCoords:`, pointer.worldX, pointer.worldY);

    // test Rotation:
    // this.scene.player.turnAndStayStill(this.clickVector);

    // Test Walk:
    // this.scene.player.walkTo([this.clickVector]);  //, new Phaser.Math.Vector2(126, 48), new Phaser.Math.Vector2(158, 66)]);

    // quick test:
    //const test_coords = new Phaser.Geom.Circle(this.game_basesize_width/2, this.game_basesize_height/2, 45).getPoints(9);
    // this.scene.player.walkTo([this.clickVector, ...test_coords]);

    // this.scene.player.walkTo([this.clickVector, new Phaser.Math.Vector2(41,20)]);
    // rotation test
    // this.benchmarkRotation();
    
  }

  destroy()
  {
    this.floorVecUtility = null;
    super.destroy();
  }

  benchmarkRotation()
  {
    const {scene} = this;
    const aryCoords = new Phaser.Geom.Circle(scene.player.x, scene.player.y - 10, 30).getPoints(68);

    Phaser.Utils.Array.Shuffle(aryCoords);

    console.log("Points coords:", aryCoords);

    const gra = scene.add.graphics().setDepth(300).fillStyle(0xadadfa, 1);
    aryCoords.forEach(v => gra.fillRect(v.x, v.y, 3, 3));
    const timedEvent = scene.time.addEvent({ delay: 1200, repeat: -1, callback: () =>  {
        const v = aryCoords.pop();
        gra.clear();
        gra.fillRect(v.x-1, v.y-1, 3, 3)
        scene.player.turnAndStayStill(v); 
            console.log(`Remaining: ${aryCoords.length}`);
            if (!aryCoords.length)
            {
                timedEvent.remove(false);
                gra.destroy();
                console.log("YEAH! BENCHDONE! ;)");
            }
        }
    });
  }

}
