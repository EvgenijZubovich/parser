import requests
from bs4 import BeautifulSoup
import csv
import subprocess

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
           'accept': '*/*'}
HOST = 'https://cars.av.by'
FILE = 'cars.csv'


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    x = soup.find('a', class_='button button--default', rel='next', role='button')
    if x:
        pagination = HOST + soup.find('a', class_='button button--default', rel='next', role='button').get('href')
        return pagination


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item')
    cars = []
    for item in items:
        cars.append({
            'title': (item.find('span', class_='link-text').get_text()).replace('· ', ''),
            'link': HOST + item.find('a', class_='listing-item__link').get('href'),
            'usd_price': ' '.join((item.find('div', class_='listing-item__priceusd').get_text()).split()),
            'sity': item.find('div', class_='listing-item__location').get_text()
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в usd', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['sity']])


def parse():
    URL = input('Введите URL: ')
    URL.strip()
    sp_cars = []
    page = 1
    html = get_html(URL)
    if html.status_code == 200:
        while True:
            print(f'Парсинг страницы {page}.')
            content = get_content(html.text)
            sp_cars.extend(content)
            pages_count = get_pages_count(html.text)
            if pages_count != None:
                html = get_html(pages_count)
                page += 1
            else:
                break
    else:
        print('Error')
    print(f'Получено {len(sp_cars)} автомобилей.')
    save_file(sp_cars, FILE)
    subprocess.Popen(['see', f'{FILE}'])


parse()
# URL = 'https://cars.av.by/audi/a8'
