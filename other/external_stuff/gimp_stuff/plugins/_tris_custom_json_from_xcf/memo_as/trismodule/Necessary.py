# import gi

# gi.require_version("Gimp", "3.0")
# from gi.repository import Gimp

# gi.require_version("GimpUi", "3.0")
# from gi.repository import GimpUi

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk
from .TrisData import TrisData

class Necessary():
    _ready = False
    _image = None
    _current_layer = None
    _gamedata = None
    _tool_widgets_ary = None
    _summary_widgets_ary = None
    _parasite_data_ary = None
    _layer_name = None
    _layer_x = None
    _layer_y = None
    _layer_width = None
    _layer_height = None

    @classmethod
    def setup(cls, image, gamedata):
        if not cls._ready:
            cls._ready = True
            cls._image = image
            cls._gamedata = gamedata
            cls._tool_widgets_ary = []
            cls._summary_widgets_ary = []
            cls._parasite_data_ary = []
        else:
            print("'Necessary' Class already set.")

    @classmethod
    def update_layer(cls):
        selected_layers = cls._image.get_selected_layers()
        assert type(selected_layers) is list and len(selected_layers) != 0, "No layer selected! Make sure that at least one layer exists in image!"
        cls._current_layer = selected_layers[0]

        # some_bool, ox, oy = l.get_offsets()
        # cls._layer_x = ox
        # cls._layer_y = oy
        # cls._layer_width = l.get_width()
        # cls._layer_height = l.get_height()
        # cls._layer_name = l.get_name()
        return

    @classmethod
    def get_layer_details(cls, layer=None, store_res=False):
        if layer is None:
            layer = cls._current_layer       
        _, ox, oy = layer.get_offsets()
        width = layer.get_width()
        height = layer.get_height()
        name = layer.get_name()
        if store_res:
            cls._layer_x = ox
            cls._layer_y = oy
            cls._layer_width = width
            cls._layer_height = height
            cls._layer_name = name
        return ox, oy, width, height, name
    
    @staticmethod
    def encode_data(data):
        if type(data) is not list:
            data = [data]
        res = " ".join([str(el) for el in data])
        to_bytes = bytes(res.encode('utf-8'))
        return to_bytes
    
    @staticmethod
    def grab_parasite_data(parasite):
        res_string = bytes(parasite.get_data()).decode('utf-8')
        #altern = str(object=parasite.get_data(), encoding='utf-8')
        to_int_ary = [ int(x) for x in res_string.split(" ")]
        return to_int_ary[0] if len(to_int_ary) == 1 else to_int_ary

    # instance stuff:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def data_receptacle(self):
        return Necessary._parasite_data_ary[self.idx]
    
    def update_current_layer(self):
        Necessary.update_layer() #update_layer

    @property
    def image(self):
        return Necessary._image #type(self)._image  

    @property
    def current_layer(self):
        return Necessary._current_layer
    
    # @property
    # def layer_x(self):
    #     return Necessary._layer_x
    
    # @property
    # def layer_y(self):
    #     return Necessary._layer_y
    
    # @property
    # def layer_width(self):
    #     return Necessary.layer_width
    
    # @property
    # def layer_height(self):
    #     return Necessary._layer_height
    
    # @property
    # def layer_name(self):
    #     return Necessary._layer_name
    
    @property
    def gamedata(self):
        # maybe... return Necessary._gamedata
        return type(self)._gamedata
    
    @property
    def tool_widgets_ary(self):
        #return type(self)._tool_widgets_ary
        return Necessary._tool_widgets_ary
    
    @property
    def summary_widgets_ary(self):
        #return type(self)._summary_widgets_ary
        return Necessary._summary_widgets_ary
    
    def tool_widget_from_idx(self, index):
        return self.tool_widgets_ary[index]
    
    def summary_widget_from_idx(self, index):
        return self.summary_widgets_ary[index]
    
    
