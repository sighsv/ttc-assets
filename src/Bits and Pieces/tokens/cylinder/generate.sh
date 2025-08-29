#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../../../assets/Bits and Pieces/tokens/cylinder"
mkdir -p "$outdir"

render() {
    inkscape flippers.svg --export-width=512 --export-type=png --export-filename="$outdir/$1.png" --export-id="$1" 2>/dev/null
}

render reversi
render red_yellow
render green_blue

cp -v *.cfg "$outdir"
