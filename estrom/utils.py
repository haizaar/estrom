import base64
import math


class DotDict(dict):
    """
    a dictionary that supports dot notation access
    as well as dictionary access notation
    """
    def __init__(self, dictionary):
        for key, val in dictionary.items():
            self[key] = val

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            val = self.__class__(val)
        return super().__setitem__(key, val)

    __setattr__ = __setitem__
    __getattr__ = dict.__getitem__


class Hasher:
    @classmethod
    def index_qid_to_sid(cls, index, qid):
        # Remove '===...' padding - it's ugly and we can reconstruct it later
        encoded_index = base64.b32encode(index.encode()).decode().rstrip("=")
        sid = encoded_index + "_" + qid
        return sid

    @classmethod
    def sid_to_index_qid(cls, sid):
        index, _, qid = sid.partition("_")
        index = base64.b32decode(cls.pad(index).encode()).decode()
        return index, qid

    @classmethod
    def pad(cls, v, length=8):  # TODO: Understand why it's 8
        return v.ljust(math.ceil(float(len(v))/length)*length, "=")
