#! /bin/bash

grep -o . | sort | uniq -ic | sort -rn | sed -E 's/^[[:space:]]*//' | tr ' ' ','
