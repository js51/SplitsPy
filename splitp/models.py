from enum import Enum, auto

class Model(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
    JC      = auto()
    K2ST    = auto()