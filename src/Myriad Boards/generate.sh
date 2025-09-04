#!/bin/sh
cd "$(dirname "$(realpath "$0")")"
gen="../boardgen.sh"

$gen "Tables Board" -x 52 -y 0.5 -z 39 -v 0.75 -c 6c5353ff
$gen "Ludo Board" -x 40 -y 0.5 -z 40
$gen "Game of the Goose" -x 40 -y 0.5 -z 28.5
$gen "Leopard 14" -x 40 -y 0.5 -z 40
$gen "Leopard 19" -x 40 -y 0.5 -z 40
$gen "Leopard 29" -x 50 -y 0.5 -z 40
$gen "Nine Men Morris" -x 28 -y 0.5 -z 28
$gen "Zohn Ahl" -x 50 -y 0.5 -z 50 -c f7eae4ff
$gen "O an quan" -x 35 -y 0.5 -z 15 -c c83737ff

outdir="../../assets/Myriad Boards/boards"
mkdir -p "$outdir"
mv -v *.glb "$outdir"
cp -v *.cfg "$outdir"
