export default function* SnappedCoord(val)
{
    console.log("Incrim VAL:", val);

    const f = Math.floor(val);

    yield f;

    for (let i = 1; i < 4; i++)
    {
        yield f + i;
        yield f - i;
    }
}

// export default function* SnappedCoord(val)
// {
//     yield Math.floor(val);
//     yield Math.ceil(val);
// }
