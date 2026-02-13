import RotationHelper from "./actorStuff/rotationHelper";

export default class Actor extends Phaser.GameObjects.Sprite
{
    costume;
    id;
    inventory;
    _rotAnim;
    _rotFrames;

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

        // TEST - delete when done!
        this._rotAnim = this.scene.anims.anims.get(`${this.costume}_rotate`);
        this._rotFrames = this._rotAnim.frames;
        console.log(this._rotFrames);
        console.log("🇮🇹 ROT", RotationHelper._isDestroyed)
    }

    preUpdate(time, delta)
    {
        super.preUpdate(time, delta);
    }
    destroy()
    {
        this._rotAnim = null;
        this._rotFrames = null;
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

    relativeAngle(vec)
    {
        const dirInRadians = RotationHelper.getRelativeCardinal(this, vec)
        console.log(`relativeAngle: ${RotationHelper.cardinals.get(dirInRadians)} (${dirInRadians})`);
        return dirInRadians;
    }

    setupRotation(vec)
    {
        const targetInRadians = this.relativeAngle(vec);
        const targetAcronym = RotationHelper.cardinals.get(targetInRadians)

        console.log(`Destination ${targetAcronym}`);
         


        const facingString = this.frame.name.split("_")[2]
        console.log("curr Frame:", this.frame.name, facingString);
        
        let currfacing = null;
        for (const [r, stDir] of RotationHelper.cardinals)
        {
            if (stDir === facingString)
            {
                currfacing = r;
                break;
            }
        }

        let fromFrame = null;


        const gap = Phaser.Math.Angle.GetShortestDistance(currfacing, targetInRadians);
        if (Math.abs(gap) < 1.5707963267948966)
        {
            console.log("No rotation needed.");
            return;
        }
        const clockwise = gap >= 0;

        // console.log("🍐 ", targetCardinalString, targetInRadians);
        let realFrame ;
        for (const [idx, frame] of this._rotFrames.entries())
        {
            console.log("...Iterating", idx, frame.textureFrame);
            if (frame.textureFrame === `${this.costume}_walk_${facingString}_0`)
            {
                fromFrame = idx;
                //realFrame = frame;
                
            }
            
            
            if (frame.textureFrame === `${this.costume}_walk_${targetAcronym}_0`)
            {
                realFrame = frame;
            }
            
        }

        console.log("REALFRAME LAST", realFrame, fromFrame);
        
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