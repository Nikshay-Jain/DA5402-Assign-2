from scraper import scrape
from bs4 import BeautifulSoup
import os, json, argparse, configparser

def get_data(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        t = soup.find('h2')
        try:
            name = t.get_text().split('\n')[0]
        except:
            return [None, None, None, None]
        
        price = soup.find('span', class_='a-price-whole').text
        rating = soup.find('span', attrs={'class': 'a-icon-alt'}).text
        url = f"https://amazon.in/{soup.find('a', class_='a-link-normal s-line-clamp-2 s-link-style a-text-normal')['href']}"

        return [name, price, rating, url]
    
    except Exception as e:
        print(f"Error: {e}")
        return [None, None, None, None]

if __name__ == '__main__':
    os.system("mkdir data")
    scrape()

    data = {"Name": [], "Price": [], "Rating": [], "URL": []}
    for file in os.listdir('data'):
        d = get_data(open(f"data/{file}", 'r', encoding='utf-8').read())
        data['Name'].append(d[0])
        data['Price'].append(d[1])
        data['Rating'].append(d[2])
        data['URL'].append(d[3])
        print(f"Data from data/{file} added to data.")
        
    pd.DataFrame(data).to_csv('data.csv', index=False)
