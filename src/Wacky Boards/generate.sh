#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Wacky Boards"
mkdir -p "$outdir/boards"

inkscape crokinole_board.svg --export-width=2048 --export-type=png --export-filename=crokinole_board.png 2>/dev/null
../blender_gltf.sh "Crokinole Board.blend"

inkscape pachisi.svg --export-width=2048 --export-type=png --export-filename=pachisi.png 2>/dev/null
../blender_gltf.sh "Pachisi Board.blend"

rm *.png

mv -v *.glb "$outdir/boards"
cp -v *.cfg "$outdir/boards"
