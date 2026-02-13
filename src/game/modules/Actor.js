import RotationHelper from "./actorStuff/rotationHelper";

export default class Actor extends Phaser.GameObjects.Sprite
{
    costume;
    id;
    inventory;
    _rotAnim;
    _framesByAcronym = new Map();
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
        this._rotAnim = this._framesByAcronym = undefined;
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
            this._framesByAcronym.set(frame.textureFrame.split("_")[2], frame);
        }

        // Event that fires when _rotAnim has reached its end. Used to enable walking
        this.on(Phaser.Animations.Events.ANIMATION_STOP, e => console.log("Animation stopped"));

        // A 'switch' that indicates whether pre-walk rotation is active
        this.rotateBeforeWalk = true;
    }

    disableRotation()
    {
        this._framesByAcronym.clear();
        this._rotAnim = null;
        this.off(Phaser.Animations.Events.ANIMATION_STOP);
        this.rotateBeforeWalk = false;
    }

    relativeAngle(vec)
    {
        return RotationHelper.getRelativeCardinal(this, vec);
        // const dirInRadians = RotationHelper.getRelativeCardinal(this, vec);
        // console.log(`(relativeAngle method): ${RotationHelper.cardinals.get(dirInRadians)} (${dirInRadians})`);
        // return dirInRadians;
    }

    rotateToVec(vec)
    {
        // Target Angle
        const targetInRadians = this.relativeAngle(vec);

        // Target Acronym
        const targetAcronym = RotationHelper.cardinals.get(targetInRadians);

        // Start Acronym
        const startAcronym = this.frame.name.split("_")[2]
        
        // Start Angle 
        let currfacing = null;
        for (const [r, stDir] of RotationHelper.cardinals)
        {
            if (stDir === startAcronym)
            {
                currfacing = r;
                break;
            }
        }
        
        // console.log(`🍐 Data so far:\nStart Angle: ${currfacing}\nStart Acronym: ${startAcronym}\nTarget Angle: ${targetInRadians}\nTarget Acronym: ${targetAcronym}`)

        // Distance
        const gap = Phaser.Math.Angle.GetShortestDistance(currfacing, targetInRadians);

        // Skip if too close
        if (Math.abs(gap) < 1) //.5707963267948966)
        {
            console.log("No rotation needed.");
            // In standard condition we must return now.
            // Changing frame just for fun...
            this.setFrame(`${this.costume}_walk_${targetAcronym}_0`);
            return;
        }

        // rot direction
        const clockwise = gap >= 0;

        
        let realFrame = this._framesByAcronym.get(targetAcronym);
        let fromFrame = this._framesByAcronym.get(startAcronym).index - 1;

        console.log("Start From idx:", fromFrame, "REALFRAME name LAST", realFrame.textureFrame);
        
        clockwise ? this.play({key: `${this.costume}_rotate`, startFrame: fromFrame}): this.playReverse({key: `${this.costume}_rotate`, startFrame: fromFrame})
        this.stopOnFrame(realFrame);
    }

    calcRotation(from, to)
    {
        const {cardinals} = RotationHelper;
        let gap = Phaser.Math.Angle.GetShortestDistance(from, to);
        const clockwise = gap >= 0;
        console.log(`\nFrom: ${cardinals.get(from)} to ${cardinals.get(to)}`);
        console.log("Maybe useless?", Math.abs(gap) < 1.5707963267948966);
        console.log(`Distance: ${gap} (in senso ${clockwise? "orario": "antiorario"})`); 
    }

    testRot()
    {
        console.log("Gen cardinals", RotationHelper)
        const dirs = [...RotationHelper.cardinals.keys()];
        for (const from of dirs)
        {
            for (const to of dirs)
            {
                this.calcRotation(from, to);
            }
        }
    }
}