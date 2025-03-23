import requests
from bs4 import BeautifulSoup

URL = "https://princecharlescinema.com/whats-on/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_current_films():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # DEBUG: Print the first 500 characters of the page
    print("---- PAGE SNAPSHOT ----")
    print(soup.prettify()[:500])
    print("------------------------")

    titles = [h3.get_text(strip=True) for h3 in soup.select("h3.title")]
    return titles

if __name__ == "__main__":
    films = get_current_films()
    if films:
        print("🎬 Currently Showing:")
        for title in films:
            print("•", title)
    else:
        print("No films are currently listed.")