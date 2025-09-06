#!/bin/bash

canonicalize

for d in */generate.sh; do
    echo $d
    "$d"
done
