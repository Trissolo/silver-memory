export default class DataBaseList extends Phaser.GameObjects.BitmapText
{
    listData;

    row;

    marker = 'X123456789';

    _inThrottle = true;

    constructor(scene)
    {
        super(scene, 8, 8, 'font0', '')
            .setOrigin(0)
            .setVisible(false)
            .setInteractive()
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OVER, this.onListOver)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_OUT, this.onListOut)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_MOVE, this.onListMove)
            .on(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, this.onListDown);
        
        this.addToDisplayList();

        // this.wordWrapCharCode = 160;
    }

    clearList()
    {
        this.setVisible(false);

        this.disableInteractive();

        this.row = undefined;

        this.text = '';

        this.listData = null;

        this.scene.dbsSelectionRect.setVisible(false);
    }

    setList(param)
    {
        if (param === undefined)
        {
            param = [
                'Exit',
                'Blammo 1.0',
                'ArmorAll 1.0',
                'BattleChess 2.0',
                'Hammer 2.0',
                'DoorStop 4.0',
                'Logic Bomb 5.0',
            ];
        }

        this.listData = param;

        this.charColors.length = 0;

        const {local} = this.setText(param.map(this.utilGetListElement, this)).getTextBounds();

        Phaser.Geom.Rectangle.CopyFrom(local, this.input.hitArea);

        this.input.hitArea.height -= 1;

        this.setInteractive();
        
        this.row = null;
        
        this.setVisible(true);
    }

    deriveRowIdx(locY)
    {
        return Math.floor(locY / this.fontData.lineHeight);
    }

    setSelection()
    {
        const {row} = this;

        const rowElement = this.listData[row];

        this.scene.dbsSelectionRect.y = this.y + row * this.fontData.lineHeight;

        this.charColors.length = 0;

        this.setCharacterTint(this.text.indexOf(rowElement) - row, rowElement.length, true, 0x320822);
    }

    onListOver(pointer, locX, locY, event)
    {
        const currRow = this.deriveRowIdx(locY);

        this.scene.dbsSelectionRect.setVisible(true);

        if (this.row !== currRow)
        {
            this.row = currRow;

            this.setSelection();

            // if (currRow >= 0)
            // {
            //     console.log('isNumbRow', currRow);

            //     this.setSelection();
            // }
        }

    }

    onListOut(pointer, locX, locY, event)
    {
        this.scene.dbsSelectionRect.setVisible(false);

        this.charColors.length = 0;

        this.row = undefined;
    }

    onListMove(pointer, locX, locY, event)
    {
        if (this._inThrottle = !this._inThrottle)
        {
            console.log("Skipping, but I'm not sure if it's needed");

            return;
        }

        const currRow = this.deriveRowIdx(locY);

        if (this.row !== currRow)
        {
            this.row = currRow;

            this.setSelection();
        }
    }

    onListDown()
    {
        console.log(this.row);
        this.scene.varsSetValue(3, this.row);

        if(this.row === 0)
        {
            this.clearList();
        }
    }

    forceSelection(wantedRow)
    {
        if (this.listData && wantedRow < this.listData.length)
        {
            this.row = wantedRow;

            this.setSelection();

            this.scene.dbsSelectionRect.setVisible(true);

            this.scene.input.forceDownState(this.scene.input.activePointer, this);
        }
    }

    utilGetListElement(element, index, array)
    {
        return `${this.marker.charAt(index)}. ${element}`;
    }

    destroy()
    {
        this.off(Phaser.Input.Events.GAMEOBJECT_POINTER_OVER, this.onListOver);
        this.off(Phaser.Input.Events.GAMEOBJECT_POINTER_OUT, this.onListOut);
        this.off(Phaser.Input.Events.GAMEOBJECT_POINTER_MOVE, this.onListMove);
        this.off(Phaser.Input.Events.GAMEOBJECT_POINTER_DOWN, this.onListDown);

        this.clearList();

        super.destroy();
    }
}
