#!/bin/sh

# Automatically timestamp the aligntoreveal.md file

request() {
    temp=$(mktemp)
    openssl ts -query -data "$1" -cert -sha256 -no_nonce -out "$temp"
    curl "$2" -H 'Content-Type: application/timestamp-query' -s -S \
        --data-binary "@$temp" -o "$3"
    rm "$temp"
}

input="aligntoreveal.md"
outdir="aligntoreveal.timestamp"

mkdir -p "$outdir"

while read authority; do
    echo $authority
    outname=$(echo "$authority" | sed -E 's/.*\/\/([a-z0-9.]+)\/.*/\1/')
    request "$input" "$authority" "$outdir/$outname.tsr"
done < authorities
