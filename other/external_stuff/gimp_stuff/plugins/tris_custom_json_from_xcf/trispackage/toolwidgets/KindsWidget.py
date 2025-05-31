from ..mixins.BaseWidget import BaseWidget

class KindsWidget(BaseWidget):
    def __init__(self, prop):
        super().__init__()
        self.prop = prop
        self.make_left_gui(prop)
        self.label_a.write(bgcolor=0x565698, width=20)
        self.label_b.write(width=20, monospace=True)