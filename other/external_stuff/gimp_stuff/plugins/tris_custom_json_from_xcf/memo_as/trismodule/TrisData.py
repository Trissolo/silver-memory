class TrisData():
    def __init__(self, slots):
        self._data = []
        self.slots = slots
        self.emu_number = slots == 1
        self.emu_variable = slots == 2
        self.emu_condition = slots == 3
        self.reset()
    
    @property
    def data(self):
        return self._data
    
    @property
    def slots(self):
        """Getter for the slots property."""
        return self._slots

    @slots.setter
    def slots(self, value):
        """Setter for the slots property."""
        if 0 < value < 4:
            self._slots = value
        else:
            raise ValueError("OverflowError Out Of Range Error. 'TrisData.slots' must be between 1 and 3")

    # def set_behavior(self, behavior):
    #     self.slots = behavior
    #     self.emu_number = behavior == 1
    #     self.emu_variable = behavior == 2
    #     self.emu_condition = behavior == 3
    #     return self.reset()
    
    def reset(self):
        self.set_from_array([None] * self.slots)
        return self
    
    def set_from_array(self, array):
        self.data.clear()
        self.data.extend(array)
        return self
        
    def set_at_zero(self, value):
        self.data[0] = value
        return self
    
    def set_at_one(self, value):
        assert not self.emu_number, "No slot ONE available"
        #if not self.emu_number:
        self.data[1] = value
        return self
        
    def set_at_two(self, value):
        assert self.emu_condition, "No slot TWO available"
        #if self.emu_condition:
        self.data[2] = value
        return self
    
    def get_at_zero(self):
        return self.data[0]
    
    def get_at_one(self):
        assert not self.emu_number, "No slot ONE available"
        return self.data[1] 
        
    def get_at_two(self):
        assert self.emu_condition, "No slot TWO available"
        return self.data[2]
    
    def is_valid(self):
        return not None in self.data
    
    def rawencoded(self):
        return type(self).ary_to_bytes(self.data)
    
    def absorb_parasite(self, parasite):
        data = type(self).para_data_to_ary(parasite.get_data())
        self.set_from_array(data)
    
    
    @staticmethod
    def ary_to_bytes(data):
        return (" ".join([str(el) for el in data])).encode('utf-8')

    @staticmethod
    def para_data_to_ary(data):
        res_string = str(object=bytes(data), encoding='utf-8')
        return [int(x) for x in res_string.split(" ")]

'''
def ary_to_bytes(data):
       return (" ".join([str(el) for el in data])).encode('utf-8')

def para_data_to_ary(data):
   res_string = str(object=bytes(data), encoding='utf-8')
   return [int(x) for x in res_string.split(" ")]

da_scrivere = [0, 40, 235]

pronti_da_scrivere = ary_to_bytes(da_scrivere)
b'0 40 235'

tempara = Gimp.Parasite.new("tempara", 0, pronti_da_scrivere)
<Gimp.Parasite object at 0x7ed6db9c21b0 (GimpParasite at 0x5dd80f1e6030)>

tempara.get_name()
'tempara'
tempara.get_data()
[48, 32, 52, 48, 32, 50, 51, 53]

dati_del_parassita = tempara.get_data()
[48, 32, 52, 48, 32, 50, 51, 53]

quelli_di_prima = para_data_to_ary(dati_del_parassita)
[0, 40, 235]
'''
