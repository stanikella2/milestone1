import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_wiki_link(movies_ids):
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "inprop": "url",
        "titles": movies_ids,
        "formatversion": 2,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    results = data["query"]["pages"][0]["fullurl"]
    return results
