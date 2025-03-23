import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://princecharlescinema.com/whats-on/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
DATA_FILE = "film_log.json"

def get_current_films():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    titles = [a.get_text(strip=True) for a in soup.select("a.liveeventtitle")]
    return titles

def load_previous_films():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_films(films):
    with open(DATA_FILE, "w") as f:
        json.dump(films, f, indent=2)

if __name__ == "__main__":
    current_films = get_current_films()
    previous_films = load_previous_films()

    if not current_films:
        print("No films are currently listed.")
    else:
        print("🎬 Currently Showing:")
        for title in current_films:
            print("•", title)

        new_films = [film for film in current_films if film not in previous_films]
        if new_films:
            print("\n🆕 New Films Detected:")
            for title in new_films:
                print("✨", title)
        else:
            print("\nNo new films since last check.")

        save_films(current_films)