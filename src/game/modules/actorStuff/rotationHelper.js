export default class RotationHelper
{
    static cardinalPointStrings;
    static directionAngles
    static ARC = Math.PI / 4;
    static _isDestroyed = false;
    static snapTo = Phaser.Math.Snap.To;
    static angleBetween = Phaser.Math.Angle.Between;
    static {
        const cardinalPointStrings = new Map();

        const directionAngles = new Map();

        let angle = Math.PI;

        for (const dirString of [ "W", "SW", "S", "SE", "E", "NE", "N", "NW", "W" ])
        {
                cardinalPointStrings.set(angle, dirString);

                directionAngles.set(dirString, angle);

                angle -= this.ARC;
        }

        this.cardinalPointStrings = cardinalPointStrings;

        this.directionAngles = directionAngles;


        // console.log(`directionAngles --> ${this.directionAngles.size}`);

        // console.assert(cardinalPointStrings.has(Math.PI) && cardinalPointStrings.has(-Math.PI), "Due volte");

    }

    static getRelativeCardinal({x: ax, y: ay}, {x: vecX, y: vecY})
    {
        return this.snapTo(this.angleBetween(ax, ay, vecX, vecY), this.ARC);
    }

    static _getAcronym(angle)
    {
        console.assert(this.cardinalPointStrings.has(angle), `Number: ${angle} not in cardinalPointStrings.`);

        return this.cardinalPointStrings.get(angle);
    }

    static getAngle(cardinalString)
    {
        console.assert(this.directionAngles.has(cardinalString), `String: ${cardinalString} not in directionAngles.`);

        return this.directionAngles.get(cardinalString);
    }

    static destroy()
    {
        if (this._isDestroyed)
        {
            return;
        }

        this.cardinalPointStrings = this.cardinalPointStrings.clear();
        
        this.directionAngles = this.directionAngles.clear();

        this.snapTo = undefined;

        this.angleBetween = undefined;
    }
}
