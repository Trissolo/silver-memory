class WidgetTree:
    def __init__(self, root_dir):
        self._generator = _TreeGenerator(root_dir)
    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)
        self._generator = None
        

class _TreeGenerator:   
    def __init__(self, root_dir):
        self._root_dir = root_dir #pathlib.Path(root_dir)
        self._tree = []
        self.PIPE = "│"
        self.ELBOW = "└──"
        self.TEE = "├──"
        self.PIPE_PREFIX = "│   "
        self.SPACE_PREFIX = "    "
    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree
    def _tree_head(self):
        self._tree.append(f"{self._root_dir}")
        self._tree.append(self.PIPE)
    def _tree_body(self, directory, prefix=""):
        entries = directory.get_children() #directory.iterdir()
        entries = sorted(entries, key=lambda entry: not hasattr(entry, 'get_children')) #entry.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            if hasattr(entry, 'get_children'):
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)
    
    def _add_directory(self, directory, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {directory.get_name()}")
        if index != entries_count - 1:
            prefix += self.PIPE_PREFIX
        else:
            prefix += self.SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())
    
    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.get_name()}")