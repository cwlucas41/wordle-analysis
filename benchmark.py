import math

from itertools import repeat
from multiprocessing import Pool
from time import time

from play import play

def benchmark(mode, answers, valid_words, rounds, debug):

    missed_words = dict()

    with Pool() as pool:
        for hard in [False, True]:
            start = time()
            results = pool.starmap(play, zip(repeat(mode), answers, repeat(valid_words), repeat(hard), repeat(rounds)), 25)
            end = time()

            histogram = dict()
            for word, end_round in results:
                histogram[end_round] = histogram.get(end_round, set()) | {word}

            win_count = sum([len(words) for end_round, words in histogram.items() if end_round != math.inf])
            game_count = sum([len(words) for _, words in histogram.items()])
            missed_words[hard] = histogram[math.inf]
            
            print(f'{"Hard" if hard else "Easy"} mode')
            print(f'Win rate: - {round(win_count / len(answers) * 100, 1)}%')
            print(f'Total games - {game_count}')
            print(f'Duration: {round(end - start, 1)}s')

            for end_round in sorted([key for key in histogram.keys() if key != math.inf]):
                words = histogram[end_round]
                print(f'{end_round}\ufe0f\u20e3 : {len(words)}')

            print(f'☠️ : {len(missed_words[hard])}')
            if len(missed_words[hard]) > 0:
                print(sorted(list(missed_words[hard])))

            print()

    if debug:
        easy_misses = missed_words[False]
        hard_misses = missed_words[True]

        easy_only = easy_misses - hard_misses
        hard_only = hard_misses - easy_misses
        both = easy_misses & hard_misses

        print(f'Easy only misses - {len(easy_only)}')
        if len(easy_only) > 0:
            print(f'{sorted(list(easy_only))}')
        print()

        print(f'Hard only misses - {len(hard_only)}')
        if len(hard_only) > 0:
            print(f'{sorted(list(hard_only))}')
        print()

        print(f'Easy and Hard misses - {len(both)}')
        if len(both) > 0:
            print(f'{sorted(list(both))}')