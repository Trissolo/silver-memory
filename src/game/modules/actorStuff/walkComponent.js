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

    constructor(parent, speed = 60)
    {
        this.parent = parent;

        this.speed = this.calcSpeed(speed);

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
        // if no destination, nothing happens
        if (!dest.length)
        {
            return false;
        }

        // First of all reset potential old data, and stop any movement.
        this.stopAndClear();

        // Populate the queue
        this.destinations.push(...dest);

        // the index to determine the status of the walk cycle
        this.highestIndex = this.destinations.length - 1;

        // the first destination
        this.grabTarget();

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

            // this.velocity
            //     .copy(this.endCoords)
            //     .subtract(this.startCoords)
            //     .normalize();
            
            // alternative way:
            this.velocity.setToPolar(Phaser.Math.Angle.BetweenPoints(this.startCoords, this.endCoords), 1);
            
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
            // no destination, but this point will never be reached
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
            // just some info
            //          const nowIsLegal = this.parent.inAllowedPosition();
            // if (nowIsLegal)
            // {
            //     this.quellaDecente.copy(this.parent);
            // }

            // if (this.debuLegal !== nowIsLegal)
            // {
                //     console.log(nowIsLegal);
                //     this.debuLegal = nowIsLegal;
            // }


            // have we reached the goal?
            if (this.startCoords.distanceSq(this.parent) >= this.maxDistAllowed)
            {
                // Yes! Here we are!
                this.aTargetExists = false;

                this.parent.copyPosition(this.endCoords);

                if (this.destinations.length === 0)
                {
                    return this.walkFinished();
                }
                else
                {
                    // not yet. Let's grab the next target...
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

    // vaiARitroso()
    // {
    //     const internalVector = new Phaser.Math.Vector2(this.parent.x, this.parent.y);
    //     const lastUsedVelocity = this.velocity.clone();
    //     for (let i = 30; i--; /* --- */)
    //     {
    //         if (this.parent.inAllowedPosition(internalVector))
    //         {
    //             console.log(`Found Decent position going backwards! ${i}`);

    //             this.parent.setPositionfromVector(internalVector);

    //             return;
    //         }

    //         internalVector.subtract(lastUsedVelocity);
    //     }

    //     console.log("MEEEERDA! Nulla! :(");
    //     // this.parent.setPositionfromVector(this.quellaDecente);
    // }


//   setSpeed(n)
//   {
//       this.speed = this.calcSpeed(n)
//   }

}
