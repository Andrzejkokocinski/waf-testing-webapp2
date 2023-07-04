from flask import *
import os

app = Flask(__name__, template_folder = os.path.abspath('template'))
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')
app.config['SECRET_KEY'] = 'yt83t0ghasyg0j'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['GET'])
def index():
    args = request.args
    arg_search = args.get("search")

    get_request = {}
    if arg_search != '':
        get_request['search'] = arg_search

    return render_template('index.html', request=get_request)

