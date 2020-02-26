#!/bin/bash

# Mission Checker deploy script
function deploy {
    # Install virtualenv, uwsgi
    # http://flask.pocoo.org/docs/1.0/installation/#install-virtualenv
    # https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html#installing-uwsgi-with-python-support
    sudo apt-get install python-virtualenv build-essential python-dev

    # Create necessary folders
    mkdir -p $1/uploads &&

    cd $1

    # Create virtual environment
    virtualenv -p /usr/bin/python2 venv

    # Activate the environment
    . venv/bin/activate

    pip install Flask
    pip install uwsgi

    export -f deactivate

    # deactivate virtualenv
    deactivate

    echo -n "# Run app on bare flask in dev-mode. Must never be used on production machines.
cd $1; . venv/bin/activate; FLASK_APP=$1/src/app.py FLASK_ENV=development flask run --host=0.0.0.0 && deactivate

# Uwsgi-way
cd $1; . venv/bin/activate; uwsgi --pythonpath $1/src --virtualenv $1/venv --protocol http --socket 0.0.0.0:3331 --wsgi-file $1/src/app.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:9111 --thunder-lock --logto $1/checker.log && deactivate

# logs into console
cd $1; . venv/bin/activate; uwsgi --pythonpath $1/src --virtualenv $1/venv --protocol http --socket 0.0.0.0:3331 --wsgi-file $1/src/app.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:9111 --thunder-lock && deactivate

### Update process steps ###
# Pack uploads if any files and logs; put away
if ! [[ -z \"\$(ls -A $1/uploads)\" ]] || ! [[ -z \"\$(ls -A $1/checker.log)\" ]];
    then tar cfJ analizeIt.tar.xz --ignore-failed-read $1/uploads $1/checker.log;
fi

# Remove old files
#rm -rf $1/src $1/uploads/* $1/checker.log
rm -rf $1/*

" > $1/run_n_update_commands &&

    echo "instructions and commands was written to $1/run_n_update_commands"
}

if [[ -z $1 ]];
    then echo "first parameter must be absolute path to deploy destination folder";
    else deploy $1;
fi
