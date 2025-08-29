#!/bin/sh
cd "$(dirname "$(realpath "$0")")"
gen="../boardgen.sh"

$gen "knaves" -x 54 -y 0.5 -z 54

outdir="../../assets/Knaves Hounds Hares/boards"
mkdir -p "$outdir"
mv -v *.glb "$outdir"
cp -v *.cfg "$outdir"