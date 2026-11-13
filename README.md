
# Python Project 3: Web Scraping and Multi-Format Output

## Project Overview

For Project 3, I created a Python web scraper that collects quotes from the Quotes to Scrape website. The goal was to practice retrieving information from webpages, extracting specific data using BeautifulSoup, and saving the results in different file formats.

The scraper automatically follows the Next links until it reaches the last page. It collected 100 quotes from 10 pages, including the quote text, author, tags, page number, and scraping timestamp.

## Tools Used

- Python 3
- Requests: Retrieves webpage content.
- BeautifulSoup4: Extracts quotes, authors, and tags from HTML.
- PyYAML: Saves the collected data as YAML.
- CSV and JSON: Built-in Python libraries used for file exports.

## How to Run the Project

1. Download or clone the repository.
2. Open Terminal in the project folder.
3. Install the required libraries:

   `python -m pip install -r requirements.txt`

4. Run the scraper:

   `python scraper.py`

The scraper creates an `output` folder containing four files:

- `quotes.csv`
- `quotes.txt`
- `quotes.json`
- `quotes.yaml`

## Data Collection and Error Handling

The scraper uses a User-Agent to identify itself and waits 1.5 seconds between webpage requests.

If a request fails, it retries up to two additional times. If the page still cannot be retrieved, the program stops cleanly without overwriting the previous output files.

## Results

The completed scraper successfully collected 100 quotes across 10 pages and saved them in four formats.

I verified that the CSV, JSON, and YAML files contain matching records. The TXT file also contains the requested labelled fields and formatting.

## What I Learned

This project helped me understand how Python can retrieve information directly from websites instead of working only with existing datasets. I practiced using BeautifulSoup to navigate HTML, following pagination links, handling connection errors, and organizing scraped data into different file formats.

Unlike Project 2, this project focused on collecting data rather than processing it through a larger ETL pipeline.
