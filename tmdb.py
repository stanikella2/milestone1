import os

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://api.themoviedb.org/3/movie"
BASE_URL2 = "https://api.themoviedb.org/3/configuration"


def get_movie_details(movieid):

    params = {
        "api_key": os.getenv("tmdb_key"),
        "language": "en-US",
        "movie_id": movieid,
    }
    response = requests.get(f"{BASE_URL}/{movieid}", params=params)

    def get_movie_title(name):
        name = response.json()["title"]
        return name

    def get_movie_tagline(name):
        name = response.json()["tagline"]
        return name

    def get_movie_genres(name):
        name = response.json()["genres"]
        genre = []
        for i in range(len(name)):
            genre.append(name[i]["name"])
        return ",".join(genre)

    titles = get_movie_title(response)
    taglines = get_movie_tagline(response)
    genres = get_movie_genres(response)

    images = response.json()["poster_path"]
    params = {
        "api_key": os.getenv("tmdb_key"),
    }
    response2 = requests.get(f"{BASE_URL2}", params=params)

    def get_images(name):
        data = response2.json()
        name = data["images"]["base_url"]
        return name

    movie_image = get_images(response2)
    movieid = response.json()["id"]

    return {
        "movieid": movieid,
        "titles": titles,
        "taglines": taglines,
        "genres": genres,
        "images": images,
        "movie_image": movie_image,
    }
