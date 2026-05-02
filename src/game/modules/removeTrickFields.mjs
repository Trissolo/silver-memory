export default function (instance, mixin)
{
    console.log(`Removing those Public FIELDS that were added just to fool IntelliSense:`);
    for (const elem in mixin)
    {
        console.log(elem);
        delete instance[elem];
    }
}

// Merge the desired Mix-in into the class prototype (do this after defining the class):
// {
//     const descriptors = Object.getOwnPropertyDescriptors(moduGag);
        
//     // Remove the constructor from the mixin so we don't overwrite the base class one
//     delete descriptors.constructor;
    
//     // Define the properties on the prototype
//     Object.defineProperties(RotatingSprite.prototype, descriptors);
// }
