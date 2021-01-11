import requests
import re
from bs4 import BeautifulSoup
from .createDevices import create

def main(company):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36','accept':'*/*'}

    URLS = [
        'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/noutbuki/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/fotoapparaty/zerkalnye-fotoapparaty/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/planshety/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
           ]
    HOST = 'https://shop.kz'

    def get_html(url,params = None):
        r = requests.get(url,headers = HEADERS, params=params)
        return r

    def get_content(html,cat_id,company):
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('div',class_ = 'bx_catalog_item_container gtm-impression-product')
        for item in items:
            name = re.sub(r'[А-я]+', '',item.find('div',class_ = 'bx_catalog_item_title').find('a').get_text(strip=True)).strip()
            description = re.sub(r'/', ' ', item.find('div',class_ = 'bx_catalog_item_articul').get_text(strip=True)).strip()
            price = int(re.sub('\D', '',item.find('span',class_ = 'bx-more-price-text').get_text(strip=True)))
            link = HOST + item.find('div',class_ = 'bx_catalog_item_title').find('a').get('href')
            url = company.replace(' ','-') + '-' +name.replace(' ','-')
            create(name, url, link, price, description, cat_id, company)


    def parse(URLS,company):
        for i,URL in enumerate(URLS):
            html = get_html(URL)
            if html != None and html.status_code == 200:
                get_content(html.text,i,company)
            else:
                print('Error')

    parse(URLS,company)