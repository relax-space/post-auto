class NameStrDto:
    def __init__(self, name, value):
        self.name: str = name
        self.value: str = value

    @classmethod
    def to_dict(cls, obj):
        entry = obj.__dict__
        return entry

    @classmethod
    def from_dict(cls, dict):
        obj = NameStrDto()
        obj.__dict__ = dict
        return obj
