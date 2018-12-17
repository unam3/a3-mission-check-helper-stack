from flask import Flask, request, render_template#, url_for
app = Flask(__name__)


#url_for('static', filename='style.css')

@app.route('/', methods=['GET', 'POST'])
def index():

    print request, request.mimetype, request.data, request.headers

    if request.method == 'POST':

        return 'POST processing'

        #return process_file()

    else:

        #return show_the_login_form()

        #return 'Hello, World!'

        return render_template('upload.html')
