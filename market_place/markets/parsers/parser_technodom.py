""" Parser for store Technodom """
import re
import time
from bs4 import BeautifulSoup

from .create_devices import create


def main(company, driver):
    """ Main function for parsing """
    urls = [
        'https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony/',
        'https://www.technodom.kz/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki',
        'https://www.technodom.kz/fototehnika-i-kvadrokoptery/fotoapparaty/fotoapparaty-zerkal-nye',
        'https://www.technodom.kz/smartfony-i-gadzhety/planshety-i-jelektronnye-knigi/planshety'
    ]
    host = 'https://www.technodom.kz'

    def get_content(html, cat_id, company):
        """ Get info from html """
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', class_='ProductCard')
        for item in items:
            description = item.find('h4').get_text(strip=True)
            price = int(re.sub('\\D',
                               '',
                               item.find('p', class_='ProductPrice'
                                         ).find('data').get_text(strip=True)))

            link = host + item.find('a').get('href')
            name = re.sub(r'[А-я,\',\"]+', '', description).strip()
            url = str(company) + '-' + name.replace(' ', '-')
            device_info = [name, url, link, price, description, cat_id, company]
            create(device_info)

    def parse(urls, driver, company):
        """ Parsing through categories"""
        for i, url in enumerate(urls):
            driver.get(url)
            time.sleep(10)
            html = driver.page_source
            if html is not None:
                get_content(html, i, company)

    parse(urls, driver, company)
