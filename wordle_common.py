from dataclasses import dataclass

@dataclass
class State:
    green: list
    yellow: list
    grey: set
    yellow_negative: dict
    guesses: set