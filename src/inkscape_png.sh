#!/bin/bash

svg="$1"
dimension="$2"

d="${dimension:0:1}"

if [ "$d" = "w" ]; then
    esize="--export-width=${dimension:1}"
elif [ "$d" = "h" ]; then
    esize="--export-height=${dimension:1}"
else
    esize="--export-width=$dimension"
fi

if [ -n "$3" ]; then
    eid="--export-id=$3"
fi

temp=$(mktemp --suffix=.png)

inkscape "$svg" "$esize" --export-type=png --export-filename="$temp" "$eid" 2>/dev/null >/dev/null

echo "$temp"
