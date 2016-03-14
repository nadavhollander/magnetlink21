from pymongo import MongoClient
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests
import os

# client = MongoClient()
# db = client.db
wallet = Wallet()

STORAGE_SERVERS = ['https://foo.com', 'https://bar.com', 'https://zed.com']

UPLOAD_FOLDER = 'storage'
AUTH_TOKEN = 'TEMP_AUTH_TOKEN' 

def storeFile(file, filename, sharding=False):
	if sharding:
		chunkData(file, filename)
	else:
		file.save(os.path.join('storage', filename))

def fetchFile(filename, sharded=False):
	try:
		file = open(os.path.join(UPLOAD_FOLDER, filename), 'rb')
		return file
	except Exception:
		raise Exception("File: 'filename' does not exist")

def chunkData(file, filename):
	numServers = len(STORAGE_SERVERS)        

 	# Get the file size
	file.seek(0, os.SEEK_END)
	fsize = file.tell()
	file.seek(0, 0)
	print(fsize)	
	# Get size of each chunk
	chunksz = int(float(fsize)/float(len(STORAGE_SERVERS)))
	print(chunksz)
	total_bytes = 0

	for x in range(len(STORAGE_SERVERS)):
		filename_x = filename + '-' + str(x+1)

    	# if reading the last section, calculate correct
    	# chunk size.
		if x ==  len(STORAGE_SERVERS) - 1:
			chunksz = fsize - total_bytes
		try:
			data = file.read(chunksz)
			total_bytes += len(data)
			print(total_bytes)
			chunkf = open(filename_x, 'wb')
			chunkf.write(data)
			chunkf.close()
		except (OSError, IOError) as e:
			print(e)
			continue
		except EOFError as e:
			print(e)
			break