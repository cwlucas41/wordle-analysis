from enum import Enum

ANSWER_FILENAME = 'words/answers.txt'
VALID_FILENAME = 'words/valid.txt'
WORD_LENGTH = 5
DEFAULT_ROUNDS=6

class Mode(Enum):
    PLAY = 'play'
    SOLVE = 'solve'
    BENCHMARK = 'benchmark'

    def __str__(self):
        return self.value
    
def get_words(filename):
    with open(filename, 'r') as f:
        words = {word.strip() for word in set(f)}
    for word in words:
        if WORD_LENGTH != len(word):
            print(f'word list contains words of different lengths')
            exit(1)

    return words