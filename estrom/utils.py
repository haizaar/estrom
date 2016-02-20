
class DotDict(dict):
    """
    a dictionary that supports dot notation access
    as well as dictionary access notation
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __init__(self, dictionary):
        for key, val in dictionary.items():
            self[key] = val

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            val = self.__class__(val)
        return super().__setitem__(key, val)

    __setattr__ = __setitem__
