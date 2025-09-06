#!/bin/sh

temp=$(mktemp --suffix=.png)

here=$(realpath "$0")
heredir=$(dirname "$here")
boardgen="$heredir/cuboid.py"

name="$1"
inkscape "$name.svg" --export-width=2048 --export-type=png --export-filename="$temp" 2>/dev/null
shift
python3 "$boardgen" -n "$name" -i "$temp" "$@" --glb -o "$name.glb"
rm -rf "$temp"
