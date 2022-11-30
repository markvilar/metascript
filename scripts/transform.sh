#!/usr/bin/bash

DIR="/home/martin/test"

python src/transform_to_ned.py \
    --models \
        "$DIR/r29mrd124_20090613_02_dense_global.ply" \
    --poses \
        "$DIR/r29mrd124_20090613_02_cameras_global.csv" \
    --output \
        "/home/martin/test";
