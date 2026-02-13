export default class RotationHelper
{
    static cardinals;
    static ARC = Math.PI / 4;
    static _isDestroyed = false;
    static {
        this.cardinals = new Map( [
        [2.356194490192345, "SW"],
        [1.5707963267948966, "S"],
        [0.7853981633974483, "SE"],
        [0, "E"],
        [-0.7853981633974483, "NE"],
        [-1.5707963267948966, "N"],
        [-2.356194490192345, "NW"],
        [-3.141592653589793, "W"],
        [3.141592653589793, "W"]
        ]);
        console.log("cardinals", this.cardinals);
    }

    static getRelativeCardinal({x: ax, y: ay}, {x: vecX, y: vecY})
    {
        return Phaser.Math.Snap.To(Phaser.Math.Angle.Between(ax, ay, vecX, vecY), this.ARC);
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