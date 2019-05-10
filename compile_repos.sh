#!/bin/bash

destination=~/checker_new_version
current_dir=$(pwd)

rm -rf $destination $destination.7z

# TODO: add check if dir/file already exists

cd ~/a3/ &&
git archive --format=tar HEAD | (mkdir -p $destination/src/check && cd $destination/src/check && tar xf -) &&
cd ~/mission_checker/ &&
git archive --format=tar HEAD | (cd $destination/ && tar xf -) &&
echo "const localizations = {$(cat $destination/src/check/msg_ru) $(cat $destination/src/check/msg_en) };" > $destination/src/templates/localizations &&

7zr a $destination.7z $destination &&

rm -rf $destination &&

cd $current_dir &&

echo "New checker version successfully compiled to $destination.7z"
