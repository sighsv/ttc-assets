#!/bin/bash
canonicalize

gen() {
    echo Generating $1.glb
    boardgen.sh "$@"
}

idgen() {
    name="$3"
    echo Generating $name.glb
    f=$(inkscape_png.sh "$1" "$4" "$2")
    shift
    shift
    shift
    shift
    cuboid.py -b -n "$name" -i "$f" -o "$name.glb" "$@"
    rm -f "$f"
}

gen "Tables Board" -x 52 -y 0.5 -z 39 -v 0.75 -c 6c5353ff
gen "Ludo Board" -x 40 -y 0.5 -z 40
gen "Game of the Goose" -x 40 -y 0.5 -z 28.5
gen "Leopard 14" -x 40 -y 0.5 -z 40
gen "Leopard 19" -x 40 -y 0.5 -z 40
gen "Leopard 29" -x 50 -y 0.5 -z 40
gen "Nine Men Morris" -x 28 -y 0.5 -z 28
gen "Zohn Ahl" -x 50 -y 0.5 -z 50 -c f7eae4ff
gen "O an quan" -x 35 -y 0.5 -z 15 -c c83737ff

idgen various.svg alquerque "Alquerque Board" w1024 -x 24.5 -y 0.5 -z 24.5
idgen various.svg alquerque_2tri "Alquerque 2 Triangles" h2048 -x 24.5 -y 0.5 -z 44.1
idgen various.svg alquerque_4tri "Alquerque 4 Triangles" w2048 -x 44.1 -y 0.5 -z 44.1
idgen various.svg agon "Agon Board" w1024 -x 51.629 -y 0.5 -z 46.55
idgen various.svg surakarta "Surakarta Board" w1024 -x 49.7 -y 0.5 -z 49.7
idgen various.svg fanorona "Fanorona Board" w1024 -x 24.5 -y 0.5 -z 44.1

outdir="$ASSETS/Myriad Boards/boards"
mkdir -p "$outdir"
mv -v *.glb "$outdir"
cp -v *.cfg "$outdir"
