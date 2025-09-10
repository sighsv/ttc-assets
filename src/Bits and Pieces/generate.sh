#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Bits and Pieces"
mkdir -p "$outdir/pieces"

./pieces/generate.sh
mv -v pieces/*.glb "$outdir/pieces"
cp -v pieces/*.cfg "$outdir/pieces"

./dice/generate.sh

./tokens/cylinder/generate.sh
