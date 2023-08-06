from typing import Union
from typing import List
from typing import Dict


STR_OR_LIST = Union[str, List[str]]


class SingletonMetaClass(type):
    _instances_ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances_:
            cls._instances_[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs
            )
        return cls._instances_[cls]


class BagOfWords(metaclass=SingletonMetaClass):
    def __init__(self):
        self._dict = {}

    @property
    def keys(self):
        return self._dict.keys()

    @staticmethod
    def _list_of_strings(s: STR_OR_LIST):
        if isinstance(s, str):
            return [s]
        return s

    def add_dict(self, d: Dict[str, STR_OR_LIST]):
        for key, values in d.items():
            values = self._list_of_strings(values)
            if key in self._dict:
                self._dict[key].extend(values)
            else:
                self._dict[key] = values

    def add(self, key: str, values: STR_OR_LIST):
        values = self._list_of_strings(values)
        if key not in self._dict:
            self._dict[key] = []
        self._dict[key].extend(values)

    def set(self, key: str, values: STR_OR_LIST):
        self._dict[key] = self._list_of_strings(values)

    def get(self, category: str):
        if not category in self.keys:
            raise ValueError(f"Bag of word does not contain `{category}`")
        return self._dict[category]
