import os
import requests
from config.settings import YELP_API_KEY

YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

def yelp_search(term, location="San Francisco"):
    if not YELP_API_KEY:
        return {"error": "Missing Yelp API key"}

    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }

    params = {
        "term": term,
        "location": location,
        "limit": 5
    }

    try:
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}