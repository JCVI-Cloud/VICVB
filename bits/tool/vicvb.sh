#!/bin/bash
index=$1
extras=$2
src=/home/atovtchi/work/jcvi_cloud_vir/jbrowse/jbrowse
rsync -av $src/ $extras/
cp $src/index.html $index

