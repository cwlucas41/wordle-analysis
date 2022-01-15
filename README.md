# wordle-analysis

Analaysis scripts and solver program for https://www.powerlanguage.co.uk/wordle/

## Wordle Solver
### Solver
`./wordle.py` or `./wordle.py --solve`

Picks a random word, runs the solving algorithm for it, and prints the result formatted like the real game.

By default, it guesses among all words accepted by real Wordle and chooses a random answer word among the special list of answer words that real Wordle has.

### Benchmark
`./wordle.py --benchmark` 

The benchmark tool runs the solver for every possible answer word and reports a summary of the results. It uses the same valid words and answer words list that the solver mode uses.

#### Current Results
```
Easy mode
Win rate: - 99.5%
Total games - 2315
Duration: 159.8s
2️⃣ : 24
3️⃣ : 151
4️⃣ : 221
5️⃣ : 53
6️⃣ : 1854
☠️ : 12
['aging', 'boozy', 'catch', 'eager', 'giver', 'maker', 'might', 'penny', 'queer', 'river', 'roger', 'rower']

Hard mode
Win rate: - 94.5%
Total games - 2315
Duration: 91.0s
2️⃣ : 42
3️⃣ : 423
4️⃣ : 915
5️⃣ : 580
6️⃣ : 227
☠️ : 128
['abate', 'aging', 'award', 'aware', 'baker', 'basis', 'batch', 'beefy', 'berry', 'boozy', 'boxer', 'brave', 'burly', 'cabby', 'caddy', 'chirp', 'clack', 'crawl', 'daddy', 'dried', 'droop', 'eager', 'eater', 'elude', 'embed', 'finch', 'floss', 'foyer', 'fussy', 'gayer', 'handy', 'hardy', 'hasty', 'hilly', 'hippy', 'hitch', 'holly', 'hound', 'hurry', 'hutch', 'irate', 'jaunt', 'jelly', 'later', 'ledge', 'leery', 'liner', 'lorry', 'louse', 'lumpy', 'maker', 'maybe', 'might', 'moral', 'mound', 'mouse', 'mover', 'mower', 'muddy', 'nerve', 'ninny', 'noose', 'otter', 'paddy', 'paler', 'paper', 'paste', 'patch', 'patty', 'penny', 'power', 'prism', 'prone', 'pushy', 'queer', 'ratty', 'reply', 'rider', 'riper', 'river', 'roger', 'roomy', 'rover', 'rower', 'rural', 'safer', 'saner', 'sappy', 'sassy', 'savvy', 'scram', 'serve', 'sever', 'sewer', 'share', 'shore', 'skill', 'smart', 'smear', 'smell', 'smite', 'snake', 'spare', 'spasm', 'spell', 'spree', 'stare', 'start', 'state', 'steer', 'store', 'stout', 'strap', 'tabby', 'table', 'tamer', 'taper', 'tatty', 'terse', 'tight', 'tithe', 'toddy', 'trait', 'tripe', 'unwed', 'verve', 'wager', 'water']
```

### Play
`./wordle.py --play`

Like solver mode, but prompts for the guess word rather than running the solving algorithm.

### Help Info:
```
usage: wordle.py [-h] [-p | -s | -b] [-r num_rounds] [-a word] [-H] [-d] [--answer-words-file path] [--valid-words-file path]

optional arguments:
  -h, --help            show this help message and exit
  -p, --play            use "play" mode
  -s, --solve           use "solve" mode (default)
  -b, --benchmark       use "benchmark" mode
  -r num_rounds, --rounds num_rounds
                        number of rounds (default="6")
  -a word, --answer word
                        sets the answer word - useful for debugging a specific case. Ignored in benchmark mode
  -H, --hard            enable hard mode (any revealed hints must be used in subsequent guesses). Ignored in benchmark mode.
  -d, --debug           print extra output for debugging
  --answer-words-file path
                        file with all possible answers (default="words/answers.txt")
  --valid-words-file path
                        file with all accepted words (default="words/valid.txt")
```

## Manual scripts

Used to get data for https://gist.github.com/cwlucas41/6ce8404c5940cdca632d55abcff4f526

### Usage

#### Get the raw frequency of each letter in a set of words
```
cat words/valid.txt | ./analysis-scripts/letter-count.sh
```

#### Get the presence rate of each letter
```
cat words/valid.txt | ./analysis-scripts/presence-count.sh
```

#### Get the contingent frequencies of each letter
```
cat words/valid.txt | ./analysis-scripts/letter-contingency.sh
```
