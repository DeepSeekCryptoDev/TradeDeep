import os
import requests

# Load BonkBot API key from environment variables
BONKBOT_API_KEY = os.getenv("BONKBOT_API_KEY")
BONKBOT_BASE_URL = "https://api.bonkbot.io"  # Example base URL, replace with actual URL

# Helper function to make authenticated requests to BonkBot
def bonkbot_request(endpoint, payload):
    headers = {
        "Authorization": f"Bearer {BONKBOT_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(f"{BONKBOT_BASE_URL}/{endpoint}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error interacting with BonkBot API: {e}")
        return {"success": False, "error": str(e)}

# Initiate a trade using BonkBot
def initiate_trade(token, amount):
    payload = {
        "token": token,
        "amount": amount
    }
    result = bonkbot_request("trade", payload)
    if result.get("success"):
        return f"Trade successful: {result}"
    else:
        return f"Trade failed: {result.get('error')}"

# Initiate a withdrawal using BonkBot
def initiate_withdrawal(address, amount):
    payload = {
        "address": address,
        "amount": amount
    }
    result = bonkbot_request("withdraw", payload)
    if result.get("success"):
        return f"Withdrawal successful: {result}"
    else:
        return f"Withdrawal failed: {result.get('error')}"
