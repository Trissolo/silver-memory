import WalkEvents from "./walkEvents";

export default class WalkComponent
{
    parent;

    //basically 'Walk isPaused'
    aTargetExists = false;

    destinations = [];

    highestIndex = 0;

    startCoords = new Phaser.Math.Vector2();

    endCoords = new Phaser.Math.Vector2();

    velocity = new Phaser.Math.Vector2();

    maxDistAllowed = 0;

    speed;

    debuVel = "";

    debuLegal = null;

    quellaDecente = new Phaser.Math.Vector2();;

    constructor(parent, speed = 60)
    {
        this.parent = parent;

        this.speed = this.calcSpeed(speed) // speed * 0.001

    } // end constructor

    // No movement/destination/velocity set. The sprite stay still/stops; any destination is cleared.
    stopAndClear()
    {
        this.aTargetExists = false;

        this.destinations.length = 0;
    }

    pause()
    {
        this.aTargetExists = false;
    }

    // /** 
    // * @method WalkComponent.setPath
    // * @param {Phaser.Types.Math.Vector2Like[]} dest -An Array of point-like objects 
    // */
    setPath(dest)
    {
        // First of all reset potential old data, and stop any movement.
        if (!dest.length)
        {
            return false;
        }
                      
        this.destinations.push(...dest);

        this.highestIndex = this.destinations.length - 1;

        this.grabTarget();

        // Debug  da rimuovere
        this.debuLegal = null;
        //this.quellaDecente.reset();
        console.log("Resetting because starting"); //, this.quellaDecente);
        // Debug  da rimuovere end

    }

    // now we have a target pool! Let's grab one!
    grabTarget()
    {
        const dest = this.destinations.pop();

        if (dest)
        {
            // ok! Setup target!
            this.startCoords.copy(this.parent);

            this.endCoords.copy(dest);

            this.maxDistAllowed = this.startCoords.distanceSq(this.endCoords);

            this.velocity
                .copy(this.endCoords)
                .subtract(this.startCoords)
                .normalize();
            
            if (this.destinations.length === this.highestIndex)
            {
                this.parent.emit(WalkEvents.WALK_START, this.parent, this.startCoords, this.endCoords);
            }
            else
            {
                this.parent.emit(WalkEvents.WALK_SUBSTART, this.parent, this.startCoords, this.endCoords);
            }

        }
        
        else
        {
            this.parent.emit(WalkEvents.WALK_STAY_IDLE, this.parent);

            this.stopAndClear();
        }
    }

    // start()
    // {
    //     this.walk.aTargetExists = true
    // }

    update(time, delta)
    {
        if (this.aTargetExists)
        {
            const vel = this.speed * delta;

            this.parent.x += this.velocity.x * vel;

            this.parent.y += this.velocity.y * vel;

            // Debug da rimuovere
            const nowIsLegal = this.parent.inAllowedPosition();
            // if (nowIsLegal)
            // {
            //     this.quellaDecente.copy(this.parent);
            // }

            if (this.debuLegal !== nowIsLegal)
            {
                console.log(nowIsLegal);
                this.debuLegal = nowIsLegal;
            }

            // const controlloVel = JSON.stringify(this.velocity);
            // if (controlloVel !== this.debuVel)
            // {
            //     console.log(controlloVel);
            //     this.debuVel = controlloVel;
            // }

            //console.log(this.velocity, this.parent.inAllowedPosition())
            // Debug da rimuovere End

            if (this.startCoords.distanceSq(this.parent) >= this.maxDistAllowed)
            // our target as been reached!
            {
                this.aTargetExists = false;

                this.parent.copyPosition(this.endCoords);

                // Debug da rimuovere
                this.quellaDecente.copy(this.endCoords);
                // Debug da rimuovere End

                if (this.destinations.length === 0)
                {
                    return this.walkFinished();
                }
                else
                {
                    this.grabTarget();
                }
            }
        }

    }

    walkFinished()
    {
        this.stopAndClear();

        this.parent.emit(WalkEvents.WALK_COMPLETE, this.parent);
    }

    destroy()
    {   
        this.aTargetExists = undefined;
        this.parent = undefined;
        this.destinations.length = 0;
        this.destinations = undefined;

        this.startCoords = undefined;
        this.endCoords = undefined;
        this.velocity = undefined;

        this.maxDistAllowed = undefined;
        this.speed = undefined;
    }

    calcSpeed(numSpeed)
    {
        return Phaser.Math.GetSpeed(numSpeed, 1);
    }

    vaiARitroso()
    {
        const internalVector = new Phaser.Math.Vector2(this.parent.x, this.parent.y);
        const lastUsedVelocity = this.velocity.clone();
        for (let i = 0; i < 30; i++)
        {
            if (this.parent.inAllowedPosition(internalVector))
            {
                console.log(`Found Decent pos andando a rotroso! ${i}`);

                this.parent.setPositionfromVector(internalVector);

                return;
            }

            internalVector.subtract(lastUsedVelocity);
        }

        console.log("MEEEERDA! Nulla! :(", this.quellaDecente);
        this.parent.setPositionfromVector(this.quellaDecente);
    }


//   setSpeed(n)
//   {
//       this.speed = this.calcSpeed(n)
//   }

}
