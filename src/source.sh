#!/bin/bash
export ASSETS="$(realpath ../assets)"
export PATH="$(realpath .):$PATH"

function canonicalize() {
    cd "$(dirname "$(realpath "$0")")"
}

export -f canonicalize

