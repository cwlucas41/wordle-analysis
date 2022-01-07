import string
import re

from wordle_common import State

# TODO: remove?
WORD_LENGTH = 5

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
    positional_frequencies = positional_frequency(words)

    scores = []
    for word in words:
        score = 0
        for i, letter in enumerate(word):
            # better idea - contingencies among word corpus

            times_letter_seen_so_far = word[:i+1].count(letter)
            factor = 1 / 10 ** (times_letter_seen_so_far - 1)

            score = score + positional_frequencies[i][letter] * factor
        scores.append((word, score))
    
    return sorted(scores, key=lambda score: score[1])

def reduce_and_score(words, state: State):
    reduced_words = words
    if state != None:
        green_yellow = [letter for letter in state.green + state.yellow if letter != '.']

        reduced_words = [word for word in words if
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
        ]

    if len(reduced_words) > 0:
        val = score(reduced_words)
        return val
    else:
        return []

def best_word(words, state):
    scored = reduce_and_score(words, state)
    if len(scored) > 0:
        return scored.pop()[0]
    else:
        return None

if __name__ == '__main__':
    WORD_FILENAME = 'valid.txt'

    with open(WORD_FILENAME, 'r') as f:
        valid_words = {word.strip() for word in set(f)}

    for word in valid_words:
        if len(word) != WORD_LENGTH:
            print(f'all words must be length {WORD_LENGTH}')
            exit(1)
        for char in word:
            if char not in string.ascii_lowercase:
                print('all words must be lowercase')
                exit(1)

    state = State(green=['g', 'l', 'i', '.', 'e'], yellow=[], grey={'c', 'o', 'k', 'r', 'a', 'n', 'b', 'u', 's', 'd'}, yellow_negative={3: {'e', 'l', 'i'}}, guesses={'guile', 'bonie', 'glike', 'cares', 'glide'})
    print(reduce_and_score(valid_words, state))
    print(best_word(valid_words, state))