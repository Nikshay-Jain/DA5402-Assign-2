from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os

def scrape_google_news_images(url):
    """
    Scrapes headlines and downloads corresponding images from Google News top stories.

    Args:
        url: The URL of the Google News homepage.

    Returns:
        None
    """

    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")  # Run browser in headless mode

        # Initialize a WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Explicit wait for headlines to appear
        wait = WebDriverWait(driver, 20)
        headline_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
                                                "h3.sv-title-header" 
                                                # Adjust this CSS selector as needed
                                                )) 
        )

        # Allow some time for JavaScript rendering
        sleep(5) 

        # Extract headlines and image URLs
        headlines = []
        image_urls = []
        for headline_element in headline_elements:
            headline = headline_element.text.strip()
            headlines.append(headline)

            # Find the corresponding image element (adjust this as needed)
            try:
                image_element = headline_element.find_element(By.XPATH, 
                                                             '..//ancestor::div[contains(@class, "sv-c-top-stories-article")]'
                                                             '//img') 
                image_url = image_element.get_attribute('src')
                image_urls.append(image_url)
            except:
                print(f"Image not found for headline: {headline}")
                image_urls.append(None)

        # Download images
        if not os.path.exists("google_news_images"):
            os.makedirs("google_news_images")

        for i, (headline, image_url) in enumerate(zip(headlines, image_urls)):
            if image_url:
                try:
                    response = requests.get(image_url)
                    response.raise_for_status() 
                    with open(f"google_news_images/image_{i+1}_{headline[:20]}.jpg", "wb") as f:
                        f.write(response.content)
                    print(f"Image {i+1} saved successfully.")
                except Exception as e:
                    print(f"Error downloading image {i+1}: {e}")

        driver.quit()

    except Exception as e:
        print(f"Error scraping headlines and images: {e}")

if __name__ == "__main__":
    url = "https://news.google.com/" 
    scrape_google_news_images(url)