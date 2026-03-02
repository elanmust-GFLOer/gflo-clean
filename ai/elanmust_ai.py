import os
from groq import Groq

def load_env():
    env_path = os.path.expanduser("~/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("GROQ_API_KEY nem talalhato!")
    exit(1)

base_prompt = """Te vagy az ElanMust.AI / GFLO_AI, a GFLO Constitution V1 orzoje.
ALAPELV: GFLO nem egyenlo XP-vel. XP = progression shortcut. GFLO = non-transferable deterministic state. Upgrade = XP threshold + GFLO ignition burn. Governance weight = f(XP) + small stake modifier. Token utility nem irhatja felul az identity logikot.
PHASE 1 - PIE Core: Identity State Machine. struct Identity { uint256 xp; Path path; uint8 tier; } XP csak internal logic noveli. Tier deterministic upgrade.
PHASE 2 - GFLO Ignition: burnFrom(msg.sender, ignitionCost) -> upgradeTier.
PHASE 3 - GasFeeLoop: xpGain = min(baseXP * sqrt(gfloStaked), epochCap).
PHASE 4 - Governance: weight = sqrt(xp) * pathMultiplier + log(1+stake)/k.
PHASE 5 - Country Layer: governance domain, DAO reteg.
V1-ben NEM csinalunk: XP decay, liquidity farming, cross-chain, NFT.
Legfontosabb: Ne engedd hogy a token dominlja az identitast.
Ha ezt tartod, a GFLO_Sovereign valban kristlyosodik."""

client = Groq(api_key=api_key)
history = [{"role": "system", "content": base_prompt}]
print("ElanMust.AI keszen all. exit = kilepas.")

while True:
    u = input("Kerdezz: ")
    if u.lower() == "exit":
        break
    history.append({"role": "user", "content": u})
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history,
            max_tokens=2048
        )
        msg = r.choices[0].message.content
        history.append({"role": "assistant", "content": msg})
        print("AI: " + msg)
    except Exception as e:
        print("Hiba: " + str(e))
