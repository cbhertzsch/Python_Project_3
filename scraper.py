
"""Project 3: Web scraping and multi-format output."""

import csv
import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


# Project settings
START_URL = "https://quotes.toscrape.com/"
OUTPUT_DIR = Path("output")
HEADERS = {
    "User-Agent": "PythonProject3-EducationalWebScraper/1.0"
}


def fetch_page(url):
    """Retrieve a webpage, retrying twice if the request fails."""
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
            return response

        except RequestException as error:
            print("Request failed:", error)

            if attempt < 2:
                print("Trying again...")
                time.sleep(2)

    print("Unable to retrieve the webpage after three attempts.")
    return None


def scrape_quotes():
    """Collect quotes, authors, tags, and page numbers from all pages."""
    url = START_URL
    page_number = 1
    all_quotes = []
    scraped_at = datetime.now().isoformat(timespec="seconds")

    while url:
        print("Scraping page:", page_number)
        response = fetch_page(url)

        if response is None:
            print("Scraping stopped because a page could not be retrieved.")
            return None, page_number - 1

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")

        for item in quotes:
            quote_text = item.find("span", class_="text").get_text()
            author = item.find("small", class_="author").get_text()

            tags = item.find_all("a", class_="tag")
            tag_list = []

            for tag in tags:
                tag_list.append(tag.get_text())

            record = {
                "quote": quote_text.strip("“”").strip(),
                "author": author,
                "tags": tag_list,
                "page": page_number,
                "scraped_at": scraped_at
            }

            all_quotes.append(record)

        next_button = soup.find("li", class_="next")

        if next_button:
            next_link = next_button.find("a")["href"]
            url = urljoin(url, next_link)
            page_number += 1
            time.sleep(1.5)
        else:
            url = None

    return all_quotes, page_number


def save_files(all_quotes):
    """Save the same quote records as JSON, CSV, TXT, and YAML."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_DIR / "quotes.json", "w", encoding="utf-8") as file:
        json.dump(all_quotes, file, indent=2, ensure_ascii=False)

    with open(
        OUTPUT_DIR / "quotes.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["quote", "author", "tags", "page", "scraped_at"])

        for record in all_quotes:
            writer.writerow([
                record["quote"],
                record["author"],
                ";".join(record["tags"]),
                record["page"],
                record["scraped_at"]
            ])

    with open(OUTPUT_DIR / "quotes.txt", "w", encoding="utf-8") as file:
        for record in all_quotes:
            file.write("Quote: " + record["quote"] + "\n")
            file.write("Author: " + record["author"] + "\n")
            file.write("Tags: " + ", ".join(record["tags"]) + "\n")
            file.write("Page: " + str(record["page"]) + "\n")
            file.write("Scraped: " + record["scraped_at"] + "\n")
            file.write("\n")

    with open(OUTPUT_DIR / "quotes.yaml", "w", encoding="utf-8") as file:
        yaml.safe_dump(
            all_quotes,
            file,
            allow_unicode=True,
            sort_keys=False
        )

    return 4


def main():
    """Run the scraper and report the results."""
    all_quotes, pages_fetched = scrape_quotes()

    if all_quotes is None:
        print("No output files were overwritten.")
        return

    files_written = save_files(all_quotes)

    print("Pages fetched:", pages_fetched)
    print("Quotes extracted:", len(all_quotes))
    print("Files written:", files_written)


if __name__ == "__main__":
    main()
