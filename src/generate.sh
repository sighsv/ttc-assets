#!/bin/sh

for d in */generate.sh; do
    echo $d
    "$d"
done
