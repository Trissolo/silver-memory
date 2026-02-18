export default function* SnappedCoord(val)
{
    yield Math.floor(val);
    yield Math.ceil(val);
}
