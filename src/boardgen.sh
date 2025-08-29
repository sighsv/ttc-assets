#!/bin/sh

temp=$(mktemp)

here=$(realpath "$0")
heredir=$(dirname "$here")
boardgen="$heredir/boardgen.py"

name="$1"
inkscape "$name.svg" --export-width=2048 --export-type=png --export-filename="$temp.png" 2>/dev/null
shift
python3 "$boardgen" -n "$name" -i "$temp.png" "$@" --glb -o "$name.glb"
rm -rf "$temp.png"
