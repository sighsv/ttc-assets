#!/bin/sh
here=$(dirname "$(realpath "$0")")
blender "$1" --background --python "$here/blender_gltf.py" -- "${1%.*}.glb"
