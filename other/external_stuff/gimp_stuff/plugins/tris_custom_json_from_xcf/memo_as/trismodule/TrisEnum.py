class TrisEnum:
    def __init__(self, ary, desc = "not specified"):
        assert len(ary) == len({x for x in ary}), "TrisEnum: Duplicate names in parameter List"
        tlist = []
        tdict = {}
        for idx, elem in enumerate(ary):
            tlist.append(elem)
            tdict[idx] = elem
            tdict[elem] = idx
        self.tdict = tdict
        self.tlist = tlist
        self.get = self.get_corresponding
        self.desc = desc
    def get_list(self):
        return self.tlist
    def get_corresponding(self, param):
        if not self.has(param):
            raise KeyError(f'Element NOT present in TrisEnum: {param}') 
        return self.tdict[param]
    def get_all(self, param):
        value = self.get_corresponding(param)
        return (value, self.tdict[value]) if type(value) is int else (self.tdict[value], value)
    def has(self, param):
            return param in self.tdict
    def get_length(self):
        #return len(self.tdict) >> 1
        return len(self.tlist)
    def __repr__(self):
        l = self.get_length()
        a = f"TrisEnum for: {self.desc}, lenght: {l}.\n"
        if l > 0:
            a += f"Elem[0]: '{self.tlist[0]}', elem[1]: '{self.tlist[1]}', elem[last]: '{self.tlist[-1]}'\n"
        return a
    