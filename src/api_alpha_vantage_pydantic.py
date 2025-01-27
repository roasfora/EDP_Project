from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal
import requests
import os
import pandas as pd


class APIRequestParams(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10, pattern=r"^[A-Za-z0-9\.]+$")
    apikey: str = Field(..., min_length=10, description="API Key must be a valid string")
    function: Literal["TIME_SERIES_MONTHLY_ADJUSTED"] = "TIME_SERIES_MONTHLY_ADJUSTED"
    datatype: Literal["json"] = "json"


def fetch_monthly_adjusted_data(symbol: str):
    """
    Fetches monthly adjusted stock data using Alpha Vantage API.
    """
    # Retrieve API key from environment
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API Key not defined. Set the 'API_KEY' environment variable.")

    # Validate input parameters using Pydantic
    try:
        params = APIRequestParams(symbol=symbol, apikey=api_key)
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return None

    # Make the request
    url = "https://www.alphavantage.co/query"
    response = requests.get(url, params=params.dict())

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return None

    # Process the response
    data = response.json()
    if "Monthly Adjusted Time Series" not in data:
        print("Error: No data found for the provided symbol.")
        return None

    # Convert to DataFrame
    time_series = data["Monthly Adjusted Time Series"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)
    df.columns = [
        "open", "high", "low", "close",
        "adjusted_close", "volume", "dividend_amount"
    ]
    df = df.sort_index()

    # Save as CSV with an explicit header for the index column
    output_path = "./data/monthly_adjusted_data.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index_label="date")  # Ensure index column is labeled
    print(f"Data saved to {output_path}")

    return df


if __name__ == "__main__":
    try:
        result = fetch_monthly_adjusted_data("EDP.LS")
        if result is not None:
            print(result.head())
    except Exception as e:
        print(f"Error: {e}")
