""" Parser for store Sulpak """
import re
import requests
from bs4 import BeautifulSoup
from .create_devices import create


def main(company):
    """ Main function for parsing """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'accept': '*/*'}

    # # Sulpak
    urls = [
        'https://www.sulpak.kz/f/smartfoniy',
        'https://www.sulpak.kz/f/noutbuki',
        'https://www.sulpak.kz/f/zerkalniye_fotoapparatiy',
        'https://www.sulpak.kz/f/planshetiy'
    ]
    host = 'https://www.sulpak.kz'

    def get_html(url, params=None):
        """ Get html """
        req = requests.get(url, headers=headers, params=params)
        return req

    def get_content(html, cat_id, company):
        """ Get info from html """
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='product-container-right-side')
        for item in items:
            description = item.find('h3', class_='title').get_text(strip=True)

            if item.find('span', class_='availability').get_text() == 'Нет в наличии':
                continue
            price = int(re.sub('\\D', '', item.find('div', class_='price').get_text(strip=True)))
            link = host + item.find('a').get('href')
            name = re.sub(r'[А-я]+', '', description).strip()
            url = company + '-' + name.replace(' ', '-')

            device_info = [name, url, link, price, description, cat_id, company]
            create(device_info)

    def parse(urls, company):
        """ Parsing through categories"""
        for i, url in enumerate(urls):
            html = get_html(url)
            if html is not None and html.status_code == 200:
                get_content(html.text, i, company)

    parse(urls, company)
