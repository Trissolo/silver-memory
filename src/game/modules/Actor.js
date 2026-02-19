import RotationHelper from "./actorStuff/rotationHelper";
import WalkEvents from "./actorStuff/walkEvents";
import WalkComponent from "./actorStuff/walkComponent";
import PMStroll from "./actorStuff/pmStroll/PMStroll.mjs";

export default class Actor extends Phaser.GameObjects.Sprite
{
    costume;
    id;
    inventory;
    polygonalMap;
    comfyDest = new Phaser.Math.Vector2();
    rotationAnim;
    pendingFunc = null;
    rotFrames = new Map();
    rotateBeforeWalkEnabled = false;
    walkAfterRotation = false;
    timedEvent;


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

        this.walk = new WalkComponent(this);

        // this.setWalkEventsJustWalk();
        // this.setWalkEventsFacing();
        this.setWalkEventsRotate();

        // console.log("🍒");

        // this.timedEvent

        // console.log(`🍒 🍐`);
        // this[0] = this.updStateZero;
        // this[1] = this.updStateOne;
    }

    preUpdate(time, delta)
    {
        

        if (this.walk.aTargetExists)
        {
            this.walk.update(time, delta);
        }

        // this[this.state]();
        super.preUpdate(time, delta);

    }
    destroy()
    {
        this.disableRotation();

        this.removeWalkEvents();

        this.rotationAnim = this.rotFrames = undefined;

        RotationHelper.destroy();

        this.walk.destroy();

        super.destroy();
    }

    setIdle()
    {
        // Stop any animation played by the Sprite
        this.anims.stop();

        this.walk.stopAndClear();

        this.setStandingFrame();

        // if (this.inAllowedPosition())
        // {
        //     return this;
        // }

        // if (!this.walk.quellaDecente.equals(Phaser.Math.Vector2.ZERO))
        // {
        //     console.log("Setting quella decente");
        //     this.setPositionfromVector(this.walk.quellaDecente);
        // }
        // else
        // {
            //console.log("The position was wrong :(\nAndando a ritroso. Calling '.walk.vaiARitroso'.")
            //this.walk.vaiARitroso();
        // }

        //PMStroll.snapIfRequired(this);

        // if (!PMStroll.permittedPosition(this, this.polygonalMap))
        // {
        //     this.emit("panic", this.polygonalMap, this.walk.startCoords, this.walk.endCoords);
        // }

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
        this.rotateBeforeWalkEnabled = true;
    }

    disableRotation()
    {
        this.rotFrames.clear();
        this.rotationAnim = null;
        this.off(Phaser.Animations.Events.ANIMATION_STOP);
        this.rotateBeforeWalkEnabled = false;
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
        // Target Angle
        const finalAngle = typeof vec === 'object'? this.relativeAngle(vec): vec;

        // Target Acronym
        const finalAcronym = this.getAcronym(finalAngle); //RotationHelper.cardinalPointStrings.get(finalAngle);

        // Start Acronym
        const startAcronym = this.frame.name.split("_")[2];
        
        // Start Angle
        const startAngle = RotationHelper.getAngle(startAcronym); //RotationHelper.directionAngles.get(startAcronym);

        // Distance
        const gap = Phaser.Math.Angle.GetShortestDistance(startAngle, finalAngle);

        // Skip if too close
        if (Math.abs(gap) < 1) //.5707963267948966)
        {
            // console.log("☀️ There is no need to play the animation, but let's pretend it was done.\nwalkAfterRotation:", this.walkAfterRotation);
            
            // Changing frame just for fun...
            //this.setFrame(`${this.costume}_walk_${finalAcronym}_0`);
            if (this.walkAfterRotation)
            {
                this.play(`${this.costume}_walk_${finalAcronym}`, true);
            }

            return this.manageStoppedRot();
        }

        // determine the direction of rotation
        // const clockwise = gap >= 0;
        
        const realFrame = this.rotFrames.get(finalAcronym);

        const fromFrame = this.rotFrames.get(startAcronym).index - 1;

        (gap >= 0) ? this.play({key: this.rotationAnim.key, startFrame: fromFrame}, true)
                : this.playReverse({key: this.rotationAnim.key, startFrame: fromFrame}, true)
        

        // Note that 'stopOnFrame' must be called *after* the animation has started playing!
        this.stopOnFrame(realFrame);

        if (this.walkAfterRotation)
        {
            this.chain(`${this.costume}_walk_${finalAcronym}`);
        }
    }

    manageStoppedRot(animation, frame, gameObject, frameKey)
    {
        if (this.rotateBeforeWalkEnabled && this.walkAfterRotation)
        {
            this.walkAfterRotation = false;

            this.startWalking();
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
            .on(WalkEvents.WALK_COMPLETE, this.walkCompleteListener, this);
    }

    setWalkEventsFacing()
    {
        this
            .removeWalkEvents()
            .on(WalkEvents.WALK_START, this.playFacingAndWalk, this)
            .on(WalkEvents.WALK_SUBSTART, this.playFacingAndWalk, this)
            .on(WalkEvents.WALK_COMPLETE, this.walkCompleteListener, this);
    }

    setWalkEventsRotate()
    {
        this
            .removeWalkEvents()
            .on(WalkEvents.WALK_START, this.rotateThenWalk, this)
            .on(WalkEvents.WALK_SUBSTART, this.playFacingAndWalk, this)
            .on(WalkEvents.WALK_COMPLETE, this.walkCompleteListener, this)
            .enableRotation();

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

    walkTo(destinationVector, y)
    {
        if (typeof y === 'number')
        {
            this.comfyDest.set(destinationVector, y);
        }
        else
        {
            this.comfyDest.copy(destinationVector);
        }

        // setIdle is called HERE in walkTo!
        this.setIdle();

        if (this.comfyDest.equals(this))
        {
            return this.walk.walkFinished();
        }

        this.walk.setPath(PMStroll.calculatePathWithTrick(this, this.comfyDest, this.polygonalMap));
    }

    debugWalk()
    {
        const {walk} = this;

        console.log(`🌡️Debug Walk`);

        console.log(`Dest. vecs remaining: ${walk.destinations.length}`);

        console.log(`highestIndex: ${walk.highestIndex}`);

        console.log(`startCoords:`, walk.startCoords);

        console.log(`☁️ endCoords:`, walk.endCoords);
    }

    playFacingAndWalk(actor, startVec, destVec)
    {
        this.play(`${this.costume}_walk_${this.getAcronym(this.relativeAngle(this.walk.endCoords))}`);   //, frameRate: 10, });

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

        this._calcRotation(directionAngles.has(destVec)? directionAngles.get(destVec): destVec);
    }

    clearMission()
    {
        this.pendingFunc = null;

        console.log("Mission cleared");

        return this;
    }

    assignMission(roomMethod)
    {
        this.pendingFunc = roomMethod;
        
        return this;
    }

    walkCompleteListener()
    {
        this.setIdle();

        if (this.pendingFunc)
        {
            this.pendingFunc.call(this.scene);
        }

        this.pendingFunc = null;
    }

    setPolygonalMapByIndex(visibilityMapIndex = 0, idx)
    {
        this.polygonalMap = idx === undefined? this.scene.roomJson.visMaps[visibilityMapIndex] : this.scene.getJson(this.scene.roomId).visMaps[visibilityMapIndex];

        return this;
    }

    // panic(pomap, stvec, endvec)
    // {
    //     console.clear();
    //     console.log("✈️ Panic!");
    //     const poly = pomap.polygons[0];
    //     if (Phaser.Geom.Polygon.Contains(poly, this.x, this.y))
    //     {
    //         console.log("NO Problem! 😅");
    //         return true;
    //     }

    //     const {x, y} = this;

    //     // stvec.setFromObject(this);

    //     // console.log(stvec);

    //     for (const potX of [Math.floor(x), Math.ceil(x)])
    //     {
    //         for (const potY of [Math.floor(y), Math.ceil(y)])
    //         {
    //             if (Phaser.Geom.Polygon.Contains(poly, potX, potY))
    //             {
    //                 this.setPosition(potX, potY);
    //                 console.log("🫡👌 FIXED!")
    //                 return true;
    //             }
    //             // endvec.setFromObject(potX, potY);
    //             // // console.log("Map", PMStroll.permittedPosition(endvec, pomap), `{ x: ${potX}, y: ${potY}}`);
    //             // console.log("Polygon", Phaser.Geom.Polygon.Contains(poly, potX, potY), `{ x: ${potX}, y: ${potY}}`);
    //         }
    //     }
    //     console.log("😈 Cannot fix :(", x, y, poly);
    //     return false
    // }

    inAllowedPosition(src = this)
    {
        return PMStroll.permittedPosition(src, this.polygonalMap);
    }

    setPositionfromVector(vector)
    {
        this.x = vector.x;
        this.y = vector.y;
    }

    setStandingFrame()
    {
        this.setFrame(`${this.costume}_walk_${this.frame.name.split("_")[2]}_0`);
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