# Google News Scraper README

This Python script scrapes headlines and image thumbnails from Google News.

## Requirements

- Python 3.7+
- Required packages: requests, beautifulsoup4, selenium, undetected-chromedriver

## Installation

1. Install required packages:
   ```
   pip install requests beautifulsoup4 selenium undetected-chromedriver
   ```

2. Download ChromeDriver and add it to your system PATH.

## Configuration

Create a `module1_config.ini` file with the following structure:

```ini
[DEFAULT]
BaseURL = https://news.google.com
OutputFormat = json
UserAgent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
ProxyEnabled = False
ProxyAddress = 
UseSelenium = True
```

## Usage

1. Basic run:
   ```
   python module3_images_title.py
   ```

2. Custom configuration:
   ```
   python module3_images_title.py --config news_config.ini
   ```

3. Specify output format:
   ```
   python module3_images_title.py --format csv
   ```

4. Custom URL:
   ```
   python script_name.py --url https://news.google.com/topstories
   ```

## Output

The script generates either `images_titles.json` or `images_titles.csv` in the current directory, containing scraped article data.

## Debugging

- Check `debug.html` for the raw HTML content of the scraped page.
- Console output provides information on the number of articles found and any errors encountered.