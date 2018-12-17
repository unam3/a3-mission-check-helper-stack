#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys, os

#from subprocess import call, check_output, CalledProcessError


from flask import Flask, request, render_template#, url_for

app = Flask(__name__)

#url_for('static', filename='style.css')

@app.route('/', methods=['GET', 'POST'])
def index():

    print request, request.mimetype, len(request.files)#, request.headers

    # TODO: add file length check
    if request.method == 'POST' and len(request.files) == 1 and request.files.has_key('mission_file'):

        # extractpbo can't read file from pipe, so we must save file on disk
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        path_to_uploads = current_script_dir + '/uploads/'

        # implement next line in python:
        # sed -n -E '/^wog_[0-9]{2,3}_[a-z0-9_]+_[0-9]{2}\.[A-Za-z0-9_]+\.pbo$/p' <<< $filename

        file_storage_instance = request.files.get('mission_file')

        path_to_save_uploaded_file = path_to_uploads + file_storage_instance.filename

        # two separate open because python2 with 'r+' mode I'll get "no such file" error
        file_to_write = open(path_to_save_uploaded_file, 'w')

        file_storage_instance.save(path_to_save_uploaded_file)

        file_to_write.close()

        # run mission_check.py path_to_save_uploaded_file

        # put json to the template
        return render_template('report.html', json='213')

    else:

        return render_template('upload.html')
