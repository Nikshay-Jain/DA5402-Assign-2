import argparse
import configparser
from pathlib import Path
from typing import Dict
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def load_config(config_path: str = "module2_config.ini") -> Dict:
    config = configparser.ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
        return {
            'base_url': config.get('DEFAULT', 'BaseURL', fallback='https://news.google.com'),
            'nav_selector': config.get('DEFAULT', 'NavSelector', 
                fallback='div[role="navigation"] a:first-child'),
            'user_agent': config.get('DEFAULT', 'UserAgent', 
                fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'use_selenium': config.getboolean('DEFAULT', 'UseSelenium', fallback=True)
        }
    return {}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Google News Navigation Scraper')
    parser.add_argument('--url', help='Base URL for Google News')
    parser.add_argument('--selector', help='CSS selector for navigation link')
    parser.add_argument('--config', default='module2_config.ini', help='Configuration file path')
    return parser.parse_args()

def get_soup_selenium(url: str) -> BeautifulSoup:
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="navigation"]'))
        )
        return BeautifulSoup(driver.page_source, 'html.parser')
    finally:
        driver.quit()

def get_soup_requests(url: str, headers: Dict) -> BeautifulSoup:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def extract_nav_link(soup: BeautifulSoup, selector: str) -> str:
    nav_item = soup.select_one(selector)
    if nav_item and (link := nav_item.get('href')):
        return f'https://news.google.com{link[1:]}' if link.startswith('./') else link
    return None

def main():
    args = parse_arguments()
    config = load_config(args.config)
    
    base_url = args.url or config['base_url']
    nav_selector = args.selector or config['nav_selector']
    user_agent = config['user_agent']
    
    headers = {'User-Agent': user_agent}
    
    if config['use_selenium']:
        soup = get_soup_selenium(base_url)
    else:
        soup = get_soup_requests(base_url, headers)
    
    if soup:
        if nav_link := extract_nav_link(soup, nav_selector):
            print(f"Found navigation link: {nav_link}")
        else:
            print("No navigation link found. Try updating the selector.")
    else:
        print("Failed to retrieve page content")

if __name__ == "__main__":
    main()
