from enum import Enum
from random import choice
from colorama import Fore, Back, Style
from itertools import repeat
from multiprocessing import Pool, freeze_support

from wordle_common import State
from wordle_solver import best_word

ANSWER_FILENAME = 'answers.txt'
VALID_FILENAME = 'valid.txt'
ROUNDS = 6


class Mode(Enum):
    INTERACTIVE = 1
    SOLVER = 2
    BENCHMARK = 3

def read_as_list(filename):
    with open(filename, 'r') as f:
        return {word.strip() for word in set(f)}

def get_words(filename):
    words = read_as_list(filename)

    for word in words:
        if len(next(iter(words))) != len(word):
            print(f'word list contains words of different lengths')
            exit(1)

    return words

def get_guess(mode, valid_words, state):

    guess = None 
    if mode == Mode.INTERACTIVE:
        guess = input("Guess: ").lower()
    elif mode in [Mode.SOLVER, Mode.BENCHMARK]:
        guess = best_word(valid_words, state)
        if guess == None:
            print(f'solver did not make a guess')
            print(state)
            exit(1)

    expected_len = len(next(iter(valid_words)))
    if len(guess) != expected_len:
        print(f'guess must be {expected_len} letters long')
        return get_guess(mode, valid_words, state)
    
    if guess not in valid_words:
        print(f'{guess} is not a valid word')
        return get_guess(mode, valid_words, state)

    return guess

def score_guess(guess, answer) -> State:
    green = [pair[0] if pair[0] == pair[1] else '.' for pair in zip(guess, answer)]

    # remove green letters from answer so we don't duplicate them into yellow
    for index, letter in enumerate(guess):
        if green[index] == letter:
            answer = list(answer)
            answer[index] = '.'
            answer = ''.join(answer)

    yellow = []
    grey = set()
    yellow_negative = dict()
    for index, letter in enumerate(guess):
        if green[index] == letter:
            continue
        elif letter in answer:
            yellow.append(letter)
            yellow_negative[index] = yellow_negative.get(index, set()) | set(letter)
            # after finding a yellow, remove it from the answer so duplicates of the letter in guess don't all match the same instance of the letter
            # if there are multiple instances of the letter in guess and answer then the number of yellows is the minimum of the number of instances in each
            answer = list(answer)
            answer[answer.index(letter)] = '.'
            answer = ''.join(answer)
        elif letter not in green and letter not in yellow:
            grey.add(letter)

    return State(green, yellow, grey, yellow_negative, {guess})

def combine_scores(s_old: State, s_new: State) -> State:
    green = [pair[0] if pair[0] != '.' else pair[1] for pair in zip(s_old.green, s_new.green)]
    added_greens = [pair[1] for pair in zip(s_old.green, s_new.green) if pair[0] == '.' and pair[1] != '.']
    removed_greens = [pair[0] for pair in zip(s_old.green, s_new.green) if pair[0] != '.' and pair[1] == '.']

    mod_old_yellows = s_old.yellow.copy()
    mod_new_yellows = s_new.yellow.copy()

    # new yellow list won't include new greens, so remove each new green from old yellows
    # these old yellows were conveted into greens this round
    for added_green in added_greens:
        if mod_old_yellows.count(added_green) > 0:
            mod_old_yellows.remove(added_green)

    # if a known green wasn't used it will show up as a new yellow
    for removed_green in removed_greens:
        if mod_new_yellows.count(removed_green) > 0:
            mod_new_yellows.remove(removed_green)

    # after adjustment, if the there are more old yellows for a letter than new yellows,
    # then that yellow info wan't used this turn but should still be carried forward
    for letter in set(mod_old_yellows):
        diff = mod_old_yellows.count(letter) - mod_new_yellows.count(letter)
        if diff > 0:
            for _ in range(diff):
                mod_new_yellows.append(letter)

    grey = s_old.grey.union(s_new.grey)

    yellow_negative = dict()
    for key in s_old.yellow_negative.keys() | s_new.yellow_negative.keys():
        yellow_negative[key] = s_old.yellow_negative.get(key, set()) | s_new.yellow_negative.get(key, set())

    return State(green, mod_new_yellows, grey, yellow_negative, s_old.guesses | s_new.guesses)

def print_result(guess, score: State):
    used_yellow = []
    for index, letter in enumerate(guess):
        color = Back.LIGHTBLACK_EX + Fore.WHITE
        if score.green[index] == letter:
            color = Back.GREEN + Fore.WHITE
        elif letter in score.yellow and score.yellow.count(letter) - used_yellow.count(letter) > 0:
            used_yellow.append(letter)
            color = Back.YELLOW + Fore.BLACK

        print(f'{color} {letter} {Style.RESET_ALL}', end='')
    print()

def play(mode, answer, valid_words, debug=False):
    won = False
    guess = None
    state = None
    for round_number in range(ROUNDS):
        if state and debug:
            print(f'total green: "{"".join(state.green)}"')
            print(f'total yellow: {sorted(state.yellow)}')
            print(f'total gray: {sorted(list(state.grey))}')
            print(f'total yellow neg: {state.yellow_negative}')

        guess = get_guess(mode, valid_words, state)

        score = score_guess(guess, answer)

        if mode in [Mode.INTERACTIVE, Mode.SOLVER]:
            print_result(guess, score)

        if state:
            state = combine_scores(state, score)
        else:
            state = score

        if guess == answer:
            won = True
            break

    if won:
        if mode in [Mode.INTERACTIVE, Mode.SOLVER]:
            print(f'You won in {round_number + 1} turns!')
        return (answer, round_number)
    else:
        if mode in [Mode.INTERACTIVE, Mode.SOLVER]:
            print(f'You lost - correct answer was "{answer}"')
        return (answer, None)

def benchmark(mode, answers, valid_words):
    with Pool() as pool:
        results = pool.starmap(play, zip(repeat(mode), answers, repeat(valid_words)), 50)

    wins = [result[1] for result in results if result[1] != None]
    losses = [result[0] for result in results if result[1] == None]
    
    print(f'Games won: {len(wins)} / {len(answers)} ({round(len(wins) / len(answers) * 100, 3)}%)')
    print(f'Avg rounds for win: {round(sum(wins) / len(wins), 2)}')
    print(f'Losses: {losses}')

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

### FIX

#  c  a  r  e  s 
#  l  a  t  e  r 
#  w  a  k  e  r 
#  g  a  y  e  r 
#  h  a  z  e  r 
#  p  a  v  e  r 
# You lost - correct answer was "paper"

if __name__ == '__main__':
    freeze_support()

    mode = Mode.BENCHMARK
    debug = False

    run(mode, debug)


