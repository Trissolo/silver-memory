export default class RotationHelper
{
    static angleToCardinalAcronym;
    static cardinalAcronymToAngle
    static ARC = Math.PI / 4;
    static _isDestroyed = false;
    static {
        console.log("Removed hardcoded map! ;)");
        const angleToCardinalAcronym = new Map(); // [
        // [2.356194490192345, "SW"],
        // [1.5707963267948966, "S"],
        // [0.7853981633974483, "SE"],
        // [0, "E"],
        // [-0.7853981633974483, "NE"],
        // [-1.5707963267948966, "N"],
        // [-2.356194490192345, "NW"],
        // [-3.141592653589793, "W"],
        // [3.141592653589793, "W"]
        // ]);
        // console.log("angleToCardinalAcronym", this.angleToCardinalAcronym, [...this.angleToCardinalAcronym.values()]);

        // opposite:
        const cardinalAcronymToAngle = new Map();
        let angle = Math.PI;
        for (const dirString of [ "W", "SW", "S", "SE", "E", "NE", "N", "NW", "W" ])
        {
            //if (this.angleToCardinalAcronym.has(angle) && this.angleToCardinalAcronym.get(angle) === dirString)
            //{
                angleToCardinalAcronym.set(angle, dirString);
                cardinalAcronymToAngle.set(dirString, angle);
                //console.log(`Cool! ${dirString} - ${angle}`);
                angle -= this.ARC;
            //}
            //else
            //{
                // console.log("Something wrong happens...");
            //}
        }

        this.angleToCardinalAcronym = angleToCardinalAcronym;
        this.cardinalAcronymToAngle = cardinalAcronymToAngle;

        console.log(`cardinalAcronymToAngle --> ${this.cardinalAcronymToAngle.size}`);
        // for (const [a, b] of this.cardinalAcronymToAngle)
        // {
        //     console.log(a, b);
        // }

        // console.log(`this.angleToCardinalAcronym --> ${this.angleToCardinalAcronym.size}`);
        // for (const [a, b] of this.angleToCardinalAcronym)
        // {
        //     console.log(a, b);
        // }
        console.assert(angleToCardinalAcronym.has(Math.PI) && angleToCardinalAcronym.has(-Math.PI), "Due volte");

    }

    static getRelativeCardinal({x: ax, y: ay}, {x: vecX, y: vecY})
    {
        return Phaser.Math.Snap.To(Phaser.Math.Angle.Between(ax, ay, vecX, vecY), this.ARC);
    }

    static getAcronym(angle)
    {
        console.assert(this.angleToCardinalAcronym.has(angle), `Number: ${angle} not in angleToCardinalAcronym.`);
        return this.angleToCardinalAcronym.get(angle);
    }

    static getAngle(cardinalString)
    {
        console.assert(this.cardinalAcronymToAngle.has(cardinalString), `String: ${cardinalString} not in cardinalAcronymToAngle.`);
        return this.cardinalAcronymToAngle.get(cardinalString);
    }

    static destroy()
    {
        if (this._isDestroyed)
        {
            return
        }
        this.testary.length = 0;
        this.testary = null;
    }

}