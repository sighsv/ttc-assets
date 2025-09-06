#!/bin/bash

canonicalize
outdir="$ASSETS/Kriegsspiel/pieces"

compile() {
    name="$2"
    echo Generating $name.glb
    f=$(inkscape_png.sh rulers.svg "$3" "$1")
    shift
    shift
    shift
    cuboid.py -b -n "$name" -i "$f" -o "$name.glb" "$@"
    rm -f "$f"
}

compile artillery_ruler_7500 'Artillery Ruler' h1024 --tr 1 -x 3.515 -y 0.25 -z 20.015
compile travel_ruler_7500 'Travel Ruler' w512 --tr 1 -x 9.015 -y 0.25 -z 5.321

mkdir -p "$outdir"
cp -v *.cfg "$outdir"
mv -v *.glb "$outdir"
