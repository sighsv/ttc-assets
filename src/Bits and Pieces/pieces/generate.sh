#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

../../normal.py -o rings.png -x 256 -y 256 -s 15 \
    -f 'lambda x, y: math.fabs(math.cos(22 * math.sqrt(x**2 + y**2)))'
../../cylinder.py -r 1.4 -y 0.635 -n rings.png -c -M 0 -R 0.8 \
    -N Checker -o Checker.glb
rm rings.png

../../blender_gltf.sh "Pawn - Humanoid.blend"
../../blender_gltf.sh "Pawn - Wide Base.blend"
../../blender_gltf.sh Bead.blend
