from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Nietzsche válaszok database
nietzsche_responses = {
    'örök visszatérés': 'Az örök visszatérés: Élj úgy, mintha minden pillanatod örökké ismétlődne! A GFLO-ban ez azt jelenti: semmi energia nem veszik el, csak átalakul. Burned tokenek újjászületnek XP-ként.',
    'amor fati': 'Amor fati = szeresd a sorsodat! Fogadd el a randomságot (VRF), de strukturáld. A GFLO ezt teszi: chaos → order.',
    'übermensch': 'Az Übermensch nem felhalmoz, hanem teremt. XP-t csak aktivitással lehet szerezni, nem vásárlással. You ARE what you DO.',
    'path': 'Három út áll előtted: 🌊 Sovereign (kezdő), 🎨 Reformer (kreátor), 🔧 Praxis (építő). Melyiket választod?',
    'xp': 'XP = tapasztalat = identitás. Nem transferálható, nem csökken, csak nő. Ez a tied örökre.',
}

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'message': 'GFLO Backend Running',
        'ai': 'mock (no API key needed!)'
    })

@app.route('/api/paths')
def paths():
    return jsonify({
        'paths': [
            {'name': 'Sovereign', 'xp': 50000, 'emoji': '🌊'},
            {'name': 'Reformer', 'xp': 100000, 'emoji': '🎨'},
            {'name': 'Praxis', 'xp': 200000, 'emoji': '🔧'}
        ]
    })

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    message = data.get('message', '').lower()
    
    # Find best response
    response = "Érdekes kérdés! A GFLO filozófiája a merit-based identitásról szól. XP-t nem lehet venni, csak megszerezni. #NietzscheWeb3"
    
    for keyword, answer in nietzsche_responses.items():
        if keyword in message:
            response = answer
            break
    
    return jsonify({
        'response': response,
        'source': 'GFLO Mock AI (no API key needed)',
        'axiom': random.choice(['Eternal Return', 'Amor Fati', 'Übermensch'])
    })

if __name__ == '__main__':
    print("🚀 GFLO Flask API Starting...")
    print("🤖 AI: Mock responses (no API key needed!)")
    print("🌐 API running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
