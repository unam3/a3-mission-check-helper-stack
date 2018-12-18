# Install virtualenv
http://flask.pocoo.org/docs/1.0/installation/#install-virtualenv

#mkdir -p mission_checker/src/uploads
#cd mission_checker

# Create virtual environment
virtualenv -p /usr/bin/python2 venv

# Activate the environment
. venv/bin/activate

# Install Flask
pip install Flask

# Run app
cd ~/mission_checker
. venv/bin/activate
FLASK_APP=~/mission_checker/src/app.py flask run

# Run app. Must never be used on production machines.
cd ~/mission_checker
. venv/bin/activate
FLASK_APP=~/mission_checker/src/app.py FLASK_ENV=development flask run

#
cd ~/a3/; rm -rf ~/mission_checker/src/check/; git archive --format=tar HEAD | (mkdir ~/mission_checker/src/check && cd ~/mission_checker/src/check && tar xf -)
