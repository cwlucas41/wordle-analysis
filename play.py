import math

from colorama import Fore, Back, Style

from common import WORD_LENGTH, DEFAULT_ROUNDS, Mode
from state import State, score_guess, combine_scores, validate_guess_hard_mode
from solver import best_word

def get_guess(mode, valid_words, hard, state, round_number, rounds, debug):
    guess = None
    while True:
        if mode == Mode.PLAY:
            guess = input("Guess: ").lower()
        elif mode in [Mode.SOLVE, Mode.BENCHMARK]:
            guess = best_word(valid_words, hard, state, round_number, rounds, debug)
            if guess == None:
                print(f'solver did not make a guess')
                print(state)
                exit(1)

        if len(guess) != WORD_LENGTH:
            print(f'"{guess}" is not {WORD_LENGTH} letters long')
            continue
        
        if guess not in valid_words:
            print(f'"{guess}" is not a valid word')
            continue

        if hard and not validate_guess_hard_mode(guess, state):
            print(f'"{guess}" does not use all previous hints which is required in hard mode')
            continue

        break
    return guess

def print_result(guess, score: State, debug=False):
    used_yellow = []
    for index, letter in enumerate(guess):
        color = None
        if score.green[index] == letter:
            color = Back.GREEN + Fore.WHITE
        elif letter in score.yellow and score.yellow.count(letter) - used_yellow.count(letter) > 0:
            used_yellow.append(letter)
            color = Back.YELLOW + Fore.BLACK
        elif letter in score.grey:
            color = Back.LIGHTBLACK_EX + Fore.WHITE
        else:
            # these indicate that the letter appears in the word, but the answer has less instances of the letter than the guess
            color = (Back.RED if debug else Back.LIGHTBLACK_EX) + Fore.WHITE

        print(f'{color} {letter} {Style.RESET_ALL}', end='')
    print()

def play(mode, answer, valid_words, hard, rounds, debug=False):
    won = False
    guess = None
    state = None
    for round_number in range(1, rounds + 1):
        if round_number == DEFAULT_ROUNDS + 1 and mode in [Mode.PLAY, Mode.SOLVE]:
            print('---------------')            
        if state and debug:
            print(f'total green: "{"".join(state.green)}"')
            print(f'total yellow: {sorted(state.yellow)}')
            print(f'total gray: {sorted(list(state.grey))}')

        if state and len(list(filter(lambda x: x != ".",state.green))) == 5:
            guess = "".join(state.green)
        else:
            guess = get_guess(mode, valid_words, hard, state, round_number, rounds, debug)

        score = score_guess(guess, answer)

        if mode in [Mode.PLAY, Mode.SOLVE]:
            print_result(guess, score, debug)

        if state:
            state = combine_scores(state, score)
        else:
            state = score

        if guess == answer:
            won = True
            break

    if won:
        if mode in [Mode.PLAY, Mode.SOLVE]:
            print(f'You won in {round_number} turns!')
        return (answer, round_number)
    else:
        if mode in [Mode.PLAY, Mode.SOLVE]:
            print(f'You lost - correct answer was "{answer}"')
        return (answer, math.inf)