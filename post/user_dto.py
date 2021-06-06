class UserDto:
    def __init__(self):
        self.user_name = ''
        self.password = ''

    @classmethod
    def to_dict(cls, obj):
        entry = obj.__dict__
        return entry

    @classmethod
    def from_dict(cls, dict):
        obj = UserDto()
        obj.__dict__ = dict
        return obj
