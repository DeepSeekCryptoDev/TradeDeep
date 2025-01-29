import requests
import pandas as pd

# Base URL for rugcheck.xyz API or web scraping
RUGCHECK_API_URL = "https://api.rugcheck.xyz/v1/tokens"  

# Function to fetch token analysis data
def fetch_token_data(contract_address):
    try:
        # API request to check the token's contract
        response = requests.get(f"{RUGCHECK_API_URL}/{contract_address}/report")
        if response.status_code == 200:
            print(f"Successfully fetched data for contract: {contract_address}")
            return response.json()
        else:
            print(f"Failed to fetch data for contract: {contract_address}, Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching token data: {e}")
        return None

# Analyze the token's contract
def analyze_token(data):
    try:
        # Extract relevant details
        safety_score = data.get("score", 0)
        mintable = data.get("token", {}).get("mintAuthority", False)
        pausable = data.get("token", {}).get("freezeAuthority", False)

        # Exclude tokens with safety score below 100
        if safety_score < 100:
            print(f"Token excluded due to low safety score: {safety_score}")
            return None

        # Return analyzed data
        return {
            "contract_address": data.get("mint", "Unknown"),
            "token_name": data.get("tokenMeta", {}).get("name", "Unknown"),
            "token_symbol": data.get("tokenMeta", {}).get("symbol", "Unknown"),
            "safety_score": safety_score,
            "mintable": mintable,
            "pausable": pausable,
        }
    except Exception as e:
        print(f"Error analyzing token data: {e}")
        return None

# Save results to a CSV file
def save_to_csv(data, filename="rugcheck_results.csv"):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main function to run the analyzer
def main():
    # List of contract addresses to analyze
    contract_addresses = [
        "0x1234567890abcdef1234567890abcdef12345678",  # Replace with actual contract addresses
        "0xabcdef1234567890abcdef1234567890abcdef12",
    ]

    analyzed_data = []

    for contract_address in contract_addresses:
        # Fetch and analyze token data
        data = fetch_token_data(contract_address)
        if data:
            token_analysis = analyze_token(data)
            if token_analysis:
                analyzed_data.append(token_analysis)

    # Save results to CSV
    if analyzed_data:
        save_to_csv(analyzed_data)

if __name__ == "__main__":
    main()