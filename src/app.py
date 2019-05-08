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
from check.mission_check_wo_layers import check as ref_check_mission
from check.garbage_collection import remove_check_products

app = Flask(__name__)

#url_for('static', filename='style.css')

def make_json(input):
    
    return json.dumps(json.dumps(input, ensure_ascii=False), ensure_ascii=False)

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

            check_results = {'errors': {'wrong_filename': True}}

            check_results_json = make_json(check_results)

            return render_template(
                'report.html',
                json=check_results_json
            )

        path_to_save_uploaded_file = path_to_uploads + file_storage_instance.filename

        # two separate open because python2 with 'r+' mode I'll get "no such file" error
        with open(path_to_save_uploaded_file, 'w') as file_to_write:

            file_storage_instance.save(path_to_save_uploaded_file)

        #print os.getcwd()

        try:

            extract_pbo(path_to_save_uploaded_file)

        except ExtractpboError as error:

            # we don't need unextractable file
            remove_check_products(path_to_save_uploaded_file)

            return render_template(
                'report.html',
                #json=('\'{"errors": {"extraction_error": "%s"}}\'' % (error.value.decode('utf-8')))
                json=make_json({"errors": {"extraction_error": error.value}})
            )


        # TODO: check this case
        mission_was_not_binarized = not was_mission_binarized(path_to_save_uploaded_file)


        path_to_extracted_mission = path_to_save_uploaded_file[:-4]

        check_results = check_mission(path_to_extracted_mission)

        ref_check_results = ref_check_mission(path_to_extracted_mission)

        remove_check_products(path_to_save_uploaded_file)
        remove_check_products(path_to_extracted_mission)


        if (mission_was_not_binarized):
            
            check_results['errors']['mission_was_not_binarized'] = True

        if (check_results != ref_check_results):

            check_results['diff'] = True

        check_results_json = make_json(check_results)

        return render_template(
            'report.html',
            json=check_results_json
        )

    else:

        return render_template('upload.html')
