#!/bin/sh

for d in */; do
    echo $d
    "./$d/generate.sh"
done
