const testdata = require('../gamedata/bool.json');
console.log(testdata);

import { Scene } from 'phaser';

export class Game extends Scene
{
    constructor ()
    {
        super('Game');
    }

    create ()
    {
        this.cameras.main.setBackgroundColor(0x00ff00);

       /*
        this.add.text(512, 384, `Make something fun!\nand share it with us:\nsupport@phaser.io\n${testdata.join("\n")}`, {
            fontFamily: 'Arial Black', fontSize: 38, color: '#ffffff',
            stroke: '#000000', strokeThickness: 8,
            align: 'center'
        }).setOrigin(0.5);*/

        let roomdata = this.cache.json.get('roomdata')
        //console.log("ROOMDATA", roomdata)
        let curr = roomdata[0]
        //console.log("CURR:", curr, curr.frame + "1")
        //console.log(this.textures)
        for (let curr of roomdata)
        {
            if (curr.kind ===1)
            {
                continue
            }
            console.log(curr)
            let immy = this.add.image(curr.x, curr.y, "atlas0", curr.frame + (curr.suffix? "1": "")+".png")
            immy.setDepth(curr.kind);
            if (curr.kind === 4)
            {
                console.log("Depth Sorted")
                immy.setOrigin(0.5, 1);
            }
            else
            {
                immy.setOrigin(0);
            }


        }

        this.input.once('pointerdown', () => {

            this.scene.start('GameOver');

        });
    }
}
