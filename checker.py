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

def send_push_notification(message):
    user_key = os.getenv("PUSHOVER_USER_KEY")
    app_token = os.getenv("PUSHOVER_APP_TOKEN")
    if not user_key or not app_token:
        print("Pushover keys not set. Skipping notification.")
        return

    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": app_token,
        "user": user_key,
        "message": message,
        "title": "🎬 New Films at PCC",
        "priority": 0
    })

    if response.status_code != 200:
        print("Failed to send push notification:", response.text)
    else:
        print("✅ Push notification sent!")

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

            message = "New films listed at Prince Charles Cinema:\n" + "\n".join(f"• {film}" for film in new_films)
            send_push_notification(message)
        else:
            print("\nNo new films since last check.")

        save_films(current_films)