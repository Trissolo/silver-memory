import { Viewport } from "../../scenes/Viewport.js";
import {Geom} from 'phaser';
class InventoryManager
{
    topGap = 4;
    

    /**
     * @param {Viewport} scene 
     */
    constructor(scene)
    {
        const [main, invCamera] = scene.cameras.cameras;
        //const orcus = scene.add.graphics().fillStyle(0xefefef, 1);
        {
            const arrowSize = 13;
            const arrowX = invCamera.width - arrowSize;
            const {height} = main;

            for (let i = 0; i < 2; i++)
            {
                const arrow = scene.add.stamp(arrowX, this.topGap + invCamera.y + arrowSize * i, 'atlasbase', 'gui_inv_arrow_d')
                .setOrigin(0)
                .setScrollFactor(0)
                //.setDepth(400000)
                //.setVisible(false)
                .setInteractive(new Geom.Rectangle(0, -height, arrowSize, arrowSize), Geom.Rectangle.Contains, false)
                .on('pointerover', this.arrowOver)
                .on('pointerout', this.arrowOut)
                .on('pointerdown', this.arrowDown);
    
                if (i)
                {
                    arrow
                    .setFlipY(true)
                    .setState(i);
                }
    
                //main.ignore(arrow);

                scene.invLayer.add(arrow);
                //orcus.fillRectShape(arrow.input.hitArea);
                console.log(`ARROW${i}`, arrow.input.hitArea);
            }

            const edge = 26
            const tempGrid = scene.add.grid(0, 0, edge * 5, edge * 3, edge, edge, 0x00b9f2)
                .setAltFillStyle(0x016fce)
                .setStrokeStyle()
                .setCellPadding(0)
                .setOrigin(0);

                scene.invLayer.add(tempGrid);
        }

        //main.ignore(orcus);
        //const {x, y, scrollX, scrollY, width, height} = invCamera;
        //const absY = invCamera.y;
        // console.log(`INV!! ${main.name}, ${invCamera.name}`);
        // console.log(x, y, scrollX, scrollY, width, height);

        // this.arrow_up = scene.add.stamp(0, absY, 'atlasbase', 'gui_inv_arrow_d').setOrigin(0);
        // this.arrow_down = scene.add.stamp(0, absY+this.arrow_up.height, 'atlasbase', 'gui_inv_arrow_d').setOrigin(0).setFlipY(true);
        //const w = scene.add.stamp(0, 0, 'atlasbase', 'item_wrench').setOrigin(0);
        // main.ignore([this.arrow_down, this.arrow_up, w]);
        // invCamera.setBackgroundColor(0x121212);
        // console.dir(`INV!!`, invCamera);
    }

    arrowOver()
    {
        this.setFrame('gui_inv_arrow_l');
    }

    arrowOut()
    {
        this.setFrame('gui_inv_arrow_d');
    }
    arrowDown()
    {
        console.log(`Arrow${this.state}`);

        const cam = this.scene.cameras.cameras[1];
        
        if (this.state === 0)
        {
            cam.scrollY = Math.max(0, cam.scrollY - 26);
        }
        else
        {
            cam.scrollY += 26;
        }
    }
}

export default InventoryManager;
