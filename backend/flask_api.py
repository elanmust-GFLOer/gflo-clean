from flask import Flask, jsonify
from flask_cors import CORS
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Web3 connection
rpc_url = os.getenv("SEPOLIA_RPC_URL", 
    "https://ethereum-sepolia-rpc.publicnode.com")
w3 = Web3(Web3.HTTPProvider(rpc_url))

@app.route('/api/status', methods=['GET'])
def status():
    connected = w3.is_connected()
    block = w3.eth.block_number if connected else 0
    return jsonify({
        'status': 'operational',
        'blockchain': 'connected' if connected else 'disconnected',
        'network': 'sepolia',
        'block_number': block,
        'message': 'GFLO Backend Running'
    })

@app.route('/api/paths', methods=['GET'])
def paths():
    return jsonify({
        'paths': [
            {
                'id': 1,
                'name': 'Sovereign',
                'xp_required': 50000,
                'eth_fee': 0.001,
                'tier': 1,
                'emoji': '🌊'
            },
            {
                'id': 2,
                'name': 'Reformer', 
                'xp_required': 100000,
                'eth_fee': 0.01,
                'tier': 2,
                'emoji': '🎨'
            },
            {
                'id': 3,
                'name': 'Praxis',
                'xp_required': 200000,
                'eth_fee': 0.1,
                'tier': 3,
                'emoji': '🔧'
            }
        ]
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    connected = w3.is_connected()
    return jsonify({
        'total_users': 0,
        'active_paths': 0,
        'block_number': w3.eth.block_number if connected else 0,
        'network': 'sepolia',
        'treasury_balance': '0 ETH',
        'total_xp_awarded': 0
    })

@app.route('/api/ai/status', methods=['GET'])
def ai_status():
    return jsonify({
        'ai_oracle': 'initializing',
        'axioms_loaded': 3,
        'last_check': 'never',
        'fraud_detections': 0
    })

if __name__ == '__main__':
    print("🚀 GFLO Flask API Starting...")
    print(f"✅ Blockchain: {'Connected' if w3.is_connected() else 'Disconnected'}")
    print(f"📦 Block: {w3.eth.block_number if w3.is_connected() else 'N/A'}")
    print("🌐 API running on http://localhost:5000")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """
    AI chatbot endpoint - Nietzsche filozófia alapján válaszol
    """
    from flask import request
    
    data = request.json
    user_message = data.get('message', '')
    
    # Mock AI response (később OpenAI/Groq)
    nietzsche_responses = {
        'örök visszatérés': 'Az örök visszatérés azt jelenti: élj úgy, mintha minden pillanatod örökké ismétlődne. "Semmi energia nem veszik el, csak átalakul" - ez a GFLO filozófiája is.',
        'amor fati': 'Amor fati: szeresd a sorsodat! Fogadd el a randomságot, de strukturáld. A GFLO-ban ezt VRF-fel valósítjuk meg.',
        'übermensch': 'Az Übermensch nem felhalmoz, hanem teremt értéket. A GFLO XP rendszer az aktivitást jutalmazza, nem a birtoklást.'
    }
    
    # Egyszerű keyword matching (később AI)
    response = "Érdekes kérdés! A GFLO filozófiája szerint..."
    for keyword, answer in nietzsche_responses.items():
        if keyword in user_message.lower():
            response = answer
            break
    
    return jsonify({
        'response': response,
        'source': 'ElanMust.AI',
        'axiom': 'Eternal Return'
    })

