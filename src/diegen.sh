#!/bin/sh

temp=$(mktemp --suffix=.png)

here=$(realpath "$0")
heredir=$(dirname "$here")
cubegen="$heredir/cuboid.py"

svg="$1"
sid="$2"
name="$3"
shift
shift
shift
inkscape "$svg" --export-width=512 --export-type=png --export-filename="$temp" --export-id="$sid" 2>/dev/null
python3 "$cubegen" -b -s -i "$temp" -o "$name.glb" "$@" --name "$name"
rm -f "$temp"
