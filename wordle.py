#!/usr/bin/env python3
import argparse
import math

from random import choice
from itertools import repeat
from multiprocessing import Pool, freeze_support
from textwrap import dedent

from wordle_common import VALID_FILENAME, ANSWER_FILENAME, Mode, get_words
from wordle_play import play

def benchmark(mode, answers, valid_words, hard):
    with Pool() as pool:
        results = pool.starmap(play, zip(repeat(mode), answers, repeat(valid_words), repeat(hard)), 25)

    histogram = dict()
    for word, end_round in results:
        histogram[end_round] = histogram.get(end_round, set()) | {word}

    win_count = sum([len(words) for end_round, words in histogram.items() if end_round != math.inf])
    game_count = sum([len(words) for _, words in histogram.items()])
    
    print(f'Win rate: - {round(win_count / len(answers) * 100, 3)}%')
    print(f'Total games - {game_count}')
    print(f'Hard mode - {hard}')
    for end_round in sorted(histogram.keys()):
        words = histogram[end_round]
        if end_round != math.inf:
            print(f'{end_round}: {len(words)}')
        else:
            print(f'L: {len(words)} - {sorted(list(words))}')

def run(args):
    mode = args.mode
    verbose = args.verbose
    hard = args.hard
    override_answer = args.answer

    if mode == Mode.BENCHMARK and override_answer:
        print(f'providing an override answer is not compatible with {mode} mode')
        exit(1)

    valid_words = get_words(VALID_FILENAME)
    answers = get_words(ANSWER_FILENAME)

    answer = override_answer or choice(list(answers))

    if answer not in valid_words:
        print(f'"{answer}" is not in the valid word list')
        exit(1)

    if mode == Mode.BENCHMARK:
        benchmark(mode, answers, valid_words, hard)
    else:
        play(mode, answer, valid_words, hard, verbose)

if __name__ == '__main__':
    freeze_support()

    arg_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, conflict_handler='resolve')
    arg_parser.add_argument('-m', '--mode', type=Mode, choices=list(Mode), default=Mode.SOLVER.value,
        help=dedent('''\
            Choose running mode.
            - "play" for a human to play
            - "solver" (default) for the solving algorithm to play
            - "benchmark" for the solver to play over all possible ansers and print summary
            '''))
    arg_parser.add_argument('-a', '--answer', type=str,
        help='sets the answer word - usefull for debugging a specific case')
    arg_parser.add_argument('-h', '--hard', action='store_true',
        help='enable hard mode (any revealed hints must be used in subsequent guesses)')
    arg_parser.add_argument('-v', '--verbose', action='store_true',
        help='increase output verbosity',)
    args = arg_parser.parse_args()

    run(args)
