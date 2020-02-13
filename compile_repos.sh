#!/bin/bash

function compile_repos_to_folder {
    destination=$1
    current_dir=$(pwd)

    # TODO: add check if dir/file already exists

    git archive --format=tar HEAD | (cd $destination && tar xf -) &&
    #https://stackoverflow.com/questions/52955067/how-to-access-variables-used-in-git-submodule-foreach-from-outside
    # only $sm_path is set
    #git submodule foreach --recursive 'echo qwe $destination/$sm_path; ls $destination/$sm_path;'
    # only $destination is set
    #git submodule foreach --recursive "echo qwe $destination/$sm_path; ls $destination/$sm_path;" &&
    echo $destination > TEMP_DESTINATION &&
    #git submodule foreach --recursive 'pwd; echo $(cat $toplevel/TEMP_DESTINATION)/' &&
    git submodule foreach 'git archive --format=tar $sha1 | (cd $(cat $toplevel/TEMP_DESTINATION)/$sm_path && tar xf -);' &&
    rm TEMP_DESTINATION &&
    # one can use $(git submodule satus) parsing for path to submodule
    echo "const localizations = {$(cat $destination/src/check/msg_ru) $(cat $destination/src/check/msg_en) };" > $destination/src/templates/localizations &&

    cd $current_dir &&

    echo "New checker version successfully compiled into $destination"
}

if [[ -z $1 ]];
    then echo "first parameter must be absolute path to deploy destination folder";
    else compile_repos_to_folder $1;
fi
