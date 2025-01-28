import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# DexScreener API base URL
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/tokens"

# Function to fetch data from DexScreener API
def fetch_dexscreener_data():
    try:
        response = requests.get(DEXSCREENER_API_URL)
        if response.status_code == 200:
            print("Successfully fetched data from DexScreener API.")
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Filter tokens based on criteria
def filter_tokens(data):
    filtered_tokens = []
    now = datetime.utcnow()
    twenty_four_hours_ago = now - timedelta(hours=24)

    for token in data.get("pairs", []):
        # Extract necessary fields
        launch_time = datetime.strptime(token.get("pairCreatedAt"), "%Y-%m-%dT%H:%M:%S.%fZ")
        hourly_txns = token.get("txns", {}).get("h1", 0)
        five_min_txns = token.get("txns", {}).get("m5", 0)

        # Apply filters
        if (
            launch_time > twenty_four_hours_ago
            and hourly_txns >= 100
            and five_min_txns >= 20
        ):
            filtered_tokens.append({
                "token_name": token.get("baseToken", {}).get("name", "Unknown"),
                "token_symbol": token.get("baseToken", {}).get("symbol", "Unknown"),
                "launch_time": launch_time,
                "hourly_transactions": hourly_txns,
                "five_minute_transactions": five_min_txns,
                "url": token.get("url", "N/A")
            })
    
    print(f"Filtered {len(filtered_tokens)} tokens meeting the criteria.")
    return filtered_tokens

# Save results to a CSV file
def save_to_csv(data, filename="filtered_tokens.csv"):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Save results to a JSON file
def save_to_json(data, filename="filtered_tokens.json"):
    try:
        with open(filename, "w") as f:
            import json
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# Main function to run the scraper
def main():
    # Fetch data from DexScreener
    data = fetch_dexscreener_data()
    if data:
        # Filter tokens based on criteria
        filtered_tokens = filter_tokens(data)
        # Save filtered tokens to files
        if filtered_tokens:
            save_to_csv(filtered_tokens)
            save_to_json(filtered_tokens)

if __name__ == "__main__":
    main()
