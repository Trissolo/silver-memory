import RotationHelper from "./actorStuff/rotationHelper";
import WalkEvents from "./actorStuff/walkEvents";
import WalkComponent from "./actorStuff/walkComponent";
export default class Actor extends Phaser.GameObjects.Sprite
{
    costume;
    id;
    inventory;
    rotationAnim;
    rotFrames = new Map();
    rotateBeforeWalk = false;
    walkAfterRotation = false;

    constructor(scene, id, costume)
    {
        super(scene, 0, 0, 'atlasbase', 'pixelA');
        this
        .setActive(false)
        .setVisible(false)
        .setOrigin(0.5, 1)
        .addToDisplayList();

        this.id = id;
        
        this.costume = costume;

        this.enableRotation();

        this.walk = new WalkComponent(this);

        // this.setWalkEventsJustWalk();
        // this.setWalkEventsFacing();
        this.setWalkEventsRotate();

        console.log("🍒", this.walkTo.toString());

        // this.timedEvent

        // console.log(`🍒 🍐`);
        // this[0] = this.updStateZero;
        // this[1] = this.updStateOne;
    }

    preUpdate(time, delta)
    {
        super.preUpdate(time, delta);

        if (this.walk.aTargetExists)
        {
            this.walk.update(time, delta);
        }

        // this[this.state]();

    }
    destroy()
    {
        this.disableRotation();

        this.removeWalkEvents();

        this.rotationAnim = this.rotFrames = undefined;

        super.destroy();

        RotationHelper.destroy();
    }

    setIdle()
    {
        this.anims.stop();

        this.walk.stopAndClear();

        return this;
    }

    hide()
    {
        return this
        .setIdle()
        .setActive(false)
        .setVisible(false);
    }

    show()
    {
        return this
        .setActive(true)
        .setVisible(true);
    }

    enableRotation()
    {
        // a reference to the rotation animation for quick access
        this.rotationAnim = this.scene.anims.anims.get(`${this.costume}_rotate`);

        // easily obtainable animation frames
        for (const frame of this.rotationAnim.frames)
        {
            this.rotFrames.set(frame.textureFrame.split("_")[2], frame);
        }

        // Event that fires when rotationAnim has reached its end. Used to enable walking
        this.on(Phaser.Animations.Events.ANIMATION_STOP, this.manageStoppedRot, this);

        // A 'switch' that indicates whether pre-walk rotation is active
        this.rotateBeforeWalk = true;
    }

    disableRotation()
    {
        this.rotFrames.clear();
        this.rotationAnim = null;
        this.off(Phaser.Animations.Events.ANIMATION_STOP);
        this.rotateBeforeWalk = false;
    }

    relativeAngle(extVec)
    {
        return RotationHelper.getRelativeCardinal(this, extVec);
    }

    getAcronymFromSnappedAngle(snappedAngle)
    {
        return RotationHelper.getAcronym(snappedAngle);
    }

    _calcRotation(vec)
    {
        // Target Angle
        const targetInRadians = this.relativeAngle(vec);

        // Target Acronym
        const targetAcronym = this.getAcronymFromSnappedAngle(targetInRadians); //RotationHelper.cardinalPointStrings.get(targetInRadians);

        // Start Acronym
        const startAcronym = this.frame.name.split("_")[2];
        
        // Start Angle
        const startAngle = RotationHelper.getAngle(startAcronym); //RotationHelper.directionAngles.get(startAcronym);

        // Distance
        const gap = Phaser.Math.Angle.GetShortestDistance(startAngle, targetInRadians);
        // console.log("☀️ GAP!", gap, startAcronym, targetAcronym, targetInRadians === startAngle);

        // Skip if too close
        if (Math.abs(gap) < 1) //.5707963267948966)
        {
            //console.log("You asked to play the RotationAnimation, ☀️ but ☀️ no rotation is needed anymore.");
            console.log("☀️ No need to play the Animation. walkAfterRotation:", this.walkAfterRotation)
            return this.manageStoppedRot();
            // Changing frame just for fun...
            //this.setFrame(`${this.costume}_walk_${targetAcronym}_0`);
        }

        // determine the direction of rotation
        // const clockwise = gap >= 0;
        
        const realFrame = this.rotFrames.get(targetAcronym);

        const fromFrame = this.rotFrames.get(startAcronym).index - 1;

        (gap >= 0) ? this.play({key: this.rotationAnim.key, startFrame: fromFrame})
                : this.playReverse({key: this.rotationAnim.key, startFrame: fromFrame})
        
        // 'stopOnFrame' must be called *after* the animation has started playing!
        this.stopOnFrame(realFrame);
    }

    manageStoppedRot(animation, frame, gameObject, frameKey)
    {
        console.log(`Rotation Stopped. walkAfterRotation is ${this.walkAfterRotation}`);
        if (this.rotateBeforeWalk && this.walkAfterRotation)
        {
            this.walkAfterRotation = false;

            this.playFacingAndStartWalk(null, null, this.walk.endCoords);
        }
    }

    removeWalkEvents()
    {
        for (const walkEventName of Object.values(WalkEvents))
        {
            this.off(walkEventName);
        }

        return this;
    }

    setWalkEventsJustWalk()
    {
        this
            .removeWalkEvents()
            .on(WalkEvents.WALK_START, this.startWalking, this)
            .on(WalkEvents.WALK_SUBSTART, this.startWalking, this)
            .on(WalkEvents.WALK_COMPLETE, this.setIdle, this);
    }

    setWalkEventsFacing()
    {
        this
            .removeWalkEvents()
            .on(WalkEvents.WALK_START, this.playFacingAndStartWalk, this)
            .on(WalkEvents.WALK_SUBSTART, this.playFacingAndStartWalk, this)
            .on(WalkEvents.WALK_COMPLETE, this.setIdle, this);
    }

    setWalkEventsRotate()
    {
        this
            .removeWalkEvents()
            .on(WalkEvents.WALK_START, this.rotateThenWalk, this)
            .on(WalkEvents.WALK_SUBSTART, this.playFacingAndStartWalk, this)
            .on(WalkEvents.WALK_COMPLETE, this.setIdle, this);
    }

    startWalking()
    {
        this.walk.aTargetExists = true;
    }

    walkTo(path)
    {
        if (!Array.isArray(path))
        {
            path = [path];
        }

        this.walk.setPath(path);
    }

    playFacingAndStartWalk(actor, startVec, destVec)
    {
        this.play(`${this.costume}_walk_${this.getAcronymFromSnappedAngle(this.relativeAngle(destVec))}`)
        this.startWalking();
    }

    rotateThenWalk(actor, startVec, destVec)
    {
        this.walkAfterRotation = true;
        this._calcRotation(destVec);
    }

    turnAndStayStill(destVec)
    {
        this.walkAfterRotation = false;
        this._calcRotation(destVec);
    }

    // updStateZero()
    // {
    //     console.log("0");
    // }

    // updStateOne()
    // {
    //     console.log("1");
    // }

}