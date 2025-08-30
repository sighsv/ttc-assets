#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Tables"
mkdir -p "$outdir"

../blender_gltf.sh fancy_table.blend

mv *.glb "$outdir"
cp *.cfg "$outdir"
