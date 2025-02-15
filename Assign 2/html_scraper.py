from pathlib import Path
import configparser, argparse, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config(config_path: str = "config.ini"):
    """ Load configuration from the INI file. """
    config = configparser.ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
        return {
            'base_url': config.get('DEFAULT', 'base_url', fallback='https://news.google.com'),
            'search_query': config.get('DEFAULT', 'search_query', fallback=''),
            'language': config.get('DEFAULT', 'Language', fallback='en'),
            'region': config.get('DEFAULT', 'Region', fallback='IN'),
            'user_agent': config.get('DEFAULT', 'user_agent',
                fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'),
        }
    return {}

def parse_arguments():
    """ Parse command-line arguments. """
    parser = argparse.ArgumentParser(description='Google News Scraper')
    parser.add_argument('--url', help='Base URL for Google News')
    parser.add_argument('--config', default='config.ini', help='Path to configuration file')
    return parser.parse_args()

def scroll_to_load(driver, pause_time=2):
    """ Scroll down the page multiple times to load more news articles. """
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:  # Stop scrolling if no new content is loaded
            break
        last_height = new_height

def scrape(driver, query):
    """ Scrape Google News and save each article as a separate HTML file. """
    output_dir = Path(f"data_{query}")
    output_dir.mkdir(parents=True, exist_ok=True)

    scroll_to_load(driver)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"{len(articles)} articles found.")

        for idx, article in enumerate(articles):
            article_html = article.get_attribute("outerHTML")
            file_path = output_dir / f"news_{idx + 1}.html"

            with open(file_path, "w", encoding='utf-8') as f:
                f.write(article_html)
                print(f"Saved: {file_path}")

    except Exception as e:
        print(f"Error: {e}")

    driver.quit()