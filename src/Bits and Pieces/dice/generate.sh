#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

compile() {
    oid="$1"
    ofile="$2"
    shift
    shift
    echo Generating $ofile.glb
    inkscape dice.svg --export-width=512 --export-type=png --export-filename="$oid.png" --export-id="$oid" 2>/dev/null
    ../../cuboid.py -b -s -i "$oid.png" -o "$ofile.glb" "$@" --name "$ofile.material"
    rm "$oid.png"
}

d="-x 1.6 -y 1.6 -z 1.6"

compile perfect_die 'Perfect Die' -x 1.9685 -y 1.9685 -z 1.9685

compile doubling_cube 'Doubling Cube' $d
compile sicherman_low 'Sicherman Die Low' $d
compile sicherman_high 'Sicherman Die High' $d
compile binary_die 'Binary Die' $d
compile binary_die_red 'Binary Die Red' $d
compile binary_die_blue 'Binary Die Blue' $d
compile average_die 'Average Die' $d
compile fudge_die 'Fudge Die' $d
compile cowrie_even 'Cowrie Die Even' $d
