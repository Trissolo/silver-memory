import hovernames from '../gamedata/hovernames.json';

export default class ThingNameLabelManager
{  
    scene;
    timeEvent;
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
        
        this.timeEvent = scene.time.addEvent({ paused: true, delay: 60, callback: this.updLabelPosition, callbackScope: this, loop: true });

        this.labelTexture = scene.textures.addDynamicTexture('dynat', 200, 20);

        this.label = scene.add.image(0, 0, 'dynat').setOrigin(0).setVisible(false).setDepth(1e9);
    }

    clear()
    {
        this.lastThing = null;

        this.timeEvent.paused = true;

        return this;
    }

    manageOveredThing(thing)
    {
        console.log("ThingNameLabelManager is managing thing");
        if (this.lastThing !== thing.state)
        {
            console.log("New label needed: calculating it");
            this.drawText(thing);
        }
        else
        {
            console.log("Recycling label");

            this.label.setVisible(true);
            
            this.timeEvent.paused = false;
        }
    }

    // setThingLabel(thing)
    // {
    //     if (this.lastThing !== thing.state)
    //     {
    //         this.drawText(thing);
    //     }      
    // }

    drawText(thing)
    {
        this.lastThing = thing.state;

        const {bitmapText, labelTexture, fakeRect} = this;
        
        thing.isTriggerArea?  bitmapText.setTintFill(0xdada67) : bitmapText.clearTint();

        const {local: {width, height}} = bitmapText.setText(hovernames[thing.rdata.hoverName]).getTextBounds();

        const {border} = this;

        fakeRect.setSize(width + border + border, height + border + border);

        labelTexture
            .clear()
            .fill(0x5656a6, 1, 0, 0, fakeRect.width, fakeRect.height)
            .draw(bitmapText, border, border, 1);
        

        this.setLabelPosition();

        this.label.setVisible(true);

        this.timeEvent.paused = false;
    }

    setLabelPosition()
    {
        const {worldX: x, worldY: y} = this.scene.input.activePointer;

        const nx = Phaser.Math.Clamp(x - (this.fakeRect.width >> 1), this.camBounds.x, this.camBounds.right - this.fakeRect.width);
        const ny = Phaser.Math.Clamp(y + this.border, 0, this.camBounds.bottom - this.fakeRect.height);

        this.label.setPosition(nx, ny);

        //this.label.setPosition(x - (this.fakeRect.width >> 1), y + this.border);
    }

    updLabelPosition()
    {
        if(this.label.visible)
        {
            this.setLabelPosition();
        }
        else
        {
            console.log("Stopping label timer");
            this.timeEvent.paused = true;
        }
    }

    destroy()
    {

    }
}