/**
 * @mixin
 */

const ThingDataHelper = {
    setOwnData(thingData)
        {
            this.rdata = thingData;

            return this;
        },

        getOwnData()
        {
            return this.rdata;
        },

        dataSuffix()
        {
            const temp = this.getOwnData()?.suffix;

            console.log(`(ThingDataHelper) Suffix: ${temp}`);

            return temp;
        },
        
        dataFrame()
        {
            return this.getOwnData()?.frame;
        },

        dataHoverName()
        {
            return this.getOwnData()?.hoverName;
        },

        dataKind()
        {
            return this.getOwnData()?.kind;
        }
}

export default ThingDataHelper;
