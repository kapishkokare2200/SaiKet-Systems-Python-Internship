
import sys
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraper for internship task)"}

SITES = {
    "1": {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/",
        "selectors": ["span.titleline > a", "a.storylink"],   # new layout, then old
    },
    "2": {
        "name": "BBC News",
        "url": "https://www.bbc.com/news",
        "selectors": ["h2[data-testid='card-headline']", "h3", "h2"],
    },
}


def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()          # raises for 404, 500, etc.
    return response.text


def extract_headlines(html, selectors, limit=15):
    soup = BeautifulSoup(html, "html.parser")
    for selector in selectors:
        found = soup.select(selector)
        headlines, seen = [], set()
        for tag in found:
            text = tag.get_text(strip=True)
            if text and text not in seen:         # skip blanks and duplicates
                seen.add(text)
                headlines.append(text)
        if headlines:
            return headlines[:limit]
    return []


def main():
    print("=== HEADLINE SCRAPER ===")
    for key, site in SITES.items():
        print(f"  {key}. {site['name']}")
    choice = input("Choose a site: ").strip()
    site = SITES.get(choice)
    if not site:
        print("Invalid choice.")
        return

    try:
        html = fetch_html(site["url"])
    except requests.exceptions.ConnectionError:
        sys.exit("Could not connect. Check your internet connection.")
    except requests.exceptions.Timeout:
        sys.exit("The request timed out. Try again later.")
    except requests.exceptions.HTTPError as e:
        sys.exit(f"The server returned an error: {e}")

    headlines = extract_headlines(html, site["selectors"])
    if not headlines:
        sys.exit("No headlines found - the site's HTML layout may have changed.")

    print(f"\nTop headlines from {site['name']}:\n" + "-" * 50)
    for i, headline in enumerate(headlines, start=1):
        print(f"{i:>2}. {headline}")


if __name__ == "__main__":
    main()