class DataGrabber():
    def set_data_path(self):#, filepath):
        import sys
        from gi.repository import GLib
        wanted = "other"
        filepath = GLib.path_get_dirname(__file__)
        print(f"DataGrabber here! ;) {filepath}")
        self._basedir = f"{filepath[0:filepath.index(wanted)]}src"
        print(f"DataGrabber here! ;) {self._basedir}")

    '''
        _base_dir = ""
        vars = []
        props = None

        @classmethod
        def _set_basedir(cls):
            import sys
            cls._base_dir = f"{sys.path[0]}/trispackage/gamedata/"

        @classmethod
        def _load_local_file(cls, filename, subfolder =""):
            import json
            with open(f"{cls._base_dir}{subfolder}{filename}.json") as json_file:
                return json.load(json_file)
    '''