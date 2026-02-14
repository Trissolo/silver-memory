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

    _inProgress = false;

    constructor(parent, speed = 60)
    {
        this.parent = parent;

        // this.defaultSpeed = this.calcSpeed(speed)
        this.speed = this.calcSpeed(speed) // speed * 0.001

    } // end constructor

    // Idle status: no movement/destination/velocity setted. The sprite stay still/stops
    stopAndClear()
    {
        this.aTargetExists = false;

        this.destinations.length = 0;

        this._inProgress = false;
    }

    pause()
    {
        this.aTargetExists = false;
    }

    /*
    * @method WalkComponent#setPath
    * @param {point-like object[]} dest - single point-like object, or an Array of point-like objects 
    */
    setPath(dest)
    {
        // First of all reset potential old data, and stop any movement.
        this.stopAndClear();

        // add destination(s) to destinations array
        if (Array.isArray(dest))
        {
            if (!dest.length)
            {
                return false;
            }

            this.destinations.push(...dest);
        }
        else
        {
            this.destinations.push(dest);
        }

        this.highestIndex = this.destinations.length - 1;

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

            this.velocity
                .copy(this.endCoords)
                .subtract(this.startCoords)
                .normalize();
            
            // set this totally unused bool
            this._inProgress = true;
            
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

            if (this.startCoords.distanceSq(this.parent) >= this.maxDistAllowed)
            // our target as been reached!
            {
                this.aTargetExists = false;
                this.parent.x = this.endCoords.x;
                this.parent.y = this.endCoords.y;

                if (this.destinations.length === 0)
                {
                    this._inProgress = false;

                    this.parent.emit(WalkEvents.WALK_COMPLETE, this.parent);
                }
                else
                {
                    this.grabTarget();
                }

            }
        }

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


//   setSpeed(n)
//   {
//       this.speed = this.calcSpeed(n)
//   }

}
