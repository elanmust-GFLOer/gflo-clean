from flask import Flask, jsonify, request
from flask_cors import CORS
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.env"))

app = Flask(__name__)
CORS(app)

# ── FAUCET BLUEPRINT ──────────────────────────────────────────
from gflo_faucet import faucet_bp
app.register_blueprint(faucet_bp)
# ─────────────────────────────────────────────────────────────

# Web3 Setup
RPC_URL = os.getenv("SEPOLIA_RPC_URL", "https://sepolia.drpc.org")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract Addresses (update as needed)
PIECORE_ADDRESS = os.getenv("PIECORE_ADDRESS", "0x9CF55d0b9D61Dc28EF3cb10765CF4b861Cd0991e")
GASFEELOOP_ADDRESS = os.getenv("GASFEELOOP_ADDRESS", "0xd2C926F67080D6315b5dbBc7D621d729Cfe8A9C7")
GFLOGNITION_ADDRESS = os.getenv("GFLOGNITION_ADDRESS", "0x414DEDcf9264614Fd087BDa58bE27a0B698CcC54")

# Updated PIECore ABI (with extended functions)
PIECORE_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getIdentity",
        "outputs": [
            {"name": "xp", "type": "uint256"},
            {"name": "path", "type": "uint8"},
            {"name": "tier", "type": "uint8"},
            {"name": "nextThreshold", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "isEligibleForUpgrade",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getXP",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getTier",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getPath",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getNextThreshold",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Updated GasFeeLoop ABI
GASFEELOOP_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getStake",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getAccumulatedXP",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getMultiplier",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getEpochXP",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getRemainingEpochXP",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getUserInfo",
        "outputs": [
            {"name": "stakeAmount", "type": "uint256"},
            {"name": "multiplier", "type": "uint256"},
            {"name": "accumulatedXP", "type": "uint256"},
            {"name": "currentEpochXP", "type": "uint256"},
            {"name": "remainingEpochXP", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# GFLOIgnition ABI
GFLOGNITION_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "isReadyToIgnite",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getIgnitionCost",
        "outputs": [
            {"name": "cost", "type": "uint256"},
            {"name": "canAfford", "type": "bool"},
            {"name": "xpEligible", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Path names mapping
PATH_NAMES = {
    0: 'None',
    1: 'Sovereign',
    2: 'Reformer',
    3: 'Praxis'
}

# Initialize contracts
pie = w3.eth.contract(address=Web3.to_checksum_address(PIECORE_ADDRESS), abi=PIECORE_ABI)
gas = w3.eth.contract(address=Web3.to_checksum_address(GASFEELOOP_ADDRESS), abi=GASFEELOOP_ABI)

if GFLOGNITION_ADDRESS != "0x0000000000000000000000000000000000000000":
    ignition = w3.eth.contract(address=Web3.to_checksum_address(GFLOGNITION_ADDRESS), abi=GFLOGNITION_ABI)
else:
    ignition = None

# ============================================
# HEALTH CHECK ENDPOINTS
# ============================================

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'blockchain': 'connected' if w3.is_connected() else 'disconnected',
        'network': 'sepolia',
        'rpc_url': RPC_URL,
        'contracts': {
            'PIECore': PIECORE_ADDRESS,
            'GasFeeLoop': GASFEELOOP_ADDRESS,
            'GFLOIgnition': GFLOGNITION_ADDRESS if ignition else 'not_configured'
        }
    })

@app.route('/api/health')
def health():
    try:
        block = w3.eth.block_number
        return jsonify({'status': 'healthy', 'block': block})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

# ============================================
# IDENTITY ENDPOINTS
# ============================================

@app.route('/api/identity/<address>')
def get_identity(address):
    """Get complete identity info for a user"""
    try:
        addr = Web3.to_checksum_address(address)

        # Get PIECore identity
        xp, path, tier, nextThreshold = pie.functions.getIdentity(addr).call()
        eligible = pie.functions.isEligibleForUpgrade(addr).call()

        # Get GasFeeLoop info
        stake_info = gas.functions.getUserInfo(addr).call()

        # Format response
        response = {
            'address': address,
            'piecore': {
                'xp': xp,
                'path': PATH_NAMES.get(path, 'Unknown'),
                'tier': tier,
                'nextThreshold': nextThreshold,
                'eligibleForUpgrade': eligible
            },
            'gasfeeloop': {
                'stakeAmount': stake_info[0] / 1e18,
                'multiplier': stake_info[1] / 1e18,
                'accumulatedXP': stake_info[2] / 1e18,
                'currentEpochXP': stake_info[3] / 1e18,
                'remainingEpochXP': stake_info[4] / 1e18
            }
        }

        # Add GFLOIgnition info if available
        if ignition:
            try:
                ignition_data = ignition.functions.getIgnitionCost(addr).call()
                response['gflognition'] = {
                    'cost': ignition_data[0] / 1e18,
                    'canAfford': ignition_data[1],
                    'xpEligible': ignition_data[2],
                    'readyToIgnite': ignition.functions.isReadyToIgnite(addr).call()
                }
            except:
                pass

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/identity/<address>/pie')
def get_pie_identity(address):
    """Get PIECore identity only"""
    try:
        addr = Web3.to_checksum_address(address)
        xp, path, tier, nextThreshold = pie.functions.getIdentity(addr).call()
        eligible = pie.functions.isEligibleForUpgrade(addr).call()

        return jsonify({
            'address': address,
            'xp': xp,
            'path': PATH_NAMES.get(path, 'Unknown'),
            'tier': tier,
            'nextThreshold': nextThreshold,
            'eligibleForUpgrade': eligible
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/identity/<address>/stake')
def get_stake_info(address):
    """Get GasFeeLoop staking info"""
    try:
        addr = Web3.to_checksum_address(address)
        stake_info = gas.functions.getUserInfo(addr).call()

        return jsonify({
            'address': address,
            'stakeAmount': stake_info[0] / 1e18,
            'multiplier': stake_info[1] / 1e18,
            'accumulatedXP': stake_info[2] / 1e18,
            'currentEpochXP': stake_info[3] / 1e18,
            'remainingEpochXP': stake_info[4] / 1e18,
            'epochDuration': '7 days',
            'epochCap': '1000 XP'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================
# UPGRADE & IGNITION ENDPOINTS
# ============================================

@app.route('/api/upgrade/status/<address>')
def upgrade_status(address):
    """Check upgrade eligibility"""
    try:
        addr = Web3.to_checksum_address(address)

        xp, path, tier, nextThreshold = pie.functions.getIdentity(addr).call()
        eligible = pie.functions.isEligibleForUpgrade(addr).call()

        response = {
            'address': address,
            'currentPath': PATH_NAMES.get(path, 'Unknown'),
            'currentTier': tier,
            'xp': xp,
            'nextThreshold': nextThreshold,
            'eligibleForUpgrade': eligible,
            'xpProgress': f"{xp}/{nextThreshold}"
        }

        # Add ignition info if available
        if ignition:
            try:
                ready = ignition.functions.isReadyToIgnite(addr).call()
                ignition_data = ignition.functions.getIgnitionCost(addr).call()
                response['gflognition'] = {
                    'readyToIgnite': ready,
                    'cost': ignition_data[0] / 1e18,
                    'canAfford': ignition_data[1],
                    'xpEligible': ignition_data[2]
                }
            except:
                pass

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================
# INFO ENDPOINTS
# ============================================

@app.route('/api/paths')
def paths_info():
    """Get path information"""
    return jsonify({
        'paths': [
            {
                'id': 1,
                'name': 'Sovereign',
                'description': 'Entry-level autonomy',
                'emoji': '🌊',
                'nextXPRequired': 1000
            },
            {
                'id': 2,
                'name': 'Reformer',
                'description': 'Creative transformation',
                'emoji': '🔥',
                'nextXPRequired': 5000
            },
            {
                'id': 3,
                'name': 'Praxis',
                'description': 'Building & implementation',
                'emoji': '🔧',
                'nextXPRequired': 'Max'
            }
        ],
        'burnCosts': {
            'sovereignToReformer': '5000 GFLO',
            'reformerToPraxis': '10000 GFLO'
        }
    })

# ============================================
# BATCH ENDPOINTS
# ============================================

@app.route('/api/batch/identities', methods=['POST'])
def batch_identities():
    """Get identities for multiple addresses"""
    try:
        data = request.json
        addresses = data.get('addresses', [])

        if not addresses or len(addresses) > 100:
            return jsonify({'error': 'Invalid addresses count (max 100)'}), 400

        results = []
        for addr_str in addresses:
            try:
                addr = Web3.to_checksum_address(addr_str)
                xp, path, tier, nextThreshold = pie.functions.getIdentity(addr).call()

                results.append({
                    'address': addr_str,
                    'xp': xp,
                    'path': PATH_NAMES.get(path, 'Unknown'),
                    'tier': tier,
                    'nextThreshold': nextThreshold
                })
            except:
                results.append({'address': addr_str, 'error': 'Invalid'})

        return jsonify({'results': results, 'count': len(results)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================
# STARTUP
# ============================================

if __name__ == '__main__':
    print("🚀 GFLO Flask API Starting...")
    print(f"🔗 Blockchain: {'✅ connected' if w3.is_connected() else '❌ disconnected'}")
    print(f"📊 Contracts configured: PIECore, GasFeeLoop, GFLOIgnition")
    print(f"🌐 RPC: {RPC_URL}")
    app.run(host='0.0.0.0', port=5000, debug=False)
