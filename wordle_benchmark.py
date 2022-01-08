import math

from itertools import repeat
from multiprocessing import Pool

from wordle_play import play

def benchmark(mode, answers, valid_words, hard, rounds):
    with Pool() as pool:
        results = pool.starmap(play, zip(repeat(mode), answers, repeat(valid_words), repeat(hard), repeat(rounds)), 25)

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