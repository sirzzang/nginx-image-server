# !/usr/bin/bash
BASE_DIR="/home/eraser/nginx/images"
for a in $(seq -w 0 99)
do
    for b in $(seq -w 0 99)
    do
        for c in $(seq -w 0 99)
        do
            SUB_DIR="$a/$b/$c"
            mkdir -p "$BASE_DIR/$SUB_DIR"
        done
        echo "----- creating $a/$b/ directory done. -----"
    done
    echo "----- creating $a/ directory done. -----"
done