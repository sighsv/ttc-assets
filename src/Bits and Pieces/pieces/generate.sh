#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

../../blender_gltf.sh Checker.blend
../../blender_gltf.sh "Pawn - Humanoid.blend"
../../blender_gltf.sh "Pawn - Wide Base.blend"
