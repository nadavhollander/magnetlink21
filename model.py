from pymongo import MongoClient

client = MongoClient()
db = client.db

def get_