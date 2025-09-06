#!/bin/bash

canonicalize
outdir="$ASSETS/Kriegsspiel/dice/d6"

compile() {
    echo Generating $2.glb
    diegen.sh dice.svg "$@"
}

d="--tr 1 -x 1.6 -y 1.6 -z 1.6"

compile die_i '1824 Kriegsspiel Die I' $d
compile die_ii '1824 Kriegsspiel Die II' $d
compile die_iii '1824 Kriegsspiel Die III' $d
compile die_iv '1824 Kriegsspiel Die IV' $d
compile die_v '1824 Kriegsspiel Die V' $d

compile die_iii_variant '1824 Kriegsspiel Die III Variant' $d
compile die_iii_table '1824 Kriegsspiel Die III Table' $d

compile die_i_1828 '1828 Kriegsspiel Die I' $d
compile die_ii_1828 '1828 Kriegsspiel Die II' $d
compile die_iii_1828 '1828 Kriegsspiel Die III' $d
compile die_iv_1828 '1828 Kriegsspiel Die IV' $d
compile die_v_1828 '1828 Kriegsspiel Die V' $d
compile die_vi_1828 '1828 Kriegsspiel Die VI' $d
compile die_vii.i_1828 '1828 Kriegsspiel Die VII I' $d
compile die_vii.ii_1828 '1828 Kriegsspiel Die VII II' $d
compile die_vii.iii_1828 '1828 Kriegsspiel Die VII III' $d

mkdir -p "$outdir"
cp -v *.cfg "$outdir"
mv -v *.glb "$outdir"
