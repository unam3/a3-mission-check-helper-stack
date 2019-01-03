#!/usr/bin/env python2
# coding: utf-8

from __future__ import unicode_literals

import re, sys, os, json

from subprocess import check_output, CalledProcessError

#print sys.path

from flask import Flask, request, render_template#, url_for

from check.check_filename import is_filename_ok
from check.extractpbo import extract_pbo, ExtractpboError
from check.check_binarization import was_mission_binarized
from check.mission_check import check as check_mission

app = Flask(__name__)

#url_for('static', filename='style.css')

@app.route('/', methods=['GET', 'POST'])
def index():

    #print request, request.mimetype, len(request.files)#, request.headers

    wrong_filename = False

    # TODO: add file length check
    if request.method == 'POST' and len(request.files) == 1 and request.files.has_key('mission_file'):

        # extractpbo can't read file from pipe, so we must save file on disk
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        path_to_uploads = current_script_dir + '/uploads/'

        file_storage_instance = request.files.get('mission_file')

        if not is_filename_ok(file_storage_instance.filename):

            wrong_filename = True

        path_to_save_uploaded_file = path_to_uploads + file_storage_instance.filename

        # two separate open because python2 with 'r+' mode I'll get "no such file" error
        file_to_write = open(path_to_save_uploaded_file, 'w')

        file_storage_instance.save(path_to_save_uploaded_file)

        file_to_write.close()

        #print os.getcwd()

        extractpbo_error = False

        try:

            extract_pbo(path_to_save_uploaded_file)

        except ExtractpboError as error:

            extractpbo_error = True
            
            return render_template(
                'report.html',
                json=('\'{"errors": ["%s"]}\'' % (error.value.decode('utf-8')))
            )


        # "mission.sqm wasn't binarized."
        mission_was_binarized = was_mission_binarized(path_to_save_uploaded_file)


        path_to_extracted_mission = path_to_save_uploaded_file[:-4]

        check_results = check_mission(path_to_extracted_mission)

        
        check_results_json = json.dumps(json.dumps(check_results, ensure_ascii=False), ensure_ascii=False)

        return render_template(
            'report.html',
            json=(
                #str('').join([
                #    check_results_json[:-3],
                #    str(', \\"wrong_filename\\": true}"')
                #])
                #if wrong_filename
                #else check_results_json[:-1]

                check_results_json
            )
        )

    else:

        return render_template('upload.html')
