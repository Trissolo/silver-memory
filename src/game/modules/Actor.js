import RotationHelper from "./actorStuff/rotationHelper";

export default class Actor extends Phaser.GameObjects.Sprite
{
    costume;
    id;
    inventory;
    _rotAnim;
    cardStringToFrame = new Map();
    rotateBeforeWalk = false;
    rotationInProgress = false;

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

        this.enableRotation();
    }

    preUpdate(time, delta)
    {
        super.preUpdate(time, delta);
    }
    destroy()
    {
        this.disableRotation();
        this._rotAnim = this.cardStringToFrame = undefined;
        super.destroy();
    }

    setIdle()
    {
        this.anims.stop();
        return this;
    }

    hide()
    {
        return this
        .setIdle()
        .setActive(false)
        .setVisible(false)
    }

    show()
    {
        return this
        //.setIdle()
        .setActive(true)
        .setVisible(true)
    }

    enableRotation()
    {
        // quick access to the rotation anim
        this._rotAnim = this.scene.anims.anims.get(`${this.costume}_rotate`);

        // easily obtainable animation frames
        for (const frame of this._rotAnim.frames)
        {
            this.cardStringToFrame.set(frame.textureFrame.split("_")[2], frame);
        }

        // Event that fires when _rotAnim has reached its end. Used to enable walking
        this.on(Phaser.Animations.Events.ANIMATION_STOP, e => e); //console.log("Animation stopped"));

        // A 'switch' that indicates whether pre-walk rotation is active
        this.rotateBeforeWalk = true;
    }

    disableRotation()
    {
        this.cardStringToFrame.clear();
        this._rotAnim = null;
        this.off(Phaser.Animations.Events.ANIMATION_STOP);
        this.rotateBeforeWalk = false;
    }

    relativeAngle(vec)
    {
        return RotationHelper.getRelativeCardinal(this, vec);
    }

    rotateToVec(vec)
    {
        // Target Angle
        const targetInRadians = this.relativeAngle(vec);

        // Target Acronym
        const targetAcronym = RotationHelper.getAcronym(targetInRadians); //RotationHelper.angleToCardinalAcronym.get(targetInRadians);

        // Start Acronym
        const startAcronym = this.frame.name.split("_")[2];
        
        // Start Angle
        const startAngle = RotationHelper.getAngle(startAcronym);//RotationHelper.cardinalAcronymToAngle.get(startAcronym);
        // console.log(`🍒 🍐`);

        // Distance
        const gap = Phaser.Math.Angle.GetShortestDistance(startAngle, targetInRadians);

        // Skip if too close
        if (Math.abs(gap) < 1) //.5707963267948966)
        {
            // console.log("No rotation needed.");
            // In standard condition we must return now.
            // Changing frame just for fun...
            this.setFrame(`${this.costume}_walk_${targetAcronym}_0`);
            return;
        }

        // rot direction
        // const clockwise = gap >= 0;
        
        const realFrame = this.cardStringToFrame.get(targetAcronym);

        const fromFrame = this.cardStringToFrame.get(startAcronym).index - 1;

        (gap >= 0) ? this.play({key: `${this.costume}_rotate`, startFrame: fromFrame}): this.playReverse({key: `${this.costume}_rotate`, startFrame: fromFrame})
        this.stopOnFrame(realFrame);
    }

}