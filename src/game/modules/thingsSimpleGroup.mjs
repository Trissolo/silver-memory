import Thing from "./ThingClass.mjs";


export default class ThingSimpleGroup
{
    
    scene;

    children = new Set();

    constructor(scene)
    {
        this.scene = scene;
    }

    get(x, y)
    {
        const {children} = this;

        for (const thing of children)
        {
            if (!thing.active)
            {
                return thing.setPosition(x, y);
            }
        }

        const thing = new Thing(this.scene, x, y);

        children.add(thing);

        return thing;
    }

}
