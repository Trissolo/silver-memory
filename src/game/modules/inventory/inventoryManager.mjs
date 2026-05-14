import { Viewport } from "../../scenes/Viewport.js";
import { Geom, Math as PhaserMath, Input } from 'phaser';

class InventoryManager
{
    topGap = 4;
    iconEdge = 26;
    itemsPerRow = 3;
    itemsPerCol = 4;
    // clickGUI = new PhaserMath.Vector2();
    currItem = null;
    marker;
    arrow0;
    arrow1;
    itemGrid;
    

    /**
     * @param {Viewport} scene 
     */
    constructor(scene)
    {
        const [main, invCamera] = scene.cameras.cameras;

        {
            const arrowSize = 13;
            const arrowX = invCamera.width - arrowSize;
            const {height} = main;
            const {GAMEOBJECT_POINTER_DOWN, GAMEOBJECT_POINTER_OVER, GAMEOBJECT_POINTER_OUT} = Input.Events

            for (let i = 0; i < 2; i++)
            {
                const arrow = scene.add.stamp(arrowX, this.topGap + invCamera.y + arrowSize * i, 'atlasbase', 'gui_inv_arrow_d')
                .setOrigin(0)
                .setScrollFactor(0)
                //.setInteractive(, , false)
                .setInteractive({
                        hitArea: new Geom.Rectangle(0, -height, arrowSize, arrowSize),
                        hitAreaCallback: Geom.Rectangle.Contains,
                        cursor: 'url("/assets/cursors/cover3.cur"), pointer'
                    })
                .on(GAMEOBJECT_POINTER_OVER, this.arrowOnOver)
                .on(GAMEOBJECT_POINTER_OUT, this.arrowOnOut)
                .on(GAMEOBJECT_POINTER_DOWN, this.arrowOnClick);
    
                if (i)
                {
                    arrow
                        .setFlipY(true)
                        .setState(i);
                }
    
                scene.invLayer.add(arrow);

                this[`arrow${i}`] = arrow;
            }

            const {iconEdge, itemsPerRow, itemsPerCol} = this;

            this.itemGrid = scene.add.grid(13, 4, iconEdge * itemsPerRow, iconEdge * itemsPerCol, iconEdge, iconEdge, 0x00b9f2)
                .setAltFillStyle(0x016fce)
                .setStrokeStyle()
                .setCellPadding(0)
                .setOrigin(0)
                .setInteractive()
                .on(GAMEOBJECT_POINTER_DOWN, this.clickOnItem, this);

            this.marker = scene
                .add.image(0, 0, 'atlasbase', 'gui_selected_item')
                .setOrigin(0)
                .setVisible(false);
            
            scene.invLayer.add([this.itemGrid, this.marker]);
        }

    }

    arrowOnOver()
    {
        this.setFrame('gui_inv_arrow_l');
    }

    arrowOnOut()
    {
        this.setFrame('gui_inv_arrow_d');
    }

    arrowOnClick()
    {
        console.log(`Arrow${this.state}`);

        const cam = this.scene.cameras.cameras[1];

        const {iconEdge} = this.scene.invPlugin;
        
        if (this.state === 0)
        {
            cam.scrollY = Math.max(0, cam.scrollY - iconEdge);
        }
        else
        {
            cam.scrollY += iconEdge;
        }
    }

    clickOnItem(pointer, relX, relY, event)
    {
        const {itemsPerCol, itemsPerRow, iconEdge} = this;
        const {Floor: snapFloor} = PhaserMath.Snap;
        //console.log(snapFloor(relX, iconEdge, 0, true) + snapFloor(relY, iconEdge, 0, true) * itemsPerRow);

        const snappedX = snapFloor(relX, iconEdge, 0, true);

        const snappedY = snapFloor(relY, iconEdge, 0, true);

        console.log(`CELL: ${snappedX + snappedY * itemsPerRow}, x: ${snappedX}, y: ${snappedY}`);

        this.manageItemSelection(snappedX, snappedY);
    }

    manageItemSelection(x, y)
    {
        this.marker.setPosition(x * this.iconEdge + this.itemGrid.x, y * this.iconEdge + this.itemGrid.y).setVisible(true);
    }
}

export default InventoryManager;
