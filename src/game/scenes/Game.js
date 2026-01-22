//const testdata = require('../gamedata/bool.json');
//console.log(testdata,"£orcus");
import VarManager from '../modules/VarManager.js';
import { Scene } from 'phaser';
export class Game extends Scene
{
    constructor ()
    {
        super('Game');
    }

    init(data)
    {
        console.log("INIIIIT", VarManager)
        /*
        for (const elem of VarManager.varContainers.values())
        {
            console.log("EKEM:", elem.typedArray)
        }*/
       /*
       console.log("SET VALUESTOCA", VarManager.newHandleAny(0,2, 1))
       console.log("SET VALUESTOCA", VarManager.newHandleAny(0,2, 0))
       console.log("VALUESTOCA GET", VarManager.newHandleAny(0,2))
       */
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

        const curr_room_id = 1;

        const currAtlasName = `atlas${Math.floor(curr_room_id / 3) }`

        const background = this.add.image(0, 0, currAtlasName, '__DEFAULT')
        .setDepth(-5)
        .setOrigin(0)

        let roomdata = this.cache.json.get(`room${curr_room_id}`)
        console.log(`room${curr_room_id}`, roomdata, currAtlasName)
        //let curr = roomdata[0]
        //console.log("CURR:", curr, curr.frame + "1")
        //console.log(this.textures)
        for (let curr of roomdata)
        {
            if (curr.kind === 1)
            {
                continue
            }

            if (curr.kind === -5)
            {
                background.setTexture(currAtlasName, `${curr.frame}${curr_room_id}`)
                continue
            }
            //console.dir(curr)
            const debuFrame = curr.frame? curr.frame: "(No frame)"
            console.log("FRAME", debuFrame)
            let immy = this.add.image(curr.x, curr.y, currAtlasName, `${curr.frame}${curr.suffix? this.getVarFromArray(curr.suffix): ""}`);
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

        //VarManager.newHandleAny(0,2,null,true)
        const hardcoded_test = VarManager.varContainers.get(0).typedArray
        hardcoded_test[0] = hardcoded_test[0]===255?0:255
        //console.log("VarM", VarManager.varContainers.get(0).typedArray)


        this.input.once('pointerdown', () => {

            this.scene.restart() //start('GameOver');

        });

        console.log(this.textures)
        //this.add.image(60,300, "atlas0", "ITcardA")//"porta1")
    }

    getVarFromArray(ary)
    {
        return VarManager.newHandleAny(ary[0], ary[1])
    }
}
