#!/bin/bash
set -e
target_dir=$1
[ -n "$target_dir" ] || exit 1
mkdir -p "$target_dir"
rc="VICVB.rc"
python lib/VICVB/data/install/helpers.py gen-rc install-dir "$target_dir" $rc
. "$rc"
python setup.py easy_install --install-dir "$target_dir" --always-copy .
#python setup.py easy_install --install-dir "$target_dir" .
mv "$rc" "$target_dir/"

galaxy_dir=$2
if [ -n "$galaxy_dir" ]; then
    galaxy_url=$3
    vicvb_postinstall install-to-galaxy --galaxy-root-url "$galaxy_url" "$galaxy_dir"
fi

