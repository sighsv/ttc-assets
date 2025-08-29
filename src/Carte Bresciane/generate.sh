#!/bin/bash
cd "$(dirname "$(realpath "$0")")"
inkscape source.svg --export-width=10000 --export-type=png --export-filename=source.png 2>/dev/null
mogrify -trim +repage source.png
convert source.png -crop 14x4@ -trim +repage carte-%02d.png
rm source.png
mogrify -gravity center -crop 654x1368+0+0 +repage carte-*.png

outdir="../../assets/Carte Bresciane/cards"

suits=(Denari Bastoni Coppe Spade)
values=(Asso Due Tre Quattro Cinque Sei Sette Otto Nove Dieci Fante Cavallo Re Retro)

value=0
suit=0

mkdir -p "$outdir"
cp -v *.cfg "$outdir/"

for i in carte-*.png; do
    mv -v "$i" "$outdir/${values[$value]} di ${suits[$suit]}.png"
    value=$(( (value + 1) % 14 ))
    if [ $value -eq 0 ]; then
        suit=$(( suit + 1 ))
    fi
done
