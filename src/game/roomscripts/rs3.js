const rs3 = {

    // static onRoomReady(){},
    
    // uo
    0(ta, actor, boolInside)
    {
        console.log(ta);
        this.toAnotherRoom(ta, 4, 220, 120, "W", 0);
    },
    
    // ue
    1(ta, actor, boolInside)
    {
        console.log(ta);
        this.toAnotherRoom(ta, 2, 30, 40, "E", 0);
    },
    
    // us
    2(ta, actor, boolInside)
    {
        console.log(ta, actor, boolInside);
    }
}

export default rs3;
