import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import glob

session = requests.Session()


def total_pages():
    url = session.get('https://gundamnesia.com/shop/page/1')
    soup = BeautifulSoup(url.text, 'html.parser')
    page_area = soup.find('ul', attrs={'class': 'page-numbers'})
    pages = []

    for page in page_area('a'):
        pag = page.get_text()
        pages.append(pag)

    del pages[-1]
    last_page = pages[-1]

    return int(last_page)


def get_url(page):
    print(f'Getting URL page {page}')
    url = session.get(f'https://gundamnesia.com/shop/page/{page}')
    soup = BeautifulSoup(url.text, 'html.parser')
    url = soup.find_all('h3', attrs={'class': 'heading-title product-name'})
    urls = []

    for i in url:
        link = i.find('a')['href']
        urls.append(link)

    return urls


def get_detail(link):
    print(f'Getting Detail {link}')
    url = session.get(link)
    soup = BeautifulSoup(url.text, 'html.parser')

    title = soup.find('h1', attrs={'class': 'product_title entry-title'}).text.strip()

    stock_area = soup.find('p', attrs={'class': 'availability stock in-stock'})
    stock = stock_area.find('span').text

    categories = soup.find('span', attrs={'class': 'cat-links'}).text

    datas = {
        'title': title,
        'stock': stock,
        'categories': categories,

    }

    'Write JSON file'
    with open(f'./results/{link.replace("https://gundamnesia.com/shop/", "").replace("/", "-")}.json', 'w') as outfile:
        json.dump(datas, outfile)


def create_csv_xlsx():
    print('Creating csv xlsx file...')
    datas = []
    files = glob.glob('./results/*.json')
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    'Create CSV File'
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)

    df = pd.DataFrame(datas)
    writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')

    df.to_excel(writer, index=False)
    writer.save()


if __name__ == '__main__':
    total_page = total_pages()
    total_urls = []

    for x in range(total_page):
        x += 1
        url = get_url(x)
        total_urls += url

    'Write JSON file'
    with open('urls.json', 'w') as outfile:
        json.dump(total_urls, outfile)

    with open('urls.json') as json_file:
        urls = json.load(json_file)

    for url in urls:
        get_detail(url)

    create_csv_xlsx()
