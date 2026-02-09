def generate_xml(image, facename = "***** Place a name"):
    special = {"Á": 193,"È": 200,"Ì": 204,"Ò": 210,"Ù": 217,"à": 224,"è": 232,"ì": 236,"ò": 242,"ù": 249,"&": 38,"<": 60,">": 62,'"': 34,"'": 39,"space": 32," ": 32}
    chars_count = 0
    char_info = ""
    lineHeight = 0
    for idx, layer in enumerate(image.get_layers()):
        if layer.get_visible():
            layername = layer.get_name()
            id = None #get_char_code(layer.get_name(), idx)
            if layername in special:
                chars_count += 1
                id = special[layername]
            elif len(layername.encode("utf-8")) == 1:
                chars_count += 1
                id = ord(layername)
            else:
                id = f"****** {layername} (layer: {idx})"
            _, x, y = layer.get_offsets()
            w = layer.get_width()
            h = layer.get_height()
            if lineHeight < h:
                lineHeight = h
            char_info += f'    <char id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" xoffset="0" yoffset="0" xadvance="{w}"/>\n'
    res = f'<?xml version="1.0"?>\n<font>\n  <info face="{facename}" size="4"/>\n  <common lineHeight="{lineHeight}"/>\n  <chars count="{chars_count}">\n{char_info}  </chars>\n</font>'
    print(res)

#generate_xml(Gimp.get_images()[0])
