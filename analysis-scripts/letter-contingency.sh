#! /bin/bash

#! /bin/bash
words="$(cat /dev/stdin)"

header=("Given\Contingent")
for letter in {a..z}
do
    header+=("$letter")
done
echo $(IFS=, ; echo "${header[*]}")

for givenLetter in {a..z}
do
    # find words with the given letter and then remove the first occurence of the letter from the relevant word
    # this is so when the contingent letter is the same as the given letter it is matching a different instance of the letter
    relevantWords=$(echo "$words" | grep "$givenLetter" | sed "s/${givenLetter}//")
    
    line=()
    for contingentLetter in {a..z}
    do
        count=$(echo "$relevantWords" | grep "$contingentLetter" | wc -l)
        line+=("$count")
    done
    echo $(IFS=, ; echo "${givenLetter},${line[*]}")
done
