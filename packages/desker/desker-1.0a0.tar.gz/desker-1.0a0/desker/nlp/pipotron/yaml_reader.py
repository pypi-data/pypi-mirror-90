import ruamel.yaml as yaml


class YAMLReader:
    def __init__(self, path: str):
        self._path = path
        self.file = None

    def __enter__(self):
        self.file = open(self._path, "r")
        return yaml.safe_load(self.file.read())

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()
