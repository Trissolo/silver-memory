
#from os import listdir
#complete_path= f"{sys.path[0]}/"
#qqqu = sys.path[0]

# wanted dir path, as string
#folder_path = f"{sys.path[0]}{GLib.DIR_SEPARATOR_S}splitted_gamedata{GLib.DIR_SEPARATOR_S}"

# list of filenames, as string
#dir_content = listdir(folder_path)
#print(*dir_content, sep="\n")
#print(complete_path)


def _grab_file_hardcoded():
    import sys
    import json
    base_dir = f"{sys.path[0]}/trispackage/splitted_gamedata/"

    def _load_local_file(filename, base_dir = base_dir):
        with open(f"{base_dir}{filename}.json") as json_file:
            return json.load(json_file)
    
    # Tech data
    filename = "misc_info"
    misc_info = _load_local_file(filename)
    
    # ---
    vars_ary = []
    for filename in ["bool_names", "crumble_names", "nibble_names", "byte_names"]:
        vars_ary.append(_load_local_file(filename))
    
    # ---
    filename = "hover_names"
    hover_names_ary = _load_local_file(filename)

    # Tech/thingProps data
    thingProps_dataSize = misc_info['thingProps_dataSize']
    #thingProps_props = thingProps_dataSize.keys() #misc_info['thingProps']

    # Thing Kinds
    thingKind_dict = {}
    for elem in misc_info['thingKind']:
        a = elem[ "val"]
        b = elem[ "comment"]
        #print(f"{elem[ "val"]} <--> {elem["comment"]}")
        thingKind_dict[b] = a
        thingKind_dict[int(a)] = b
    
    names = {"hover_names_ary": hover_names_ary,
             "vars_ary": vars_ary, #ary of arys
             "thingKind_dict": thingKind_dict}

    # check
    for elem in names:
        print(f"{elem =}")
        print(*names[elem], sep="\n")

    
    return names, thingProps_dataSize

names, thingProps_dataSize = _grab_file_hardcoded()

'''
class Stocker():
    data_ary = []
    summary_ary = []
    tool_ary = []
    
    @classmethod
    def build_and_fill(cls):
        gr =  ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        ita = [*"ABCDE"]
        nums = range(5)
'''