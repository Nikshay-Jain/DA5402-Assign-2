# Parses the HTMLs to get the thummbnails & headlines to be stored in a dictionary.

import pandas as pd
import os, requests, base64
from bs4 import BeautifulSoup

def download_image(img_url, save_path):
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()

        # Save the image locally
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        # Read and encode the image in Base64
        with open(save_path, 'rb') as file:
            encoded_img = base64.b64encode(file.read()).decode('utf-8')

        return [encoded_img, save_path]    # Return encoded image and file path

    except Exception as e:
        print(f"Thumbnail couldn't be downloaded")
        return ['','']

def get_data(file):
    dir = f'img_{file.split("/")[0][5:]}'
    count = file.split("/")[1][5:-5]

    if not os.path.exists(dir):
        os.mkdir(dir)

    html = open(file, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract image URL
    figure = soup.find('figure')
    if figure:
        img_tag = figure.find('img')
        if img_tag:
            img_url = img_tag.get('src')  # Extract src attribute
    else:
        img_url = ''
    
    img_url = f"https://news.google.com{img_url}"
    [encoded_img, save_path] = download_image(img_url, f"{dir}/thumbnails_{count}.jpg")

    all_a_tags = soup.find_all('a')
    headline = ''                  # Initialize headline to store result

    for a in all_a_tags:
        if not a.find_parent('div'):                   # Check if <a> is NOT inside <div>
            headline = " ".join(a.get_text().split())
            break 

    if headline == '':
        for cls in ['gPFEn', 'JtKRv', 'JtKRv vDXQhc', 'JrYg1b vP0hTc', 'JtKRv iTin5e', 'kEAYTc r5Cqre']:
            headline_tag = soup.find('a', {'class': cls})
            if headline_tag:
                headline = " ".join(headline_tag.get_text().split())
                break
    
    return [headline, save_path, encoded_img]

def main3():
    dirs = [d for d in os.listdir() if os.path.isdir(d) and d.startswith('data_')]
    for dir in dirs:
        print(f"Processing {dir}...")
        data = {"Headline": [], "Image Path": [], "Encoding": []}
        files = os.listdir(dir)
        for file in files:
            d = get_data(f"{dir}/{file}")
            data['Headline'].append(d[0])
            data['Image Path'].append(d[1])
            data['Encoding'].append(d[2])
        df = pd.DataFrame(data)
        df.to_csv(f'{dir}.csv', index=False)
        print(f"Data saved to {dir}.csv")

if __name__ == '__main__':
    main3()