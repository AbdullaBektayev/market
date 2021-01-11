import time
from selenium import webdriver
import re
from bs4 import BeautifulSoup

from .createDevices import create


def main(company):
    URLS = [
        'https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony/',
        'https://www.technodom.kz/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki',
        'https://www.technodom.kz/fototehnika-i-kvadrokoptery/fotoapparaty/fotoapparaty-zerkal-nye',
        'https://www.technodom.kz/smartfony-i-gadzhety/planshety-i-jelektronnye-knigi/planshety'
    ]
    HOST = 'https://www.technodom.kz'

    def get_content(html,cat_id,company):
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('li',class_='ProductCard')
        for item in items:
            description = item.find('h4').get_text(strip=True),
            price = int(re.sub('\D', '',item.find('p',class_ = 'ProductPrice').find('data').get_text(strip = True))),
            link = HOST + item.find('a').get('href')
            name = re.sub(r'[А-я,\',\"]+', '', description[0]).strip()
            url = str(company) + '-' + name.replace(' ','-')
            create(name, url, link, price[0], description[0], cat_id, company)

    def parse(URLS,driver,company):
        for i,URL in enumerate(URLS):
            driver.get(URL)
            time.sleep(10)
            html = driver.page_source
            if html != None:
                get_content(html,i,company)
            else:
                print('Error')

    driver = webdriver.Chrome()
    parse(URLS,driver,company)
    driver.close()
