""" Parser for store Belyy Veter """
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
    urls = [
        'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/noutbuki/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/fotoapparaty/zerkalnye-fotoapparaty/filter/' +
        'almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/planshety/filter/almaty-is-v_' +
        'nalichii-or-ojidaem-or-dostavim/apply/'
           ]
    host = 'https://shop.kz'

    def get_html(url,params = None):
        """ Get html """
        req = requests.get(url,headers=headers, params=params)
        return req

    def get_content(html,cat_id,company):
        """ Get info from html """
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('div',class_ = 'bx_catalog_item_container gtm-impression-product')
        for item in items:
            name = re.sub(r'[А-я]+', '',item.find('div',
                                                  class_='bx_catalog_item_title'
                                                  ).find('a').get_text(strip=True)).strip()
            description = re.sub(r'/', ' ', item.find('div',
                                                      class_='bx_catalog_item_articul'
                                                      ).get_text(strip=True)).strip()
            price = int(re.sub('\\D', '', item.find('span',
                                                   class_='bx-more-price-text'
                                                   ).get_text(strip=True)))
            link = host + item.find('div',
                                    class_='bx_catalog_item_title'
                                    ).find('a').get('href')

            url = company.replace(' ', '-') + '-' + name.replace(' ', '-')
            device_info = [name, url, link, price, description, cat_id, company]
            create(device_info)


    def parse(urls, company):
        for i, url in enumerate(urls):
            html = get_html(url)
            if html is not None and html.status_code == 200:
                get_content(html.text, i, company)

    parse(urls, company)
