# wordle-analysis

## Solver

```
Easy mode
Win rate: - 99.3%
Total games - 2315
Duration: 133.0s
2️⃣ : 25
3️⃣ : 278
4️⃣ : 911
5️⃣ : 805
6️⃣ : 280
☠️ : 16
['booby', 'boxer', 'daddy', 'eager', 'eater', 'elude', 'nanny', 'penny', 'putty', 'queer', 'rural', 'sappy', 'seven', 'tight', 'wafer', 'waver']

Hard mode
Win rate: - 94.4%
Total games - 2315
Duration: 82.3s
2️⃣ : 42
3️⃣ : 441
4️⃣ : 898
5️⃣ : 584
6️⃣ : 220
☠️ : 130
['aging', 'award', 'baker', 'basis', 'batch', 'beefy', 'boozy', 'boxer', 'brave', 'burly', 'cabby', 'chirp', 'clack', 'crawl', 'daddy', 'dried', 'drool', 'droop', 'eager', 'eater', 'elude', 'embed', 'finch', 'fixer', 'floss', 'foyer', 'furry', 'fussy', 'gayer', 'handy', 'hardy', 'harem', 'harry', 'hasty', 'hilly', 'hippy', 'hitch', 'holly', 'hound', 'hurry', 'hutch', 'irate', 'jaunt', 'jelly', 'joker', 'later', 'ledge', 'leery', 'liner', 'lorry', 'louse', 'lumpy', 'maker', 'maybe', 'merry', 'might', 'moose', 'moral', 'mound', 'mouse', 'mover', 'mower', 'muddy', 'nanny', 'nerve', 'ninny', 'noisy', 'noose', 'otter', 'paddy', 'paler', 'paper', 'paste', 'patch', 'patty', 'penny', 'power', 'prism', 'prone', 'pushy', 'queer', 'ratty', 'reply', 'rider', 'riper', 'roomy', 'rover', 'rower', 'rural', 'safer', 'saner', 'sappy', 'sassy', 'savvy', 'scram', 'serum', 'sewer', 'share', 'shore', 'skill', 'smart', 'smear', 'smell', 'smite', 'spare', 'spell', 'stare', 'start', 'state', 'steer', 'store', 'stout', 'strap', 'tabby', 'table', 'tamer', 'taper', 'tatty', 'terse', 'tight', 'tithe', 'toddy', 'trait', 'tripe', 'unwed', 'verve', 'wafer', 'wager', 'water', 'willy']
```

## Manual scripts

Used to get data for https://gist.github.com/cwlucas41/6ce8404c5940cdca632d55abcff4f526

# Usage

## Get the raw frequency of each letter in a set of words
```
cat words/valid.txt | ./analysis-scripts/letter-count.sh
```

## Get the presence rate of each letter
```
cat words/valid.txt | ./analysis-scripts/presence-count.sh
```

## Get the contingent frequencies of each letter
```
cat words/valid.txt | ./analysis-scripts/letter-contingency.sh
```
