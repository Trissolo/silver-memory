import gi

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp

class TrisData():
    def add_data(self, length):
        self.length = length
        self.final = [None] * length
        self.proposed = self.final.copy()
    
    def proposal_accepted(self):
        type(self).set_from_array(self.proposed, self.final)
        
    def proposal_rejected(self):
        type(self).set_from_array(self.final, self.proposed)
    
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
    
    def get_prop_parasite(self):
        return self.layer.get_parasite(self.property)
    
    def remove_prop_parasite(self):
        if self.property in self.layer.get_parasite_list(): #old_parasite:
            self.layer.detach_parasite(self.property)
    
    def attach_prop_parasite(self):
        self.remove_prop_parasite()
        self.layer.attach_parasite(Gimp.Parasite.new(self.property, 1, TrisData.ary_to_bytes(self.final)))
      
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