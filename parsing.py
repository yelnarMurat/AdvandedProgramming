import requests
from bs4 import BeautifulSoup
import csv
import re

HOST = 'https://www.sulpak.kz'
URL  = 'https://www.sulpak.kz/f/noutbuki'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.97 Chrome/78.0.3904.97 Safari/537.36'
}


def get_html(url):
    r = requests.get(url)
    return r

def write_csv(data):
    with open('Sulpak.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['brand'],
                         data['list'],
                         data['availability'],
                         data['code'],
                         data['size'],
                         data['os'],
                         data['model_cpu'],
                         data['freq'],
                         data['ram_size'],
                         data['hard_typee'],
                         data['storage'],
                         data['videocard'],
                         data['videocard_mem'],
                         data['aa']
                         ))

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tile-container')


    for laptop in items:
        url_info = HOST+laptop.find('a', class_='title').get('href')
        html_info = get_html(str(url_info))
        laptop_info = BeautifulSoup(html_info.text, 'html.parser')
        item = laptop_info.find('table', class_='short-description-table').find_all('a')
        try:
            title = laptop.get('data-name')
        except:
            title = None
        try:
            price = laptop.get('data-price')
        except:
            price = None
        try:
            brand = laptop.get('data-brand')
        except:
            brand = None
        try:
            availability = laptop.find('span', class_='availability').get_text(strip=True)
        except:
            availability = None
        try:
            code =  laptop.get('data-code') #laptop.find('span', class_='code').get_text(strip=True)
        except:
            code = None
        try:
            list =  laptop.get('data-list') #laptop.find('span', class_='code').get_text(strip=True)
        except:
            list = None
        try:
            size = item[0].get_text(strip=True)
        except:
            size = None
        try:
            os = item[1].get_text(strip=True)
        except:
            os = None
        try:
            model_cpu = item[2].get_text(strip=True)
        except:
            model_cpu = None
        try:
            freq = item[3].get_text(strip=True)
        except:
            freq = None
        try:
            ram_size = item[4].get_text(strip=True)
        except:
            ram_size = None
        try:
            hard_typee = item[5].get_text(strip=True)
        except:
            hard_typee = None
        try:
            storage = item[6].get_text(strip=True)
        except:
            storage = None
        try:
            videocard = item[7].get_text(strip=True)
        except:
            videocard = None
        try:
            videocard_mem = item[8].get_text(strip=True)
        except:
            videocard_mem = None
        try:
            aa = item[9].get_text(strip=True)
        except:
            aa = None

        laptops = {
            'title': title,
            'price': price,
            'brand': brand,
            'list': list,
            'availability': availability,
            'code': code,
            'size': size,
            'os': os,
            'model_cpu': model_cpu,
            'freq': freq,
            'ram_size': ram_size,
            'hard_typee': hard_typee,
            'storage': storage,
            'videocard': videocard,
            'videocard_mem': videocard_mem,
            'aa': aa
        }
        write_csv(laptops)

if __name__=='__main__':
    page_part = '?page='

    total_pages =  10

    for i in range(1, total_pages):
        print(i)
        url_gen = URL + page_part + str(i)
        print(url_gen)
        html = get_html(url_gen)
        get_content(html.text)