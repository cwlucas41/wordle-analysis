#!/usr/bin/env python3

import string
import re

from wordle_common import WORD_LENGTH, VALID_FILENAME, State

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

def words_with_unique_letters(words):
    return {word for word in words if len(word) == len(set(word))}

def score(words):
    if len(words) == 0:
        return []

    positional_frequencies = positional_frequency(words)

    scores = []
    for word in words:
        score = 0
        for i, letter in enumerate(word):
            # TODO: contingencies among word corpus
            factor = 1

            score = score + positional_frequencies[i][letter] * factor
        scores.append((word, score))
    
    return scores

def reduce_by_state(words, state: State):
    if state == None:
        return words

    green_yellow = [letter for letter in state.green + state.yellow if letter != '.']

    # reducing by state is absolute and will not remove all words - else bug
    return {word for word in words if
        # greens match positionally
        re.compile(f'^{"".join(state.green)}$').match(word) and

        # yellows appear somewhere in the word
        all(letter in word for letter in state.yellow) and

        # yellows might match to green slots, but if there is a green and yellow then we actually have a hint of duplicate letters
        # this ensures the count of the letter in the word is at least the number of hints we have for the letter
        all(word.count(letter) >= green_yellow.count(letter) for letter in green_yellow) and

        # greys are not in the word
        all(letter not in word for letter in state.grey) and

        # yellows not only tell us that the letter is in the word, but also that it is NOT at the position of the yellow hint
        # this uses the negative cluse to filte out words with letters matching the yellow clues at the same position
        all(word[index] not in state.yellow_negative[index] for index in state.yellow_negative) and

        # don't guess words that were previously guessed!
        word not in state.guesses
    }

def reduce_by_only_unique_letters(words, round_number, rounds):
    # consider only words with unique letters in early rounds iff doing so does not eliminate all candiate words
    reduced_words = words
    if round_number <= rounds / 2:
        words_only_unique_letters = {word for word in words if len(word) == len(set(word))}
        if len(words_only_unique_letters) > 0:
            reduced_words = words_only_unique_letters

    return reduced_words


def reduce_by_plural(words, round_number, rounds):
    # consider only words that don't seem to be plural in early rounds iff doing so does not eliminate all candiate words
    # possibly cheaty since this requires some knoledge of the answers compared to valid words, but a human could notice from play that answers are not plural
    reduced_words = words
    if round_number <= 2:
        words_not_ending_with_s = {word for word in words if not word.endswith('s')}
        if len(words_not_ending_with_s) > 0:
            reduced_words = words_not_ending_with_s

    return reduced_words

def reduce_and_score(words, state: State, round_number, rounds):
    # TODO: this always uses hard mode rules, but it will be advantageous to get information about more letters rather than repeating known information

    reduced_words = reduce_by_state(words, state)
    reduced_words = reduce_by_only_unique_letters(reduced_words, round_number, rounds)
    reduced_words = reduce_by_plural(reduced_words, round_number, rounds)
    
    return score(reduced_words)


def best_word(words, state, round_number, rounds):
    scored = reduce_and_score(words, state, round_number, rounds)
    if len(scored) == 0:
        return None

    # print(sorted(scored, key=lambda x: x[1]))
    max_score = max([score for _, score in scored])
    best_words = [word for word, score in scored if score == max_score]

    # sorting makes best word deterministic
    return sorted(best_words)[0]

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