#!/bin/bash
set -e
target_dir=$1
[ -n "$target_dir" ] || exit 1
python setup.py easy_install --install-dir $target_dir --always-copy .
