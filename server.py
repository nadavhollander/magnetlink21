import os
from flask import jsonify
import uuid
from flask import Flask, request
from flask import send_file
import model
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

@app.route('/download/<uid_filename>', methods=['GET'])
def download(uid_filename):
	sharded = request.args.get('shard')
	return send_file(model.fetchFile(uid_filename, sharded=sharded))

@app.route('/upload', methods=['GET', 'POST'])
# @payment.required(100)
def upload_file():
	sharding = request.args.get('shard')
	if not os.path.exists(UPLOAD_FOLDER):
		os.makedirs(UPLOAD_FOLDER)

	if request.method == 'POST':
		print(request.files['file'])
		file = request.files['file']
		uid = uuid.uuid4()
		filename = "{}_{}".format(uid, secure_filename(file.filename))
		
		if sharding:
			model.storeFile(file, filename, sharding=True)
		else:
			model.storeFile(file, filename)
		
		magnet_link = get_download_url(filename)
		if sharding:
			magnet_link += '?shard=1'
		return magnet_link

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
