import requests
import pandas as pd

# Base URL for rugcheck.xyz API or web scraping
RUGCHECK_API_URL = "https://rugcheck.xyz/api/check"  # Example API URL (modify as needed)

# Function to fetch token analysis data
def fetch_token_data(contract_address):
    try:
        # API request to check the token's contract
        response = requests.get(f"{RUGCHECK_API_URL}/{contract_address}")
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
        safety_score = data.get("safetyScore", 0)
        liquidity_burned = data.get("liquidity", {}).get("burned", False)
        mintable = data.get("permissions", {}).get("mintable", False)
        pausable = data.get("permissions", {}).get("pausable", False)

        # Exclude tokens with safety score below 85%
        if safety_score < 85:
            print(f"Token excluded due to low safety score: {safety_score}")
            return None

        # Return analyzed data
        return {
            "contract_address": data.get("contractAddress", "Unknown"),
            "token_name": data.get("tokenName", "Unknown"),
            "token_symbol": data.get("tokenSymbol", "Unknown"),
            "safety_score": safety_score,
            "liquidity_burned": liquidity_burned,
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
