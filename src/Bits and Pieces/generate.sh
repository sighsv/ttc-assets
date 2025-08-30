#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Bits and Pieces"
mkdir -p "$outdir/pieces"
mkdir -p "$outdir/dice/d6"

./pieces/generate.sh
mv -v pieces/*.glb "$outdir/pieces"
cp -v pieces/*.cfg "$outdir/pieces"

./dice/d6/generate.sh
mv -v dice/d6/*.glb "$outdir/dice/d6"
cp -v dice/d6/*.cfg "$outdir/dice/d6"

"./tokens/cylinder/generate.sh"
