from json import JSONEncoder

from .guild import Sort
from .number import Infinity

__all__ = ("Encoder",)


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Infinity):
            return str(o)
        if isinstance(o, Sort):
            return o.value
        return super().default(o)
