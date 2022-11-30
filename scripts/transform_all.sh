#!/usr/bin/bash

# 1
CLUSTER="/home/martin/pCloudDrive/data/clusters/queensland/r7jjss8n6/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r7jjss8n6_20101023_dense_global.ply" \
        "$CLUSTER/r7jjss8n6_20121013_dense_global.ply" \
        "$CLUSTER/r7jjss8n6_20131022_dense_global.ply" \
    --poses \
        "$CLUSTER/r7jjss8n6_20101023_cameras_global.csv" \
        "$CLUSTER/r7jjss8n6_20121013_cameras_global.csv" \
        "$CLUSTER/r7jjss8n6_20131022_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 2
CLUSTER="/home/martin/pCloudDrive/data/clusters/queensland/r7jjskxq6/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r7jjskxq6_20101023_dense_global.ply" \
        "$CLUSTER/r7jjskxq6_20121013_dense_global.ply" \
        "$CLUSTER/r7jjskxq6_20131022_dense_global.ply" \
    --poses \
        "$CLUSTER/r7jjskxq6_20101023_cameras_global.csv" \
        "$CLUSTER/r7jjskxq6_20121013_cameras_global.csv" \
        "$CLUSTER/r7jjskxq6_20131022_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 3
CLUSTER="/home/martin/pCloudDrive/data/clusters/queensland/r7jjssbhh/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r7jjssbhh_20101023_dense_global.ply" \
        "$CLUSTER/r7jjssbhh_20121013_dense_global.ply" \
        "$CLUSTER/r7jjssbhh_20131022_dense_global.ply" \
    --poses \
        "$CLUSTER/r7jjssbhh_20101023_cameras_global.csv" \
        "$CLUSTER/r7jjssbhh_20121013_cameras_global.csv" \
        "$CLUSTER/r7jjssbhh_20131022_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 4
CLUSTER="/home/martin/pCloudDrive/data/clusters/scotts_reef/qtqxshxst/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/qtqxshxst_20150327_dense_global.ply" \
        "$CLUSTER/qtqxshxst_20150328_01_dense_global.ply" \
        "$CLUSTER/qtqxshxst_20150328_02_dense_global.ply" \
    --poses \
        "$CLUSTER/qtqxshxst_20150327_cameras_global.csv" \
        "$CLUSTER/qtqxshxst_20150328_01_cameras_global.csv" \
        "$CLUSTER/qtqxshxst_20150328_02_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 5
CLUSTER="/home/martin/pCloudDrive/data/clusters/tasmania/r234xgjef/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r234xgjef_20100604_dense_global.ply" \
        "$CLUSTER/r234xgjef_20120530_dense_global.ply" \
        "$CLUSTER/r234xgjef_20140616_dense_global.ply" \
    --poses \
        "$CLUSTER/r234xgjef_20100604_cameras_global.csv" \
        "$CLUSTER/r234xgjef_20120530_cameras_global.csv" \
        "$CLUSTER/r234xgjef_20140616_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 6
CLUSTER="/home/martin/pCloudDrive/data/clusters/tasmania/r23m7ms05/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r23m7ms05_20100606_dense_global.ply" \
        "$CLUSTER/r23m7ms05_20120601_dense_global.ply" \
        "$CLUSTER/r23m7ms05_20140616_dense_global.ply" \
    --poses \
        "$CLUSTER/r23m7ms05_20100606_cameras_global.csv" \
        "$CLUSTER/r23m7ms05_20120601_cameras_global.csv" \
        "$CLUSTER/r23m7ms05_20140616_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 7
CLUSTER="/home/martin/pCloudDrive/data/clusters/tasmania/r29kz9ff0/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r29kz9ff0_20090613_01_dense_global.ply" \
        "$CLUSTER/r29kz9ff0_20090613_02_dense_global.ply" \
        "$CLUSTER/r29kz9ff0_20130611_dense_global.ply" \
    --poses \
        "$CLUSTER/r29kz9ff0_20090613_01_cameras_global.csv" \
        "$CLUSTER/r29kz9ff0_20090613_02_cameras_global.csv" \
        "$CLUSTER/r29kz9ff0_20130611_cameras_global.csv" \
    --output \
        "$CLUSTER";


# 8
CLUSTER="/home/martin/pCloudDrive/data/clusters/tasmania/r29kz9dg9/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r29kz9dg9_20090613_01_dense_global.ply" \
        "$CLUSTER/r29kz9dg9_20090613_02_dense_global.ply" \
        "$CLUSTER/r29kz9dg9_20110616_dense_global.ply" \
        "$CLUSTER/r29kz9dg9_20130611_dense_global.ply" \
    --poses \
        "$CLUSTER/r29kz9dg9_20090613_01_cameras_global.csv" \
        "$CLUSTER/r29kz9dg9_20090613_02_cameras_global.csv" \
        "$CLUSTER/r29kz9dg9_20110616_cameras_global.csv" \
        "$CLUSTER/r29kz9dg9_20130611_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 9
CLUSTER="/home/martin/pCloudDrive/data/clusters/tasmania/r29mrd124/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r29mrd124_20090613_01_dense_global.ply" \
        "$CLUSTER/r29mrd124_20090613_02_dense_global.ply" \
        "$CLUSTER/r29mrd124_20110612_dense_global.ply" \
        "$CLUSTER/r29mrd124_20130611_dense_global.ply" \
    --poses \
        "$CLUSTER/r29mrd124_20090613_01_cameras_global.csv" \
        "$CLUSTER/r29mrd124_20090613_02_cameras_global.csv" \
        "$CLUSTER/r29mrd124_20110612_cameras_global.csv" \
        "$CLUSTER/r29mrd124_20130611_cameras_global.csv" \
    --output \
        "$CLUSTER";

# 10
CLUSTER="/home/martin/pCloudDrive/data/clusters/tasmania/r29mrd5h4/output"

python src/reconstruction/transform_to_ned.py \
    --models \
        "$CLUSTER/r29mrd5h4_20090612_dense_global.ply" \
        "$CLUSTER/r29mrd5h4_20090613_dense_global.ply" \
        "$CLUSTER/r29mrd5h4_20110612_dense_global.ply" \
        "$CLUSTER/r29mrd5h4_20130611_dense_global.ply" \
    --poses \
        "$CLUSTER/r29mrd5h4_20090612_cameras_global.csv" \
        "$CLUSTER/r29mrd5h4_20090613_cameras_global.csv" \
        "$CLUSTER/r29mrd5h4_20110612_cameras_global.csv" \
        "$CLUSTER/r29mrd5h4_20130611_cameras_global.csv" \
    --output \
        "$CLUSTER";
