#!/usr/bin/env python3
import argparse

from random import choice
from multiprocessing import freeze_support
from textwrap import dedent

from wordle_common import VALID_FILENAME, ANSWER_FILENAME, Mode, get_words
from wordle_play import play
from wordle_benchmark import benchmark

def run(args):
    mode = args.mode
    verbose = args.verbose
    hard = args.hard
    rounds = args.rounds
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
        benchmark(mode, answers, valid_words, hard, rounds)
    else:
        play(mode, answer, valid_words, hard, rounds, verbose)

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
    arg_parser.add_argument('-a', '--answer', type=str, metavar='word',
        help='sets the answer word - usefull for debugging a specific case')
    arg_parser.add_argument('-r', '--rounds', type=int, default=6, metavar='num_rounds',
        help='number of rounds (default=6)')
    arg_parser.add_argument('-h', '--hard', action='store_true',
        help='enable hard mode (any revealed hints must be used in subsequent guesses)')
    arg_parser.add_argument('-v', '--verbose', action='store_true',
        help='increase output verbosity',)
    args = arg_parser.parse_args()

    run(args)
