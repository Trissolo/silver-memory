export default class rs3
{
    // uo
    static 0(ta, actor, boolInside)
    {
        console.log(ta);
        this.toAnotherRoom(ta, 4, 220, 120, "W", 0);
    }
    
    // ue
    static 1(ta, actor, boolInside)
    {
        console.log(ta);
        this.toAnotherRoom(ta, 2, 20, this.input.activePointer.worldY, "E", 0);
    }
    
    // us
    static 2(ta, actor, boolInside)
    {
        console.log(ta);
    }
}
