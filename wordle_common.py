from dataclasses import dataclass
from enum import Enum

ANSWER_FILENAME = 'words/answers.txt'
VALID_FILENAME = 'words/valid.txt'
WORD_LENGTH = 5
ROUNDS = 6

@dataclass
class State:
    green: list
    yellow: list
    grey: set
    yellow_negative: dict
    guesses: set

class Mode(Enum):
    INTERACTIVE = 1
    SOLVER = 2
    BENCHMARK = 3
    
def get_words(filename):
    with open(filename, 'r') as f:
        words = {word.strip() for word in set(f)}
    for word in words:
        if WORD_LENGTH != len(word):
            print(f'word list contains words of different lengths')
            exit(1)

    return words