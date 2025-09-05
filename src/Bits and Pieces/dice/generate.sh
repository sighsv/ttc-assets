#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

compile() {
    echo Generating $2.glb
    ../../diegen.sh dice.svg "$@"
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
