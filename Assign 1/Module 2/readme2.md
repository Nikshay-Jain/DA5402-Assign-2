# Google News Top Stories Scraper

This Python script scrapes the Top Stories section from Google News and then uses another script to fetch the articles' details.

## Requirements

- Python 3.7+
- Chrome browser installed

## Installation

1. Clone the repository or download the script.
2. Install required packages:
   ```
   pip install selenium undetected-chromedriver webdriver-manager
   ```

## Configuration

Create a `news_config.ini` file in the same directory as the script with the following content:

```ini
[DEFAULT]
BaseURL = https://news.google.com
NavSelector = //a[contains(@aria-label, "Top Stories")]
ArticleSelector = article
Timeout = 45
UserAgent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
ChromeVersion = 121
OutputFile = top_stories.json
```

## Usage

### Basic Run

```
python module2_top_stories.py
```

### Command-line Options

- Custom URL: `--url "https://news.google.com/topstories"`
- Custom selector: `--selector "//your-xpath-here"`
- Custom timeout: `--timeout 60`
- Custom config file: `--config "your_config.ini"`
- Specify Chrome version: `--chrome-version 120`
- Custom output file: `--output "your_output.json"`

Example:
```
python module2_top_stories.py --url "https://news.google.com" --timeout 60 --output "custom_output.json"
```

## Output

The script will print the URL of the Top Stories section and then run another script (`module2_scrape.py`) to scrape the actual articles. The output will be saved in a JSON file as specified in the configuration or command-line arguments.

## Troubleshooting

- If you encounter errors, check the `debug_top_stories.png` screenshot generated in the script's directory.
- Ensure your Chrome browser version matches the `ChromeVersion` in the config file.
- For persistent issues, try running without the headless mode by removing the `--headless=new` option in the `setup_driver` function.