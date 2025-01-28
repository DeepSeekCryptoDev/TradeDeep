import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for tweetscout.io
TWEETSCOUT_URL = "https://tweetscout.io/token"

# Function to fetch token social activity page
def fetch_token_social_page(token_slug):
    url = f"{TWEETSCOUT_URL}/{token_slug}/social-activity"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Successfully fetched social activity page for token: {token_slug}")
            return response.text
        else:
            print(f"Failed to fetch token page: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching token social page: {e}")
        return None

# Parse the HTML to extract influencer data
def parse_social_data(html):
    try:
        soup = BeautifulSoup(html, "html.parser")
        influencers = []

        # Locate influencer data
        influencer_rows = soup.select("table.influencer-table tr")  # Adjust based on the site's structure
        for row in influencer_rows:
            cols = row.find_all("td")
            if len(cols) >= 3:  # Ensure row has enough data
                name = cols[0].text.strip()
                followers = int(cols[1].text.strip().replace(",", ""))
                is_following = "following" in cols[2].text.lower()

                # Add data to list if influencer matches criteria
                if followers >= 40000 and is_following:
                    influencers.append({
                        "name": name,
                        "followers": followers,
                        "is_following": is_following
                    })
        print(f"Found {len(influencers)} influencers matching criteria.")
        return influencers
    except Exception as e:
        print(f"Error parsing social data: {e}")
        return []

# Save data to a CSV file
def save_to_csv(data, filename="influencers.csv"):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main function to run the scraper
def main():
    token_slug = "your_token_slug_here"  # Replace with the token's slug on tweetscout.io

    # Fetch and parse social data
    html = fetch_token_social_page(token_slug)
    if html:
        influencers = parse_social_data(html)
        # Save results to a CSV file
        if influencers:
            save_to_csv(influencers)

if __name__ == "__main__":
    main()
