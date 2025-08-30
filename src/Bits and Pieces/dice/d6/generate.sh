#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

svg_render() {
    inkscape "$1.svg" --export-width=512 --export-type=png --export-filename="$1.png" 2>/dev/null
}

svg_render doubling
../../../blender_gltf.sh "Doubling Cube.blend"
rm doubling.png
