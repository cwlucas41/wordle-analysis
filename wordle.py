#!/usr/bin/env python3

from random import choice
from itertools import repeat
import math
from multiprocessing import Pool, freeze_support

from wordle_common import VALID_FILENAME, ANSWER_FILENAME, Mode, get_words
from wordle_play import play

def benchmark(mode, answers, valid_words):
    with Pool() as pool:
        results = pool.starmap(play, zip(repeat(mode), answers, repeat(valid_words)), 25)

    histogram = dict()
    for word, end_round in results:
        histogram[end_round] = histogram.get(end_round, set()) | {word}

    win_count = sum([len(words) for end_round, words in histogram.items() if end_round != math.inf])
    game_count = sum([len(words) for _, words in histogram.items()])
    
    print(f'Win rate: - {round(win_count / len(answers) * 100, 3)}%')
    print(f'Games - {game_count}')
    for end_round in sorted(histogram.keys()):
        words = histogram[end_round]
        if end_round != math.inf:
            print(f'{end_round}: {len(words)}')
        else:
            print(f'L: {len(words)} - {sorted(list(words))}')

def run(mode, debug):
    valid_words = get_words(VALID_FILENAME)
    wordle_answers = get_words(ANSWER_FILENAME)

    # TODO: flag for answer set
    answers = wordle_answers
    answer = choice(list(answers))

    if mode == Mode.BENCHMARK:
        benchmark(mode, wordle_answers, valid_words)
    else:
        play(mode, answer, valid_words, debug)

if __name__ == '__main__':
    freeze_support()

    mode = Mode.BENCHMARK
    debug = False

    run(mode, debug)


