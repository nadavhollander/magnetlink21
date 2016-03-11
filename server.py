import os
from flask import jsonify
import uuid
from flask import Flask, request
from flask import send_from_directory
# from flask.ext.pymongo import PyMongo

#import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

from werkzeug import secure_filename

UPLOAD_FOLDER = 'storage'
SATS_PER_BYTE = 10 #change this

# set up server side wallet
app = Flask(__name__)
# mongo = PyMongo(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
wallet = Wallet()
payment = Payment(app, wallet)

def get_file_price(request):
	byteCount = 0
	if 'file' in request.files:
		byteCount = len(request.files['file'].read())
	return byteCount * SATS_PER_BYTE

def get_download_url(uid):
	return "/download/{}".format(uid)

@app.route('/download/<uid>', methods=['GET'])
def download(uid):
	uploads = app.config['UPLOAD_FOLDER']
	if os.path.isfile(os.path.join(uploads, uid)):
		return send_from_directory(uploads, uid, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
@payment.required(100)
def upload_file():
	if request.method == 'POST':
		print(request.files['file'])
		test_file = request.files['file']
		uid = uuid.uuid4()
		filename = "{}_{}".format(uid, secure_filename(test_file.filename))
		test_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print(test_file.read())
		return get_download_url(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
