from ..mixins.BaseWidget import BaseWidget
from ..mixins.TrisData import TrisData

class KindsWidget(BaseWidget, TrisData):
    def __init__(self, property):
        super().__init__()
        self.property = property
        self.make_left_gui(property)
        self.add_data(property)
        self.label_a.write(bgcolor=0x565698, width=20)
        self.label_b.write(width=20, monospace=True)