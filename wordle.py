#!/usr/bin/env python3
import argparse

from random import choice
from multiprocessing import freeze_support
from textwrap import dedent

from common import VALID_FILENAME, ANSWER_FILENAME, DEFAULT_ROUNDS, Mode, get_words
from play import play
from benchmark import benchmark

DEFAULT_MODE = Mode.SOLVE

def run(args):
    # bit of a hack
    mode = next((m for m in (getattr(args, mode.value) for mode in Mode) if m != None), DEFAULT_MODE)

    debug = args.debug
    hard = args.hard
    rounds = args.rounds
    override_answer = args.answer

    valid_words = get_words(args.valid_words_file)
    answers = get_words(args.answer_words_file)

    answer = override_answer or choice(list(answers))

    if answer not in valid_words:
        print(f'"{answer}" is not in the valid word list')
        exit(1)

    if mode == Mode.BENCHMARK:
        benchmark(mode, answers, valid_words, rounds)
    else:
        play(mode, answer, valid_words, hard, rounds, debug)

if __name__ == '__main__':
    freeze_support()

    arg_parser = argparse.ArgumentParser()

    mode_group = arg_parser.add_mutually_exclusive_group()
    for mode in Mode:
        mode_group.add_argument(f'-{mode.value[0]}', f'--{mode.value}', action='store_const', const=mode,
            help=f'use "{mode.value}" mode{" (default)" if mode == DEFAULT_MODE else ""}')

    arg_parser.add_argument('-r', '--rounds', type=int, default=DEFAULT_ROUNDS, metavar='num_rounds',
        help=f'number of rounds (default="{DEFAULT_ROUNDS}")')
    arg_parser.add_argument('-a', '--answer', type=str, metavar='word',
        help='sets the answer word - useful for debugging a specific case. Ignored in benchmark mode')
    arg_parser.add_argument('-H','--hard', action='store_true',
        help='enable hard mode (any revealed hints must be used in subsequent guesses). Ignored in benchmark mode.')
    arg_parser.add_argument('-d', '--debug', action='store_true',
        help='print extra output for debugging',)

    arg_parser.add_argument('--answer-words-file', type=str, metavar='path', default=ANSWER_FILENAME,
        help=f'file with all possible answers (default="{ANSWER_FILENAME}")')
    arg_parser.add_argument('--valid-words-file', type=str, metavar='path', default=VALID_FILENAME,
        help=f'file with all accepted words (default="{VALID_FILENAME}")')

    args = arg_parser.parse_args()

    run(args)
