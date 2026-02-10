class LayerManager():
    image = None
    layer = None

    @classmethod
    def provide_image(cls, image):
         cls.image = image
         cls.layer = None
         cls.update()

    @classmethod
    def update(cls):
        cls.layer = cls.image.get_selected_layers()[0]

    # instance things:

    @property
    def layer(self):
        return LayerManager.layer
    
    def update_layer(self):
        LayerManager.update()
