class CrossDisciplinary():
    def _iu_message(self):
        print("This is from CrossDisciplinary class!")
    @staticmethod
    def integer_to_binary(x = 0, prepend_zeroes = True):
        resulting_string = f'{x:0>8b}' if prepend_zeroes else f'{x:b}'
        print(resulting_string)
        return resulting_string
    @staticmethod
    def _gather_vcoords(kind, index):
        if kind > 3:
            raise ValueError(f"kind ({kind}) is too big!")
        return (index << 2) | kind
    @staticmethod
    def _disassemble_vcoords(vcoord):
        return [vcoord & 3, vcoord >> 2]
    @classmethod
    def manage_array(cls, ary):
        l = len(ary)
        if l == 1:
            return ary[0]
        vcoords = CrossDisciplinary._gather_vcoords(ary[0], ary[1])
        if l == 2:
            return vcoords
        elif l == 3:
            return [vcoords, ary[2]]
        else:
            raise ValueError(f"Array length ({l}) out of range!")
        
