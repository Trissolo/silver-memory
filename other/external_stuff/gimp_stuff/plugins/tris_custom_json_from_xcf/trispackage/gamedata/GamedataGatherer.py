
#from os import listdir
#complete_path= f"{sys.path[0]}/"
#qqqu = sys.path[0]

# wanted dir path, as string
#folder_path = f"{sys.path[0]}{GLib.DIR_SEPARATOR_S}splitted_gamedata{GLib.DIR_SEPARATOR_S}"

# list of filenames, as string
#dir_content = listdir(folder_path)
#print(*dir_content, sep="\n")
#print(complete_path)
import json

class GamedataGatherer():
    _base_dir = ""
    vars = []
    props = None

    @classmethod
    def _set_basedir(cls):
        import sys
        cls._base_dir = f"{sys.path[0]}/trispackage/gamedata/"

    @classmethod
    def _load_local_file(cls, filename, subfolder =""):
        with open(f"{cls._base_dir}{subfolder}{filename}.json") as json_file:
            return json.load(json_file)
    
    @classmethod
    def _on_console(cls):
        # bgrnds:
        RED     = '\033[41m'
        GREEN   = '\033[42m'
        YELLOW  = '\033[43m'
        BLUE    = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN    = '\033[46m'
        WHITE   = '\033[47m'
        RESET   = '\033[49m'
        tempstoca = vars(cls)
        for item in tempstoca:
            if not item.startswith("_"):
                print(f"{YELLOW} {item} {RESET}: {tempstoca[item]}\n")
        return cls
    
    @classmethod
    def _load_all(cls):
        cls._set_basedir()

        subfolder = "var-stuff/"
        filename = "varkind"

        # varkinds
        # ['Bool', 'Crumble', 'Nibble', 'Byte']
        cls.varkinds = cls._load_local_file(filename, subfolder)

        # vars
        # [
        #   ['unused', 'r1#doorIsOpen', 'r1#wrenchTaken', 'r1#... ],
        #   ...
        #   ['unused', 'digita', 'digitb', 'digitc']
        # ]
        for filename in cls.varkinds:
            cls.vars.append(cls._load_local_file(f"{filename.lower()}-names", subfolder))  

        filename = "json-props"
        # props_datasize
        # {'kind': 1, 'hoverName': 1, 'suffix': 2, 'skipCond': 3, 'animation': 1, 'noInteraction': 1}
        cls.props_datasize = cls._load_local_file(filename)
        
        # props
        # ['kind', 'hoverName', 'suffix', 'skipCond', 'animation', 'noInteraction']
        cls.props = [*cls.props_datasize.keys()]

        subfolder = "kind-stuff/"
        filename = "kind"
        # kinds
        # {'BACKGROUND': -5, 'RIDICULOUSLY FARAWAY': 0, 'TRIGGER AREA': 1, 'COVERED': 2, 'ALWAYS BACK': 3, 'DEPTH SORTED': 4, 'FOREGROUND': 800}
        cls.kinds = cls._load_local_file(filename, subfolder)
        
        filename = "hover-names"
        # hoverNames
        # ['?', 'Pulsante', 'Affare metallico', 'Coperchio', ...]
        cls.hoverNames = cls._load_local_file(filename)

        # end
        return cls
        
GamedataGatherer._load_all()
