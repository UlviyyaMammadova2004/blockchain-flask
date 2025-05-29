from flask import Flask, request, jsonify, render_template_string  # render_template_string eklendi
from blockchain import Blockchain
from database import save_block_to_db

app = Flask(__name__)
blockchain = Blockchain()

# Ana sayfada kullanıcı arayüzü gösterilsin:
@app.route('/', methods=['GET'])
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route('/add-data', methods=['POST'])
def add_data():
    content = request.json
    data = content.get("data")
    if not data:
        return jsonify({"error": "Data is required"}), 400

    block = blockchain.add_block(data)
    save_block_to_db(block)
    return jsonify({
        "message": "Data added to blockchain",
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash
    }), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{
        "index": block.index,
        "data": block.data,
        "hash": block.hash,
        "previous_hash": block.previous_hash
    } for block in blockchain.chain]
    return jsonify(chain_data), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))  # Azure 8080'de çalıştırır
    app.run(host='0.0.0.0', port=port)
