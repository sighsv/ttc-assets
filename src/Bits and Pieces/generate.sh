#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Bits and Pieces"
mkdir -p "$outdir/pieces"
mkdir -p "$outdir/dice/d6"

./pieces/generate.sh
mv -v pieces/*.glb "$outdir/pieces"
cp -v pieces/*.cfg "$outdir/pieces"

./dice/generate.sh
mv -v dice/*.glb "$outdir/dice/d6"
cp -v dice/*.cfg "$outdir/dice/d6"

"./tokens/cylinder/generate.sh"
