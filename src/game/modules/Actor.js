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

    getAcronym(snappedAngle)
    {
        return RotationHelper._getAcronym(snappedAngle);
    }

    _calcRotation(vec)
    {
        console.log("_CalcRotation receiving param:", vec, typeof vec);
        // Target Angle
        const finalAngle = typeof vec === 'object'? this.relativeAngle(vec): vec;
        console.log("FinalAngle", finalAngle, typeof finalAngle);

        // Target Acronym
        const finalAcronym = this.getAcronym(finalAngle); //RotationHelper.cardinalPointStrings.get(finalAngle);

        // Start Acronym
        const startAcronym = this.frame.name.split("_")[2];
        
        // Start Angle
        const startAngle = RotationHelper.getAngle(startAcronym); //RotationHelper.directionAngles.get(startAcronym);

        // Distance
        const gap = Phaser.Math.Angle.GetShortestDistance(startAngle, finalAngle);
        // console.log("☀️ GAP!", gap, startAcronym, finalAcronym, finalAngle === startAngle);

        // Skip if too close
        if (Math.abs(gap) < 1) //.5707963267948966)
        {
            // console.log("☀️ There is no need to play the animation, but let's pretend it was done.\nwalkAfterRotation:", this.walkAfterRotation);
            return this.manageStoppedRot();

            // Changing frame just for fun...
            //this.setFrame(`${this.costume}_walk_${finalAcronym}_0`);
        }

        // determine the direction of rotation
        // const clockwise = gap >= 0;
        
        const realFrame = this.rotFrames.get(finalAcronym);

        const fromFrame = this.rotFrames.get(startAcronym).index - 1;

        (gap >= 0) ? this.play({key: this.rotationAnim.key, startFrame: fromFrame})
                : this.playReverse({key: this.rotationAnim.key, startFrame: fromFrame})
        
        // 'stopOnFrame' must be called *after* the animation has started playing!
        this.stopOnFrame(realFrame);
    }

    manageStoppedRot(animation, frame, gameObject, frameKey)
    {
        if (this.rotateBeforeWalk && this.walkAfterRotation)
        {
            this.walkAfterRotation = false;

            this.playFacingAndWalk(null, null, this.walk.endCoords);
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
            .on(WalkEvents.WALK_START, this.playFacingAndWalk, this)
            .on(WalkEvents.WALK_SUBSTART, this.playFacingAndWalk, this)
            .on(WalkEvents.WALK_COMPLETE, this.setIdle, this);
    }

    setWalkEventsRotate()
    {
        this
            .removeWalkEvents()
            .on(WalkEvents.WALK_START, this.rotateThenWalk, this)
            .on(WalkEvents.WALK_SUBSTART, this.playFacingAndWalk, this)
            .on(WalkEvents.WALK_COMPLETE, this.setIdle, this);

            //just debugging
            // this
            // .on(WalkEvents.WALK_START, this.debugWalk, this)
            // .on(WalkEvents.WALK_SUBSTART, this.debugWalk, this)
            // .on(WalkEvents.WALK_COMPLETE, this.debugWalk, this);
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

    debugWalk()
    {
        const {walk} = this;

        console.log(`🌡️Debug Walk`); //${walk.aTargetExists}`);

        console.log(`Dest. vecs remaining: ${walk.destinations.length}`);

        console.log(`highestIndex: ${walk.highestIndex}`);

        console.log(`startCoords:`, walk.startCoords); // ${walk.startCoords}`);

        console.log(`☁️ endCoords:`, walk.endCoords); // ${walk.endCoords}`);
    }

    playFacingAndWalk(actor, startVec, destVec)
    {
        // this.play(`${this.costume}_walk_${this.getAcronym(this.relativeAngle(destVec))}`);
        this.play(`${this.costume}_walk_${this.getAcronym(this.relativeAngle(this.walk.endCoords))}`);
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
        const {directionAngles} = RotationHelper;
        // console.log("destVec:", destVec);
        // console.log("directionAngles", directionAngles.has(destVec), directionAngles.get(destVec));
        this._calcRotation(directionAngles.has(destVec)? directionAngles.get(destVec): destVec);
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