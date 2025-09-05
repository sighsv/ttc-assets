#!/bin/bash
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Smith-Waite-Rider Tarot/cards"
mkdir -p "$outdir"

rectify() {
    src="$1"
    shift
    ../rectify.py "$src" "$outdir/$(basename "$src")" "$@"
}

for f in raw/*.jpg; do
    rectify "$f" --margins 10 25 25 10
done

# Outliers
rectify raw/Cups01.jpg --margins 10 25 7 10
rectify raw/RWS_Tarot_00_Fool.jpg --margins 10 25 25 25
# Noise removal fails on this one
rectify raw/RWS_Tarot_02_High_Priestess.jpg -m 10 25 25 5 -r 0.5 0.5 0.5 0.75

# overlay and resize
for f in "$outdir"/*.jpg; do
    # resize the back face
    if [[ "$f" == *"Roses_and_Lilies"* ]]; then
        mogrify -resize 1015x1775 "$f"
    fi
    composite -gravity center "$f" blanked.jpg "$f"
    mogrify -resize 500x-1 "$f"
done

# rename
source_suits=(Cups Pents Swords Wands)
suits=(Cups Pentacles Swords Wands)
values=(Ace Two Three Four Five Six Seven Eight Nine Ten Page Knight Queen King)

mv "$outdir/Waite–Smith_Tarot_Roses_and_Lilies_cropped.jpg" "$outdir/Back.jpg"

i=0
for f in "$outdir"/RWS_Tarot*.jpg; do
    mv "$f" "$outdir/Major $i.jpg"
    i=$(( i + 1 ))
done

suit=0
while [ $suit -lt 4 ]; do
    value=0
    while [ $value -lt 14 ]; do
        source=$(printf %s%02d.jpg ${source_suits[$suit]} $(( value + 1 )))
        dest="${values[$value]} of ${suits[$suit]}.jpg"
        mv "$outdir/$source" "$outdir/$dest"
        value=$(( value + 1 ))
    done
    suit=$(( suit + 1 ))
done

cp -v *.cfg "$outdir/"
