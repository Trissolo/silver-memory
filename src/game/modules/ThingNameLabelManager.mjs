import hovernames from '../gamedata/hovernames.json';

export default class ThingNameLabelManager
{  
    scene;
    fakeRect = new Phaser.Geom.Rectangle();
    labelTexture;
    bitmapText;
    label;
    lastThing = null;
    hovernames = hovernames;
    camBounds = new Phaser.Geom.Rectangle();
    border = 3;

    constructor(scene)
    {
        this.scene = scene;
        this.bitmapText = scene.make.bitmapText({font: 'font0'}, false)
            .setPosition(0, 0)
            //.tintFill(true)
            .setOrigin(0); 
        
        this.labelTexture = scene.textures.addDynamicTexture('dynat', 80, 12);

        this.label = scene.add.image(0, 0, 'dynat').setOrigin(0).setVisible(false).setDepth(1e9);

        scene.cameras.cameras[1].ignore(this.label);
    }

    clear()
    {
        this.lastThing = null;

        this.label.setVisible(false);

        return this;
    }

    manageOveredThing(thing, pointer, relX, relY)
    {
        if (this.lastThing !== thing.thingIdx)
        {
            this.drawText(thing, pointer);
        }
        else
        {
            // console.log("Recycling label");

            this.label.setVisible(true);
        }
    }

    // setThingLabel(thing)
    // {
    //     if (this.lastThing !== thing.state)
    //     {
    //         this.drawText(thing);
    //     }      
    // }

    drawText(thing, pointer, relX, relY)
    {
        this.lastThing = thing.thingIdx;

        const {bitmapText, labelTexture, fakeRect} = this;
        
        // thing.isTriggerArea?  bitmapText.setTintFill(0xdada67) : bitmapText.clearTint();

        const {local: {width, height}} = bitmapText.setText(hovernames[thing.rdata.hoverName]).getTextBounds();

        const {border} = this;

        fakeRect.setSize(width + border + border, height + border + border);

        labelTexture
            .clear()
            .fill(0x5656a6, 1, 0, 0, fakeRect.width, fakeRect.height)
            .draw(bitmapText, border, border, 1);
        

        this.setLabelPosition(pointer);

        this.label.setVisible(true);
    }

    setLabelPosition(pointer, rx, ry)
    {
        const {worldX: x, worldY: y} = pointer;

        const nx = Phaser.Math.Clamp(x - (this.fakeRect.width >> 1), this.camBounds.x, this.camBounds.right - this.fakeRect.width);
        const ny = Phaser.Math.Clamp(y + this.border, 0, this.camBounds.bottom - this.fakeRect.height);

        this.label.setPosition(nx, ny);
    }

    hideLabel()
    {
        this.label.setVisible(false);
    }

    destroy()
    {

    }
}
