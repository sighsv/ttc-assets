#!/bin/sh
cd "$(dirname "$(realpath "$0")")"

outdir="../../assets/Kriegsspiel"

compile() {
    echo Generating $2.glb
    ../diegen.sh dice.svg "$@"
}

d="-x 1.6 -y 1.6 -z 1.6"

compile die_i 'Kriegsspiel Die I' $d
compile die_ii 'Kriegsspiel Die II' $d
compile die_iii 'Kriegsspiel Die III' $d
compile die_iv 'Kriegsspiel Die IV' $d
compile die_v 'Kriegsspiel Die V' $d

mkdir -p "$outdir/dice/d6"
cp -v *.cfg "$outdir/dice/d6"
mv -v *.glb "$outdir/dice/d6"
