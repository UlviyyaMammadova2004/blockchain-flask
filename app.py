from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
import os
import hashlib

# Ortam değişkeninden MONGO_URI'yi al
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB bağlantısı
client = MongoClient(MONGO_URI)
db = client["blockchaindb"]
collection = db["blocks"]

# Blockchain sınıfı
class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.data}{self.previous_hash}".encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), data, last_block.hash)
        self.chain.append(new_block)
        return new_block

# Flask app
app = Flask(__name__)
blockchain = Blockchain()

# HTML dosyasını oku
@app.route('/', methods=['GET'])
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

# Veri ekleme endpoint'i
@app.route('/add-data', methods=['POST'])
def add_data():
    content = request.json
    data = content.get("data")
    if not data:
        return jsonify({"error": "Data is required"}), 400

    block = blockchain.add_block(data)

    # MongoDB'ye kaydet
    collection.insert_one({
        "index": block.index,
        "data": block.data,
        "hash": block.hash,
        "previous_hash": block.previous_hash
    })

    return jsonify({
        "message": "Data added to blockchain",
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash
    }), 201

# Blockchain zincirini gösterme endpoint'i
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{
        "index": block.index,
        "data": block.data,
        "hash": block.hash,
        "previous_hash": block.previous_hash
    } for block in blockchain.chain]
    return jsonify(chain_data), 200

# Azure için uygun port ayarı
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
