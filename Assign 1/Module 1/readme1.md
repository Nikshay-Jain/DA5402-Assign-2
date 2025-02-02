# Google News Scraper

A flexible Python script to scrape articles from Google News.

## Requirements

- Python 3.7+
- Required packages: 
  ```
  pip install requests beautifulsoup4 undetected-chromedriver==3.5.3 selenium==4.15.2
  ```

## Setup

1. Clone or download the script.
2. Create a `module1_config.ini` file in the same directory with the following content:

```
[DEFAULT]
BaseURL = https://news.google.com
OutputFormat = json
UserAgent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
ProxyEnabled = False
UseSelenium = True
```

## Usage

### Basic Run
```
python module1_news_scraper.py
```

### Command-line Options
- Set custom URL: 
  ```
  python module1_news_scraper.py --url "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB"
  ```
- Change output format: 
  ```
  python module1_news_scraper.py --format csv
  ```
- Specify config file: 
  ```
  python module1_news_scraper.py --config custom_config.ini
  ```

## Output

The script generates either a JSON or CSV file (based on configuration) named `google_news.json` or `google_news.csv` in the same directory.

## Troubleshooting

If no articles are found, check the `debug.html` file generated in the same directory for the raw HTML content retrieved from Google News.