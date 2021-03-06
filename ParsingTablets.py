import requests
from bs4 import BeautifulSoup
import csv
import re

HOST = 'https://www.sulpak.kz'
URL  = 'https://www.sulpak.kz/f/planshetiy'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.97 Chrome/78.0.3904.97 Safari/537.36'
}


def get_html(url):
    r = requests.get(url)
    return r

def write_csv(data):
    with open('Sulpak_Tablets.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['brand'],
                         data['code'],
                         data['list'],
                         data['size'],
                         data['memory'],
                         data['ram'],
                         data['network'],
                         data['main_camera'],
                         data['front_camera']
                         ))


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tile-container')


    for phone in items:
        url_info = HOST+phone.find('a', class_='title').get('href')
        html_info = get_html(str(url_info))
        phone_info = BeautifulSoup(html_info.text, 'html.parser')
        item = phone_info.find('table', class_='short-description-table').find_all('a')
        try:
            title = phone.get('data-name')
        except:
            title = None
        try:
            price = phone.get('data-price')
        except:
            price = None
        try:
            brand = phone.get('data-brand')
        except:
            brand = None
        try:
            code =  phone.get('data-code')
        except:
            code = None
        try:
            list =  phone.get('data-list')
        except:
            list = None
        try:
            size = item[0].get_text(strip=True)
        except:
            size = None
        try:
            memory = item[1].get_text(strip=True)
        except:
            memory = None
        try:
            ram = item[2].get_text(strip=True)
        except:
            ram = None
        try:
            network = item[3].get_text(strip=True)
        except:
            network = None
        try:
            main_camera = item[4].get_text(strip=True)
        except:
            main_camera = None
        try:
            front_camera = item[5].get_text(strip=True)
        except:
            front_camera = None

        phones = {
            'title': title,
            'price': price,
            'brand': brand,
            'code': code,
            'list': list,
            'size': size,
            'memory': memory,
            'ram': ram,
            'network': network,
            'main_camera': main_camera,
            'front_camera': front_camera
        }
        write_csv(phones)

if __name__=='__main__':
    page_part = '?page='

    total_pages = 6

    for i in range(1, total_pages):
        print(i)
        url_gen = URL + page_part + str(i)
        print(url_gen)
        html = get_html(url_gen)
        get_content(html.text)