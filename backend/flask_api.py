from flask import Flask, jsonify, request
from flask_cors import CORS
from web3 import Web3
import random
import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.env"))

app = Flask(__name__)
CORS(app)

# Web3 kapcsolat
w3 = Web3(Web3.HTTPProvider("https://sepolia.drpc.org"))

PIECORE_ADDRESS = "0x9CF55d0b9D61Dc28EF3cb10765CF4b861Cd0991e"
GASFEELOOP_ADDRESS = "0xd2C926F67080D6315b5dbBc7D621d729Cfe8A9C7"

PIECORE_ABI = [
    {"inputs":[{"name":"user","type":"address"}],"name":"getXP","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"getTier","outputs":[{"name":"","type":"uint8"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"identities","outputs":[{"name":"xp","type":"uint256"},{"name":"path","type":"uint8"},{"name":"tier","type":"uint8"}],"stateMutability":"view","type":"function"}
]

GASFEELOOP_ABI = [
    {"inputs":[{"name":"user","type":"address"}],"name":"getStake","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"getAccumulatedXP","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"name":"user","type":"address"}],"name":"getMultiplier","outputs":[{"name":"","type":"uint256"}],"stateMutability":"view","type":"function"}
]

pie = w3.eth.contract(address=Web3.to_checksum_address(PIECORE_ADDRESS), abi=PIECORE_ABI)
gas = w3.eth.contract(address=Web3.to_checksum_address(GASFEELOOP_ADDRESS), abi=GASFEELOOP_ABI)

PATH_NAMES = {0: 'None', 1: 'Sovereign', 2: 'Reformer', 3: 'Praxis'}

nietzsche_responses = {
    'örök visszatérés': 'Élj úgy, mintha minden pillanatod örökké ismétlődne! Burned tokenek örökre égnek.',
    'amor fati': 'Szeresd a sorsodat! A GFLO rendszerben a commitment burn ez.',
    'übermensch': 'Az Übermensch nem felhalmoz, hanem teremt. XP-t csak aktivitással lehet szerezni.',
    'path': 'Három út áll előtted: Sovereign (kezdő), Reformer (kreátor), Praxis (építő).',
    'xp': 'XP = tapasztalat = identitás. Nem transferálható, csak nő.',
}

@app.route('/api/status')
def status():
    connected = w3.is_connected()
    return jsonify({
        'status': 'operational',
        'blockchain': 'connected' if connected else 'disconnected',
        'network': 'sepolia',
        'contracts': {
            'PIECore': PIECORE_ADDRESS,
            'GasFeeLoop': GASFEELOOP_ADDRESS
        }
    })

@app.route('/api/identity/<address>')
def get_identity(address):
    try:
        addr = Web3.to_checksum_address(address)
        xp = pie.functions.getXP(addr).call()
        tier = pie.functions.getTier(addr).call()
        identity = pie.functions.identities(addr).call()
        stake = gas.functions.getStake(addr).call()
        accumulated_xp = gas.functions.getAccumulatedXP(addr).call()
        multiplier = gas.functions.getMultiplier(addr).call()

        return jsonify({
            'address': address,
            'xp': xp / 1e18,
            'tier': tier,
            'path': PATH_NAMES.get(identity[1], 'Unknown'),
            'stake': stake / 1e18,
            'accumulated_xp': accumulated_xp / 1e18,
            'multiplier': multiplier / 1e18,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/paths')
def paths():
    return jsonify({'paths': [
        {'name': 'Sovereign', 'xp': 50000, 'emoji': '🌊'},
        {'name': 'Reformer', 'xp': 100000, 'emoji': '🔥'},
        {'name': 'Praxis', 'xp': 200000, 'emoji': '🔧'}
    ]})

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    message = data.get('message', '').lower()
    response = "Érdekes kérdés! A GFLO a merit-based identitásról szól. #NietzscheWeb3"
    for keyword, answer in nietzsche_responses.items():
        if keyword in message:
            response = answer
            break
    return jsonify({
        'response': response,
        'source': 'GFLO Mock AI',
        'axiom': random.choice(['Eternal Return', 'Amor Fati', 'Übermensch'])
    })

if __name__ == '__main__':
    print("🚀 GFLO Flask API Starting...")
    print(f"🔗 Blockchain: {'connected' if w3.is_connected() else 'disconnected'}")
    app.run(host='0.0.0.0', port=5000, debug=True)
