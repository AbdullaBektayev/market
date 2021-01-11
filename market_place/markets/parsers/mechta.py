from .createDevices import create
import time
from selenium import webdriver
import re
from bs4 import BeautifulSoup
def main(cur_comp):
    URLS = [
        'https://www.mechta.kz/section/smartfony/',
        'https://www.mechta.kz/section/noutbuki-7n9',
        'https://www.mechta.kz/section/zerkalnye-fotoapparaty',
        'https://www.mechta.kz/section/planshety'
    ]
    HOST = 'https://www.mechta.kz'

    def get_content(html,cat_id,cur_comp):
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('div',class_ = 'hoverCard-child bg-white')
        for item in items:
            description = item.find('div',class_ = 'q-pt-md q-mt-xs q-px-md text-ts3 text-color2 ellipsis').get_text(strip=True),
            price = int(re.sub('\D', '',item.find('div',class_ = 'text-ts1').get_text(strip=True))),
            link = HOST
            name = re.sub(r'[А-я,\',\"]+', '', description[0]).strip()
            url = cur_comp + '-' + name.replace(' ','-')

            create(name, url, link, price, description, cat_id, cur_comp)

    def parse(URLS,driver,cur_comp):
        for i,URL in enumerate(URLS):
            driver.get(URL)
            time.sleep(15)
            html = driver.page_source
            if html != None:
                get_content(html,i,cur_comp)
            else:
                print('Error')

    driver = webdriver.Chrome()
    parse(URLS,driver,cur_comp)
    driver.close()
    print('Mechta is correct')
