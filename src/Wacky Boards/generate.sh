#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Wacky Boards"
mkdir -p "$outdir/boards"

cp -v boards/*.glb "$outdir/boards"
cp -v boards/*.cfg "$outdir/boards"
