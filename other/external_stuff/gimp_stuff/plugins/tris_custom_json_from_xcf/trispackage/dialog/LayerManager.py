class LayerManager():
    image = None
    layer = None

    @classmethod
    def setup(cls, image):
         cls.image = image
         cls.layer = None
         cls.update()

    @classmethod
    def update(cls):
        cls.layer = cls.image.get_selected_layers()[0]

    # instance things:
    def __init__(self, image):
        if image is not None:
            self.set_image_globally(image)

    @property
    def layer(self):
        return LayerManager.layer
    
    def update_layer(self):
        LayerManager.update()
        
    #def __call__(self):
    #    return type(self).layer
    
    def set_image_globally(self, image):
        LayerManager.setup(image)
