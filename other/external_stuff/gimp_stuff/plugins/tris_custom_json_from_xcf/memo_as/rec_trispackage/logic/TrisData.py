# import gi
# gi.require_version("Gimp", "3.0")
# from gi.repository.Gimp import Parasite as GimpPara
from .LayerManager import LayerManager

class TrisData(LayerManager):
    def __init__(self, length, image):
        super().__init__(image=image)
        self.length = length
        self.final = [None] * length
        self.proposed = self.final.copy()
    
    def __getitem__(self, index):
        return self.proposed[index]
        
    def __setitem__(self, index, newvalue):
        self.proposed[index] = newvalue
    
    def __len__(self):
        return len(self.proposed)
        
    def proposal_accepted(self):
        type(self).set_from_array(self.proposed, self.final)
        
    def proposal_rejected(self):
        type(self).set_from_array(self.final, self.proposed)
    
    def clear_proposed(self):
        for idx in range(self.length):
            self[idx] = None
    
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

    # @classmethod
    # def SingleValue(cls):
    #     return cls(1, None)
    
    # @classmethod
    # def VariableKind(cls):
    #     return cls(2, None)
    
    # @classmethod
    # def Condition(cls):
    #     return cls(3, None)