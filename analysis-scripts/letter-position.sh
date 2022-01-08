#! /bin/bash

words="$(cat /dev/stdin)"
wordCount=$(echo "$words" | wc -l)

header=("Letter\Index")
for index in {0..4}
do
    header+=("$index")
done
echo $(IFS=, ; echo "${header[*]}")

regexPrefixes=("^" "^." "^.." "^..." "^....")
for letter in {a..z}
do
    counts=()
    for regexPrefix in ${regexPrefixes[@]}
    do
        count=$(echo "$words" | grep "${regexPrefix}${letter}" | wc -l)
        counts+=("$count")
    done

    line=()
    for count in ${counts[@]}
    do
        value=$(awk "BEGIN { OFMT = \"%0.4f\"; print ( $count / $wordCount ) }")
        line+=($value)
    done

    echo $(IFS=, ; echo "$letter,${line[*]}")
done
