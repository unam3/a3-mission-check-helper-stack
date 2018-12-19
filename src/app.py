#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys, os
from subprocess import check_output, CalledProcessError

#print sys.path

from flask import Flask, request, render_template#, url_for

from check.check_filename import is_filename_ok

app = Flask(__name__)

#url_for('static', filename='style.css')

@app.route('/', methods=['GET', 'POST'])
def index():

    #print request, request.mimetype, len(request.files)#, request.headers

    # TODO: add file length check
    if request.method == 'POST' and len(request.files) == 1 and request.files.has_key('mission_file'):

        # extractpbo can't read file from pipe, so we must save file on disk
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        path_to_uploads = current_script_dir + '/uploads/'

        file_storage_instance = request.files.get('mission_file')

        if not is_filename_ok(file_storage_instance.filename):

            # TODO: pass this to the client side
            print 'Filename is wrong!'

        path_to_save_uploaded_file = path_to_uploads + file_storage_instance.filename

        # two separate open because python2 with 'r+' mode I'll get "no such file" error
        file_to_write = open(path_to_save_uploaded_file, 'w')

        file_storage_instance.save(path_to_save_uploaded_file)

        file_to_write.close()

        # run mission_check.py path_to_save_uploaded_file
        devnull = open(os.devnull, 'w')

        #print os.getcwd()

        json = ''

        try:
            json = check_output(
                [
                    './src/check/check.sh',
                    path_to_save_uploaded_file,
                    './src/check/'
                ],
                #stderr=devnull
            )

        except CalledProcessError as shi:

            if (shi.returncode != 1):

                print 'return code: %s for %s' % (shi.returncode, path_to_save_uploaded_file)

        devnull.close()

        #print json


        # put json to the template
        # :-1 because of trailing newline
        return render_template('report.html', json=json[:-1].decode('utf-8'))

    else:

        return render_template('upload.html')
