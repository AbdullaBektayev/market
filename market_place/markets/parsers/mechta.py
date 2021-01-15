""" Parser for store Mechta """
import time
import re
from bs4 import BeautifulSoup
from .create_devices import create


def main(company,driver):
    """ Main function for parsing """
    urls = [
        'https://www.mechta.kz/section/smartfony/',
        'https://www.mechta.kz/section/noutbuki-7n9/',
        'https://www.mechta.kz/section/zerkalnye-fotoapparaty/',
        'https://www.mechta.kz/section/planshety/'
    ]
    host = 'https://www.mechta.kz'

    def get_content(html,cat_id,company):
        """ Get info from html """
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='hoverCard-child bg-white')
        for item in items:
            description = item.find(
                'div',
                class_='q-pt-md q-mt-xs q-px-md text-ts3 text-color2 ellipsis'
            ).get_text(strip=True)

            price = int(re.sub('\\D',
                               '',
                               item.find('div',class_='text-ts1').get_text(strip=True)))
            link = host
            name = re.sub(r'[А-я,\',\"]+', '', description).strip()
            url = company + '-' + name.replace(' ', '-')
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
