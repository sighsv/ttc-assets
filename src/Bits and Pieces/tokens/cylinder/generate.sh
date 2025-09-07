#!/bin/bash
canonicalize

outdir="$ASSETS/Bits and Pieces/tokens/cylinder"
mkdir -p "$outdir"

render() {
    echo Generating $3.png
    f="$(inkscape_png.sh "$1" w512 "$2")"
    mv "$f" "$outdir/$3.png"
}

render flippers.svg reversi reversi
render flippers.svg red_yellow red_yellow
render flippers.svg green_blue green_blue

render pokerchips.svg one "Poker Chip 1"
render pokerchips.svg five "Poker Chip 5"
render pokerchips.svg ten "Poker Chip 10"
render pokerchips.svg twenty_five "Poker Chip 25"
render pokerchips.svg one_hundred "Poker Chip 100"
render pokerchips.svg five_hundred "Poker Chip 500"
render pokerchips.svg one_thousand "Poker Chip 1000"
render pokerchips.svg five_thousand "Poker Chip 5000"
render pokerchips.svg ten_thousand "Poker Chip 10000"

cp -v *.cfg "$outdir"
