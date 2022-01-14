# wordle-analysis

## Solver

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
