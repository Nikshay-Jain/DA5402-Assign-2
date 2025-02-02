import argparse
import configparser
import json
import csv
from pathlib import Path
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def load_config(config_path: str = "module1_config.ini") -> Dict:
    config = configparser.ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
        return {
            'base_url': config.get('DEFAULT', 'BaseURL', fallback='https://news.google.com'),
            'output_format': config.get('DEFAULT', 'OutputFormat', fallback='csv'),
            'user_agent': config.get('DEFAULT', 'UserAgent', 
                fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'),
            'proxy_enabled': config.getboolean('DEFAULT', 'ProxyEnabled', fallback=False),
            'proxy_address': config.get('DEFAULT', 'ProxyAddress', fallback=''),
            'use_selenium': config.getboolean('DEFAULT', 'UseSelenium', fallback=True)
        }
    return {}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Google News Scraper')
    parser.add_argument('--url', help='Base URL for Google News')
    parser.add_argument('--format', choices=['csv', 'json'], help='Output format')
    parser.add_argument('--config', default='module1_config.ini', help='Path to configuration file')
    return parser.parse_args()

def get_soup_with_requests(url: str, headers: Dict, proxies: Dict = None) -> BeautifulSoup:
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_soup_with_selenium(url: str) -> BeautifulSoup:
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = uc.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        return BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        driver.quit()

def scrape_news_page(soup: BeautifulSoup) -> List[Dict]:
    articles = []
    for article in soup.select('article'):
        title_elem = article.select_one('a[class*="WwrzSb"]')
        source_elem = article.select_one('div[class*="vr1PYe"]')
        time_elem = article.select_one('time')
        
        if title_elem:
            relative_url = title_elem.get('href', '')
            full_url = f'https://news.google.com{relative_url[1:]}' if relative_url.startswith('./') else relative_url
            
            articles.append({
                'title': title_elem.get_text(strip=True),
                'url': full_url,
                'source': source_elem.get_text(strip=True) if source_elem else None,
                'timestamp': time_elem['datetime'] if time_elem else None
            })
    return articles

def save_output(data: List[Dict], format: str = 'csv'):
    if not data:
        print("No data to save.")
        return
    
    if format == 'json':
        with open('google_news.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open('google_news.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    print(f"Successfully saved {len(data)} articles to google_news.{format}")

def main():
    args = parse_arguments()
    config = load_config(args.config)
    
    base_url = args.url or config.get('base_url', 'https://news.google.com')
    output_format = args.format or config.get('output_format', 'csv')
    user_agent = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://news.google.com/',
        'DNT': '1'
    }
    
    proxies = None
    if config.get('proxy_enabled'):
        proxies = {'http': config['proxy_address'], 'https': config['proxy_address']}
    
    if config.get('use_selenium'):
        soup = get_soup_with_selenium(base_url)
    else:
        time.sleep(random.uniform(1.5, 3.5))  # Add human-like delay
        soup = get_soup_with_requests(base_url, headers, proxies)
    
    if soup:
        print(f"Page title: {soup.title.string if soup.title else 'No title found'}")
        articles = scrape_news_page(soup)
        print(f"Found {len(articles)} articles")
        if articles:
            save_output(articles, output_format)
        else:
            print("No articles found. Check the HTML structure or selectors.")
    else:
        print("Failed to retrieve the page. Check your internet connection or try using Selenium.")

    # Debug: Save HTML for inspection
    with open('debug.html', 'w', encoding='utf-8') as f:
        f.write(str(soup) if soup else "No HTML retrieved")
    print("Debug HTML saved")

    # Additional debugging
    if soup:
        print(f"Number of <article> tags: {len(soup.find_all('article'))}")
        print("Number of title elements:", len(soup.select('a[class*=\"WwrzSb\"]')))

if __name__ == "__main__":
    main()
