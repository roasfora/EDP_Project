import os
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fetch_eur_to_usd_rate():
    """Scrape EUR to USD exchange rate and return the data."""
    try:
        # URL for scraping
        url = "https://www.x-rates.com/calculator/?from=EUR&to=USD&amount=1"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the exchange rate
            rate_element = soup.find("span", class_="ccOutputRslt")
            if rate_element:
                rate = float(rate_element.text.split()[0])

                # Prepare data
                data = {
                    "timestamp": datetime.utcnow().isoformat(),  # Use UTC for consistency
                    "eur_to_usd_rate": rate
                }
                return data
            else:
                raise Exception("Could not find the exchange rate on the webpage.")
        else:
            raise Exception(f"Failed to fetch the webpage: {response.status_code}")
    except Exception as e:
        raise RuntimeError(f"Error scraping EUR to USD exchange rate: {e}")

def save_to_csv(data, filename="eur_to_usd_rates.csv"):
    """Save EUR to USD exchange rate data to a CSV file."""
    os.makedirs("data", exist_ok=True)  # Ensure the 'data' folder exists
    filepath = os.path.join("data", filename)

    # Load existing data if the file exists
    if os.path.isfile(filepath):
        df = pd.read_csv(filepath)
    else:
        df = pd.DataFrame(columns=["timestamp", "eur_to_usd_rate"])

    # Append the new data
    new_data = pd.DataFrame([data])
    df = pd.concat([df, new_data], ignore_index=True)

    # Save the updated data back to CSV
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

def main():
    try:
        # Fetch EUR to USD exchange rate data
        rate_data = fetch_eur_to_usd_rate()

        # Print and save the data
        print(rate_data)
        save_to_csv(rate_data, "eur_to_usd_rates.csv")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
