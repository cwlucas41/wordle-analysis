#!/usr/bin/env python3

import string

from zlib import crc32

from common import WORD_LENGTH, VALID_FILENAME
from state import State, validate_guess_hard_mode

# useful for effectively randomizing a list of strings and then picking one of them
# with the condition that the same result is given for the same input
# utilizing this allows the program to pick an item from a list without meaningful bias (alphabetical or otherwise)
# having the result be deterministic allows for the same solution to be derived from the same initial conditions
def deterministic_random_first(words):
    if len(words) == 0:
        return None

    return sorted(words, key=lambda x: crc32(x.encode()))[0]

def positional_frequency(words):
    table = dict()
    for index in range(WORD_LENGTH):
        frequencies = dict()
        for letter in string.ascii_lowercase:
            matches = {word for word in words if word[index] == letter}
            frequency = len(matches) / len(words) / WORD_LENGTH
            frequencies[letter] = frequency
        table[index] = frequencies
    return table

def score(guessable_words, candidate_words, state: State, debug):

    candidate_count = len(candidate_words)
    reduced_guessable_words = guessable_words

    # Optimization:
    # If we already know most of the letters as greens, then it can be tricky to find the one remaining letter
    # If allowed (not in hard mode) this finds all the candidates for the remaining one or two letters so that
    # the next guess can be a word that includes the most of those letters possible.
    if state and state.green.count('.') <= 2:
        if len(list(filter(lambda x: x != ".",state.green))) == 5:
            return [("".join(state.green),0)] # we know this to be the correct answer
        vip_letters = set.union(*[{w for w,g in zip(word, state.green) if g == '.'} for word in candidate_words])
        if debug:
            print(f'vip letters: {vip_letters}')
        if len(vip_letters) > 2:
            vip_dict = dict()
            for word in guessable_words:
                vip_and_word_letters = len(set(word) & vip_letters)
                vip_dict[vip_and_word_letters] = vip_dict.get(vip_and_word_letters, set()) | {word}

            top_vip_set = sorted(vip_dict.keys(), reverse=True)[0]
            if debug:
                print(f'top vip set: {top_vip_set}')
            if top_vip_set > 1 and (state.green.count('.') <=1 or top_vip_set >= 3):
                reduced_guessable_words = vip_dict[top_vip_set]
                if debug:
                    print(f'VIPs: {top_vip_set}: {reduced_guessable_words}')

    # Optimization:
    # For all possible candidate words, find the letter who's presence or absence in them that most evenly bifrucates the list
    # Ideally, we find a letter that is contained only in 50% of the candidate words
    # As an optimization, only consider guesses that include such a letter
    pivot_scores = []
    if state != None:
        for letter in state.unhinted_letters:
            count_with_letter = len([word for word in candidate_words if letter in word])
            if count_with_letter == 0 or count_with_letter == candidate_count:
                continue
            score = abs(count_with_letter / candidate_count - 1/2)
            pivot_scores.append((letter, score))

    if len(pivot_scores) > 0:
        min_pivot_score = min([score for _, score in pivot_scores])
        pivot_letter = deterministic_random_first([word for word, score in pivot_scores if score == min_pivot_score])
        pivoted = [word for word in reduced_guessable_words if pivot_letter in word]
        if len(pivoted) > 0:
            reduced_guessable_words = pivoted
            if debug:
                print(f'pivot: {pivot_letter}: {round((1 - (min_pivot_score + 0.5)) * 100, 1)}% reduction guarantee')


    # Perform presence frequency analysis among the candidate words
    # Then find the guessable word that has the highest score
    positional_frequencies = positional_frequency(candidate_words)
    scores = []
    for word in reduced_guessable_words:
        score = 0
        for i, letter in enumerate(word):
            adjusted_positional_frequency = positional_frequencies[i][letter]
            if state != None:
                if state.green[i] == letter:
                    adjusted_positional_frequency = 0
                if letter in state.grey:
                    adjusted_positional_frequency = 0
                if letter in state.yellow:
                    adjusted_positional_frequency = adjusted_positional_frequency * 0.75
            score = score + adjusted_positional_frequency
        scores.append((word, score))
    return scores

def reduce_by_hard_hints(words, state: State):
    if state == None:
        return words

    return {word for word in words if validate_guess_hard_mode(word, state)}

def reduce_by_not_hard_hints(words, state: State):
    if state == None:
        return words

    return {word for word in words if
        # greys are not in the word
        all(letter not in word for letter in state.grey) and

        # yellows not only tell us that the letter is in the word, but also that it is NOT at the position of the yellow hint
        # this uses the negative cluse to filte out words with letters matching the yellow clues at the same position
        all(word[index] not in state.yellow_negative[index] for index in state.yellow_negative) and

        # use the count of a particular letter if it is known
        all(word.count(letter) == count for letter, count in state.known_letter_count.items())
    }

def reduce_by_duplicates(words, state: State):
    if state == None:
        return words

    return {word for word in words if
        # don't guess words that were previously guessed
        word not in state.guesses
    }

def reduce_by_only_unique_letters(words):
    # consider only words with unique letters iff doing so does not eliminate all candiate words
    reduced_words = words

    words_only_unique_letters = {word for word in words if len(word) == len(set(word))}
    if len(words_only_unique_letters) > 0:
        reduced_words = words_only_unique_letters

    return reduced_words


def reduce_by_plural(words):
    # consider only words that don't seem to be plural iff doing so does not eliminate all candiate words
    # possibly cheaty since this requires some knoledge of the answers compared to valid words, but a human could notice from play that answers are not plural
    reduced_words = words

    words_not_ending_with_s = {word for word in words if not word.endswith('s')}
    if len(words_not_ending_with_s) > 0:
        reduced_words = words_not_ending_with_s

    return reduced_words

def reduce_by_speculation(words, round_number, rounds):
    # reduce to words with all unique letters in first half of game
    words = reduce_by_only_unique_letters(words) if round_number <= rounds/2 else words
    # reduce to words that don't look plural in early rounds
    words = reduce_by_plural(words) if round_number <= 2 else words
    return words

def reduce_and_score(words, hard, state: State, round_number, rounds, debug):

    ### candidate words pure reduction
    #
    candidate_words = words
    candidate_words = reduce_by_duplicates(candidate_words, state)
    candidate_words = reduce_by_hard_hints(candidate_words, state)
    candidate_words = reduce_by_not_hard_hints(candidate_words, state)

    if debug:
        print(f'solver: {len(candidate_words)} candidate words left: {list(candidate_words)[:10]}')

    # Before speculative reduction:
    # if it's the last round - try to win instead of reducing the candidate words
    if round_number >= rounds:
        return deterministic_random_first(candidate_words)

    ### candidate words speculative reduction
    candidate_words = reduce_by_speculation(candidate_words, round_number, rounds)

    ### guessable words pure reduction
    guessable_words = words
    guessable_words = reduce_by_duplicates(guessable_words, state)
    guessable_words = reduce_by_hard_hints(guessable_words, state) if hard else guessable_words    

    ### guessable words speculative reduction
    guessable_words = reduce_by_speculation(guessable_words, round_number, rounds)
    
    return score(guessable_words, candidate_words, state, debug)


def best_word(words, hard, state, round_number, rounds, debug=False):

    scored = reduce_and_score(words, hard, state, round_number, rounds, debug)
    if isinstance(scored, str):
        return scored
    elif len(scored) == 0:
        return None
    
    max_score = max([score for _, score in scored])
    best_words = [word for word, score in scored if score == max_score]

    if debug:
        print(f'top words: {sorted(best_words)[:10]}')

    return deterministic_random_first(best_words)

if __name__ == '__main__':
    with open(VALID_FILENAME, 'r') as f:
        valid_words = {word.strip() for word in set(f)}

    for word in valid_words:
        if len(word) != WORD_LENGTH:
            print(f'all words must be length {WORD_LENGTH}')
            exit(1)
        for char in word:
            if char not in string.ascii_lowercase:
                print('all words must be lowercase')
                exit(1)

    state = None
    print(best_word(valid_words, state, 1, 6))