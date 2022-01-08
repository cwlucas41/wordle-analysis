from colorama import Fore, Back, Style
import math

from wordle_common import WORD_LENGTH, ROUNDS, Mode, State, get_words
from wordle_score import score_guess, combine_scores
from wordle_solver import best_word


def get_guess(mode, valid_words, state, round_number):
    guess = None 
    if mode == Mode.INTERACTIVE:
        guess = input("Guess: ").lower()
    elif mode in [Mode.SOLVER, Mode.BENCHMARK]:
        guess = best_word(valid_words, state, round_number)
        if guess == None:
            print(f'solver did not make a guess')
            print(state)
            exit(1)

    if len(guess) != WORD_LENGTH:
        print(f'guess must be {WORD_LENGTH} letters long')
        return get_guess(mode, valid_words, state)
    
    if guess not in valid_words:
        print(f'{guess} is not a valid word')
        return get_guess(mode, valid_words, state)

    return guess

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
    for round_number in range(1, ROUNDS + 1):
        if state and debug:
            print(f'total green: "{"".join(state.green)}"')
            print(f'total yellow: {sorted(state.yellow)}')
            print(f'total gray: {sorted(list(state.grey))}')
            print(f'total yellow neg: {state.yellow_negative}')

        guess = get_guess(mode, valid_words, state, round_number)

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
            print(f'You won in {round_number} turns!')
        return (answer, round_number)
    else:
        if mode in [Mode.INTERACTIVE, Mode.SOLVER]:
            print(f'You lost - correct answer was "{answer}"')
        return (answer, math.inf)