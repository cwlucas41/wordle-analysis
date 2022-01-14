# wordle-analysis

## Solver

```
Easy mode
Win rate: - 96.2%
Total games - 2315
Duration: 105.7s
2️⃣ : 25
3️⃣ : 144
4️⃣ : 207
5️⃣ : 36
6️⃣ : 1814
☠️ : 89
['aware', 'boozy', 'boxer', 'brave', 'breed', 'broth', 'butch', 'caddy', 'candy', 'caper', 'cater', 'chart', 'chirp', 'crave', 'creed', 'curly', 'dizzy', 'drone', 'embed', 'finch', 'floss', 'funny', 'furry', 'fussy', 'gazer', 'gloss', 'gripe', 'level', 'light', 'llama', 'lumpy', 'maker', 'marry', 'merry', 'might', 'moral', 'mouse', 'mural', 'nanny', 'nerve', 'ninny', 'otter', 'paddy', 'paper', 'paste', 'patch', 'penny', 'piper', 'poker', 'pound', 'power', 'pried', 'prove', 'puffy', 'pushy', 'rebel', 'refit', 'rehab', 'roomy', 'rover', 'safer', 'savvy', 'scarf', 'sheer', 'smack', 'spare', 'spell', 'stare', 'start', 'state', 'steer', 'store', 'swell', 'table', 'taint', 'toddy', 'tramp', 'troop', 'tweet', 'vaunt', 'wafer', 'wager', 'watch', 'water', 'waver', 'wedge', 'wight', 'witch', 'woody']

Hard mode
Win rate: - 94.6%
Total games - 2315
Duration: 92.9s
2️⃣ : 38
3️⃣ : 406
4️⃣ : 915
5️⃣ : 606
6️⃣ : 224
☠️ : 126
['badge', 'batch', 'batty', 'bobby', 'booby', 'booze', 'boozy', 'boxer', 'brave', 'breed', 'bushy', 'cabal', 'cabby', 'caddy', 'candy', 'caper', 'caste', 'cater', 'catty', 'chaos', 'chart', 'chirp', 'crave', 'creed', 'cried', 'curly', 'drone', 'drool', 'droop', 'eager', 'eater', 'eying', 'foggy', 'forge', 'foyer', 'froth', 'fudge', 'furry', 'fussy', 'gayer', 'goner', 'goofy', 'goose', 'gorge', 'grill', 'guard', 'hasty', 'hatch', 'hilly', 'hippy', 'hound', 'hover', 'hutch', 'irate', 'jelly', 'jolly', 'koala', 'lager', 'ledge', 'liner', 'lorry', 'lying', 'maker', 'mercy', 'merry', 'minty', 'moral', 'mouse', 'mover', 'nanny', 'ninny', 'noisy', 'noose', 'otter', 'paddy', 'paper', 'penny', 'piper', 'plaza', 'poker', 'polar', 'pound', 'probe', 'pushy', 'queer', 'rebel', 'rehab', 'rider', 'river', 'rower', 'safer', 'saner', 'share', 'slack', 'smart', 'smell', 'snare', 'spear', 'spell', 'stage', 'stare', 'start', 'steer', 'store', 'strap', 'stuff', 'sweet', 'swore', 'table', 'taper', 'taunt', 'toddy', 'touch', 'tower', 'unfed', 'vault', 'vaunt', 'verse', 'wafer', 'wager', 'water', 'waver', 'wedge', 'whack', 'wight', 'willy']

Easy only misses - 42
['aware', 'broth', 'butch', 'dizzy', 'embed', 'finch', 'floss', 'funny', 'gazer', 'gloss', 'gripe', 'level', 'light', 'llama', 'lumpy', 'marry', 'might', 'mural', 'nerve', 'paste', 'patch', 'power', 'pried', 'prove', 'puffy', 'refit', 'roomy', 'rover', 'savvy', 'scarf', 'sheer', 'smack', 'spare', 'state', 'swell', 'taint', 'tramp', 'troop', 'tweet', 'watch', 'witch', 'woody']

Hard only misses - 79
['badge', 'batch', 'batty', 'bobby', 'booby', 'booze', 'bushy', 'cabal', 'cabby', 'caste', 'catty', 'chaos', 'cried', 'drool', 'droop', 'eager', 'eater', 'eying', 'foggy', 'forge', 'foyer', 'froth', 'fudge', 'gayer', 'goner', 'goofy', 'goose', 'gorge', 'grill', 'guard', 'hasty', 'hatch', 'hilly', 'hippy', 'hound', 'hover', 'hutch', 'irate', 'jelly', 'jolly', 'koala', 'lager', 'ledge', 'liner', 'lorry', 'lying', 'mercy', 'minty', 'mover', 'noisy', 'noose', 'plaza', 'polar', 'probe', 'queer', 'rider', 'river', 'rower', 'saner', 'share', 'slack', 'smart', 'smell', 'snare', 'spear', 'stage', 'strap', 'stuff', 'sweet', 'swore', 'taper', 'taunt', 'touch', 'tower', 'unfed', 'vault', 'verse', 'whack', 'willy']

Easy and Hard misses - 47
['boozy', 'boxer', 'brave', 'breed', 'caddy', 'candy', 'caper', 'cater', 'chart', 'chirp', 'crave', 'creed', 'curly', 'drone', 'furry', 'fussy', 'maker', 'merry', 'moral', 'mouse', 'nanny', 'ninny', 'otter', 'paddy', 'paper', 'penny', 'piper', 'poker', 'pound', 'pushy', 'rebel', 'rehab', 'safer', 'spell', 'stare', 'start', 'steer', 'store', 'table', 'toddy', 'vaunt', 'wafer', 'wager', 'water', 'waver', 'wedge', 'wight']
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
