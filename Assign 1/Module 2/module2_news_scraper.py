import argparse
import configparser
import time
import random
import json
from pathlib import Path
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import subprocess

# Configuration handling
def load_config(config_path: str = "news_config.ini") -> Dict:
    config = configparser.ConfigParser()
    
    # Set default values
    default_config = {
        'base_url': 'https://news.google.com',
        'nav_selector': '//a[contains(@aria-label, "Top Stories")]',
        'article_selector': 'article',
        'timeout': 45,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'chrome_version': 121,
        'output_file': 'top_stories.json'
    }
    
    if Path(config_path).exists():
        config.read(config_path)
        # Update default values with any config file values
        return {
            'base_url': config.get('DEFAULT', 'BaseURL', fallback=default_config['base_url']),
            'nav_selector': config.get('DEFAULT', 'NavSelector', fallback=default_config['nav_selector']),
            'article_selector': config.get('DEFAULT', 'ArticleSelector', fallback=default_config['article_selector']),
            'timeout': config.getint('DEFAULT', 'Timeout', fallback=default_config['timeout']),
            'user_agent': config.get('DEFAULT', 'UserAgent', fallback=default_config['user_agent']),
            'chrome_version': config.getint('DEFAULT', 'ChromeVersion', fallback=default_config['chrome_version']),
            'output_file': config.get('DEFAULT', 'OutputFile', fallback=default_config['output_file'])
        }
    return default_config


def parse_arguments():
    parser = argparse.ArgumentParser(description='Google News Scraper')
    parser.add_argument('--url', help='Base URL for Google News')
    parser.add_argument('--selector', help='XPath selector for Top Stories link')
    parser.add_argument('--timeout', type=int, help='Maximum wait time in seconds')
    parser.add_argument('--config', default='news_config.ini', help='Configuration file path')
    parser.add_argument('--chrome-version', type=int, help='Specific Chrome version to use')
    parser.add_argument('--output', help='Output JSON file name')
    return parser.parse_args()

# Selenium setup
def setup_driver(config: Dict) -> webdriver.Chrome:
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={config['user_agent']}")
    return uc.Chrome(
        options=options,
        version_main=config['chrome_version'],
        driver_executable_path=ChromeDriverManager().install()
    )

# Core scraping functions
def get_top_stories_url(driver: webdriver.Chrome, config: Dict) -> Optional[str]:
    try:
        driver.get(config['base_url'])
        time.sleep(random.uniform(2, 4))
        
        WebDriverWait(driver, config['timeout']).until(
            EC.presence_of_element_located((By.XPATH, '//main'))
        )

        selectors = [
            config['nav_selector'],
            '//a[contains(@href, "/topics/")]',
            '//a[.//*[contains(text(), "Top")]]'
        ]
        
        for selector in selectors:
            try:
                element = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                return element.get_attribute('href')
            except TimeoutException:
                continue
        return None

    except Exception as e:
        print(f"Error finding Top Stories: {str(e)}")
        driver.save_screenshot('debug_top_stories.png')
        return None

# Main workflow
def main():
    args = parse_arguments()
    config = load_config(args.config)
    
    # Apply command-line overrides
    if args.url: config['base_url'] = args.url
    if args.selector: config['nav_selector'] = args.selector
    if args.timeout: config['timeout'] = args.timeout
    if args.chrome_version: config['chrome_version'] = args.chrome_version
    if args.output: config['output_file'] = args.output

    driver = setup_driver(config)
    try:
        if top_stories_url := get_top_stories_url(driver, config):
            print(f"Found Top Stories: {top_stories_url}")
            format = "json"
            command = [
                "python",
                "./Assign 1/Module 1/module1_news_scraper.py",
                "--url",
                top_stories_url,
                "--format",
                format
            ]
            subprocess.run(command)

        else:
            print("Failed to find Top Stories section")
            
    except WebDriverException as e:
        print(f"Browser error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
