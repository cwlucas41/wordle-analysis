#! /bin/bash
words="$(cat /dev/stdin)"
out=$(mktemp)

for letter in {a..z}
do
    wordCount=$(echo "$words" | grep "$letter" | wc -l)
    echo "${wordCount},${letter}" >> "$out"
done

cat "$out" | sort -rn
rm -f "$out"
