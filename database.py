from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()  # .env dosyasını yükle

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["blockchaindb"]
collection = db["blocks"]

def save_block_to_db(block):
    block_data = {
        "index": block.index,
        "data": block.data,
        "hash": block.hash,
        "previous_hash": block.previous_hash
    }
    collection.insert_one(block_data)
