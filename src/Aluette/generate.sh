#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Aluette/cards"
mkdir -p "$outdir"

clean_name() {
    echo "$1" | cut -d- -f5 | cut -c2- | tr _ ' '
}

for f in raw/*.jpg; do
    outfile="$(clean_name $(basename "$f"))"
    ../rectify.py "$f" "$outdir/$outfile" --margins 25 25 30 25 --backoff 5
    composite -gravity center "$outdir/$outfile" blanked.jpg "$outdir/$outfile"
    mogrify -resize 500x-1 "$outdir/$outfile"
done

cp -v *.cfg "$outdir"
