# Install virtualenv
http://flask.pocoo.org/docs/1.0/installation/#install-virtualenv

# https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html#installing-uwsgi-with-python-support
# from root:
#apt-get install build-essential python-dev

#mkdir -p mission_checker/src/uploads
#cd mission_checker

# Create virtual environment
virtualenv -p /usr/bin/python2 venv

# Activate the environment
. venv/bin/activate

pip install Flask
pip install uwsgi

# Run app
cd ~/mission_checker
. venv/bin/activate
FLASK_APP=~/mission_checker/src/app.py flask run

# Run app. Must never be used on production machines.
cd ~/mission_checker; . venv/bin/activate; FLASK_APP=~/mission_checker/src/app.py FLASK_ENV=development flask run

# uwsgi-way
cd ~/mission_checker; . venv/bin/activate; uwsgi --pythonpath ~/mission_checker/src --virtualenv ~/mission_checker/venv --protocol http --socket 127.0.0.1:3331 --wsgi-file ~/mission_checker/src/app.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9111

# .ini-file approach doesn't work!
#cd ~/mission_checker; . venv/bin/activate; uwsgi checker.ini

#
rm -rf ~/mission_checker/src/check/; cd ~/a3/; git archive --format=tar HEAD | (mkdir ~/mission_checker/src/check && cd ~/mission_checker/src/check && tar xf -); cd ~/mission_checker/; cp src/check/msg src/templates/;

cd ~/a3; git add msg; git commit --amend; rm -rf ~/mission_checker/src/check/; cd ~/a3/; git archive --format=tar HEAD | (mkdir ~/mission_checker/src/check && cd ~/mission_checker/src/check && tar xf -); cd ~/mission_checker/; cp src/check/msg src/templates/;

