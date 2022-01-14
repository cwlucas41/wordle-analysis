#!/usr/bin/env python3

import string

from zlib import crc32

from common import WORD_LENGTH, VALID_FILENAME
from state import State, validate_guess_hard_mode

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

def score(guessable_words, candidate_words, state: State):
    positional_frequencies = positional_frequency(candidate_words)

    scores = []
    for word in guessable_words:
        score = 0
        for i, letter in enumerate(word):
            adjusted_positional_frequency = positional_frequencies[i][letter]
            if state != None:
                if state.green[i] == letter:
                    adjusted_positional_frequency = 0
                if letter in state.grey:
                    adjusted_positional_frequency = 0
            score = score + adjusted_positional_frequency
        scores.append((word, score))
    return scores

# def score(words):
#     scores = []
#     for word in words:
#         common_letter_count = [len(set(w) & set(word)) for w in words if w != word]
#         positive_common_letter_count = [letter_count for letter_count in common_letter_count if letter_count > 0]
#         scores.append((word, sum(positive_common_letter_count)))
#     # print(f"done! - {len(words)}")
#     return scores

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
        print(f'solver: {len(candidate_words)} candidate words left')

    # Before speculative reduction:
    # if it's the last round - try to win instead of reducing the candidate words
    # start guessing if the candidate words are reduced enough for us to exhaustively guess in time
    if round_number >= rounds: #or len(candidate_words) <= rounds - round_number:
        return score(candidate_words, candidate_words, state)

    ### candidate words speculative reduction
    candidate_words = reduce_by_speculation(candidate_words, round_number, rounds)

    ### guessable words pure reduction
    guessable_words = words
    guessable_words = reduce_by_duplicates(guessable_words, state)
    guessable_words = reduce_by_hard_hints(guessable_words, state) if hard else guessable_words    

    ### guessable words speculative reduction
    guessable_words = reduce_by_speculation(guessable_words, round_number, rounds)

    
    if debug:
        print(f'solver: {len(guessable_words)} guessable words left')
    
    return score(guessable_words, candidate_words, state)


def best_word(words, hard, state, round_number, rounds, debug=False):

    scored = reduce_and_score(words, hard, state, round_number, rounds, debug)
    if len(scored) == 0:
        return None

    if debug:
        print(f'top words: {scored[:20]}')
    
    max_score = max([score for _, score in scored])
    best_words = [word for word, score in scored if score == max_score]

    # sorting makes best word deterministic if index is deterministic
    # sorting by hashed value effectively randomizes the order of words to avoid alphabetical bias 
    sorted_best_words = sorted(best_words, key=lambda x: crc32(x.encode()))

    return sorted_best_words[0]

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