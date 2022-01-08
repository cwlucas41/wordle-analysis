# wordle-analysis

Used to get data for https://gist.github.com/cwlucas41/6ce8404c5940cdca632d55abcff4f526

# Usage

## Get the raw frequency of each letter in a set of words
```
cat words/valid.txt | ./letter-count.sh
```

## Get the presence rate of each letter
```
cat words/valid.txt | ./presence-count.sh
```

## Get the contingent frequencies of each letter
```
cat words/valid.txt | ./letter-contingency.sh
```
