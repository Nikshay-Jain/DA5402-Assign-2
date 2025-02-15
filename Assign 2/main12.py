# Scrapes pages from Google News

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from html_scraper import load_config, parse_arguments, scrape

def main12():
    args = parse_arguments()
    config = load_config(args.config)

    base_url = args.url or config.get('base_url', 'https://news.google.com')
    search_query = config.get('search_query', '')
    user_agent = config.get('user_agent', 'Mozilla/5.0')
    lang = config.get('language', 'en')
    region = config.get('region', 'IN')

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={user_agent}")

    # Setup WebDriver
    driver = webdriver.Firefox(options=options)

    if search_query=='home':
        driver.get(f"{base_url}/{search_query}?hl={lang}-{region}&gl={region}&ceid={region}:{lang}")

    elif search_query=='top_stories':
        driver.get("https://news.google.com/")
        full_html = driver.execute_script("return document.documentElement.outerHTML;")

        # Parse with BeautifulSoup
        soup = BeautifulSoup(full_html, "html.parser")

        # Extract all links from elements with class 'aqvwYd'
        links = []
        url = ''
        for link in soup.select('.aqvwYd'):
            href = link.get('href')
            
            if href and href.startswith('./'):
                url = f"https://news.google.com/{href[2:]}"
                links.append(url)

        # Ensure there's at least one link before accessing index 0
        if links:
            driver.get(links[0])
        else:
            print("No valid links found.")

    else:
        driver.get(f"{base_url}/search?q={search_query}&hl={lang}-{region}&gl={region}&ceid={region}:{lang}")

    scrape(driver, search_query)
    driver.quit()

if __name__ == '__main__':
    main12()