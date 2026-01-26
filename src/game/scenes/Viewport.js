//const testdata = require('../gamedata/bool.json');
// console.log(testdata,"£orcus");
import VarManager from '../modules/VarManager.js';
import { Scene } from 'phaser';
export class Viewport extends Scene
{
    constructor ()
    {
    super(
      {
        key: 'Viewport',
        active: false,
        visible: false,
        plugins: [
            'Clock',  //this.time
            //'DataManagerPlugin',  //this.data
            'InputPlugin',  //this.input
            'Loader',  //this.load
            'TweenManager',  //this.tweens
            //'LightsPlugin'  //this.lights
            ],
        cameras:
        {
            backgroundColor: "#008777" //,

            //y: 11, // 136,
            //height: 64
        }
        })
    } //end constructor

    init(data)
    {
        // console.log("INIIIIT", VarManager);
        this.debuCounter = 0;
        /*
        for (const elem of VarManager.varContainers.values())
        {
            // console.log("EKEM:", elem.typedArray)
        }*/
       /*
       // console.log("SET VALUESTOCA", VarManager.newHandleAny(0,2, 1))
       // console.log("SET VALUESTOCA", VarManager.newHandleAny(0,2, 0))
       // console.log("VALUESTOCA GET", VarManager.newHandleAny(0,2))
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

        //const curr_room_id = this.debuCounter & 1;
        this.bg = this.add.image(0, 0, 'atlas0')
        .setDepth(-5)
        .setOrigin(0)

        this.thingsGroup = this.add.group({createCallback: function (thing)
            {
                thing.setInteractive({cursor: 'url("/assets/cursors/cross.cur"), pointer', pixelPerfect: true})
            }
        })

        this.visible_things = new Set();


        // this.input.on('pointerdown', (a,b,c,d) => {console.log(a,b,c,d)})
        this.input.keyboard.on('keydown-Z', event => {

            this.disableGroupChildren(this.visible_things);
            this.drawRoom();

            const hardcoded_test = VarManager.varContainers.get(0).typedArray;
            hardcoded_test[0] = (this.debuCounter & 2)? 0: 255;
            this.debuCounter += 1;

        });
    }

    disableGroupChildren(group = this.thingsGroup)
    {
        console.log("this.visible_things:", this.visible_things)
        
        for (const thing of group)//group.children.entries)
        {
            thing.disableInteractive()
              .setActive(false)
              .setVisible(false)
              .rid = null
            //  .off('pointerover')//, thing.scene.thingOvered)
            //  .off('pointerout')//, thing.scene.thingOut)
            //  .off('pointerdown')

        }

        this.visible_things.clear();
    
    } //end disableGroupChildren

    drawRoom(curr_room_id = this.debuCounter & 1)
    {
        const currAtlasName = `atlas${Math.floor(curr_room_id / 3) }`
        
        let roomdata = this.cache.json.get(`room${curr_room_id}`)
        console.log("Roomdata", roomdata)
        this.bg.setTexture(currAtlasName, roomdata.bg)
        const palltextures = this.textures;
        for (let curr of roomdata.things)
        {
            if (curr.kind === 1)
                {
                    continue
                }
                                
            const frameuffa = `${curr.frame}${curr.suffix? this.getVarFromArray(curr.suffix): ""}`
            const immy = this.thingsGroup.get(curr.x, curr.y, currAtlasName, frameuffa, true)
            immy.setDepth(curr.kind);//.setActive(true).setVisible(true);
            immy.texture.key === currAtlasName? immy.setFrame(frameuffa): immy.setTexture(currAtlasName, frameuffa);
            immy.setActive(true);
            immy.setVisible(true)
            this.visible_things.add(immy);
            if (curr.kind === 4)
            {
                immy.setOrigin(0.5, 1);
            }
            else
            {
                immy.setOrigin(0);
            }
            /*
            if (curr.nointeraction)
            {

            }
            */
        }
    }

    getVarFromArray(ary)
    {
        return VarManager.newHandleAny(ary[0], ary[1])
    }
}
