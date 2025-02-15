import configparser
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def load_config(config_path: str = "config.ini"):
    config = configparser.ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
        return {
            'base_url': config.get('DEFAULT', 'base_url', fallback='https://news.google.com'),
            'output_format': config.get('DEFAULT', 'OutputFormat', fallback='json'),
            'language': config.get('DEFAULT', 'Language', fallback='en'),
            'region': config.get('DEFAULT', 'Region', fallback='IN'),
            'user_agent': config.get('DEFAULT', 'UserAgent',
                fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'),
            'proxy_enabled': config.getboolean('DEFAULT', 'ProxyEnabled', fallback=False),
            'proxy_address': config.get('DEFAULT', 'ProxyAddress', fallback=''),
            'use_selenium': config.getboolean('DEFAULT', 'UseSelenium', fallback=True)
        }
    return {}

def scrape():
    config = load_config()
    driver = webdriver.Firefox()
    query = "laptops"
    file = 0

    for i in range(5):
        driver.get(f"https://news.google.com/home?hl={lang}-{region}&gl={region}&ceid={region}:{lang}")

        elems = driver.find_elements(By.CLASS_NAME, "puisg-row")
        print(len(elems)," elements found.")
        for elem in elems:
            d = elem.get_attribute("outerHTML")
            with open(f"data/{query}_{file}.html", "w", encoding='utf-8') as f:
                f.write(d)
                file+=1

    driver.close()