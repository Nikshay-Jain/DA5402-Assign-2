# Google news scraper

## Overview

This project is a Google News scraper that allows users to extract news articles from the Google News website. It supports scraping the home page, top stories, and specific topics of interest.

---

## Requirements

### System Requirements
1. **Python 3.8+**
2. **Database**: PostgreSQL 14+
3. **Operating System**: Linux/MacOS (Windows WSL2 supported)
4. **ChromeDriver**: Required for headless browsing

### Python Packages
To install the necessary Python packages, run the following command:
```bash
pip install -r requirements.txt
```
*Sample requirements.txt*:
```
selenium==4.15.0
psycopg2-binary==2.9.9
imagehash==4.3.1
python-dotenv==1.0.0
```

---

## Execution  

To scrape the Google News website, update the `search_query` field in the `config.ini` file with one of the following options:  

1. `'home'` – Scrapes the entire homepage.  
2. `'top_stories'` – Scrapes only the top stories section.  
3. Any specific topic – Scrapes news articles related to the specified topic.  

Once the `config.ini` file is updated and saved, execute `main1.py`. The extracted results will be stored in a directory named after the specified `search_query`.

---