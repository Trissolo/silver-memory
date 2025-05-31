from ..gamedata.GamedataGatherer import GamedataGatherer

class TrisData():
    dict_datasize = GamedataGatherer.props_datasize
    def add_data(self, property):
        self.length = type(self).dict_datasize[property]
        self.final = [None] * self.length
        self.proposed = self.final.copy()
    
    def proposal_accepted(self):
        type(self).set_from_array(self.proposed, self.final)
        
    def proposal_rejected(self):
        type(self).set_from_array(self.final, self.proposed)
    
    def clear_proposed(self):
        for idx in range(self.length):
            self.proposed[idx] = None
    
    def reset_final(self):
        return self._reset_ary(self.final)
    
    def reset_proposed(self):
        return self._reset_ary(self.proposed)
    
    def _reset_ary(self, ary):
        for idx in range(self.length):
            ary[idx] = None
            return self
    
    def info(self):
        print(f"{self.final=}")
        print(f"{self.proposed=}")
      
    @staticmethod
    def set_from_array(source, target):
        target.clear()
        target.extend(source)
    
    def absorb_parasite(self, parasite):
        data = type(self).para_data_to_ary(parasite.get_data())
        self.set_from_array(data, self.final)
    
    @staticmethod
    def ary_to_bytes(data):
        '''Encode an array of any integer in a <bytes array> '''
        return (" ".join([str(el) for el in data])).encode('ascii')

    @staticmethod
    def para_data_to_ary(data):
        '''Convert a <bytes array> to a compact int array'''
        bytes_as_string = str(object=bytes(data), encoding='ascii')
        return [int(x) for x in bytes_as_string.split(" ")]