from flask import Flask, request, render_template#, url_for

app = Flask(__name__)

#url_for('static', filename='style.css')

@app.route('/', methods=['GET', 'POST'])
def index():

    print request, request.mimetype, len(request.files)#, request.headers

    # add file length check
    if request.method == 'POST' and len(request.files) == 1 and request.files.has_key('mission_file'):

        return render_template('report.html', data='213')

    else:

        return render_template('upload.html')
