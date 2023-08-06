from xerparser.model.classes.schedoption import SchedOption

class SchedOptions:

    _schoptions = []

    def __init__(self):
        self.index = 0

    def add(self, params):
        self._schoptions.append(SchedOption(params))

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.actv_code_type_id == id, cls._schoptions))
        if len(obj) > 0:
            return obj[0]
        return obj

    @property
    def count(self):
        return len(self._schoptions)

    def __len__(self):
        return len(SchedOptions._schoptions)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._schoptions):
            raise StopIteration
        idx = self.index
        self.index += 1
        return self._schoptions[idx]