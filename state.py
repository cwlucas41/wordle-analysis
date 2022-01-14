import re
import string

from dataclasses import dataclass

# TODO: refactor to proper class instead of this mess
@dataclass
class State:
    green: list
    yellow: list
    grey: set
    yellow_negative: dict
    known_letter_count: dict
    unhinted_letters: set
    guesses: set

def validate_guess_hard_mode(guess, state):
    if state == None:
        return True

    green_yellow = [letter for letter in state.green + state.yellow if letter != '.']
    
    # greens match positionally
    uses_greens = re.compile(f'^{"".join(state.green)}$').match(guess)

    # yellows might match to green slots, but if there is a green and yellow then we actually have a hint of duplicate letters
    # this ensures the count of the letter in the word is at least the number of hints we have for the letter
    # 
    # this asserts that all yellows appear in the word (which is the explained way to think of yellows) implicitly
    uses_yellows = all(guess.count(letter) >= green_yellow.count(letter) for letter in green_yellow)

    # hard mode does not enforce other constraints like greys, or other information
    return uses_yellows and uses_greens

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
        
    known_letter_count = dict()
    green_yellow = [letter for letter in green + yellow if letter != '.']
    for letter in set(green_yellow):
        if guess.count(letter) > green_yellow.count(letter):
            known_letter_count[letter] = green_yellow.count(letter)

    unhinted_letters = set(string.ascii_lowercase) - set(green) - set(yellow) - grey
    guesses = {guess}

    return State(green, yellow, grey, yellow_negative, known_letter_count, unhinted_letters, guesses)

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

    grey = s_old.grey | s_new.grey

    yellow_negative = dict()
    for key in s_old.yellow_negative.keys() | s_new.yellow_negative.keys():
        yellow_negative[key] = s_old.yellow_negative.get(key, set()) | s_new.yellow_negative.get(key, set())

    known_letter_count = {**s_old.known_letter_count, **s_new.known_letter_count}
    for key in s_old.known_letter_count.keys() & s_new.known_letter_count.keys():
        if s_old.known_letter_count[key] != s_new.known_letter_count[key]:
            print(f'bug in known_letter_count - "{key}" can\'t have count of {s_old.known_letter_count[key]} and {s_new.known_letter_count[key]}')
            del known_letter_count[key]

    
    unhinted_letters = set(string.ascii_lowercase) - set(green) - set(mod_new_yellows) - grey

    guesses = s_old.guesses | s_new.guesses

    return State(green, mod_new_yellows, grey, yellow_negative, known_letter_count, unhinted_letters, guesses)