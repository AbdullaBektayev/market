import requests
import re
from bs4 import BeautifulSoup
from .createDevices import create

def main(cur_comp):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36','accept':'*/*'}

    # # Sulpak
    URLS = [
        'https://www.sulpak.kz/f/smartfoniy',
        'https://www.sulpak.kz/f/noutbuki',
        'https://www.sulpak.kz/f/zerkalniye_fotoapparatiy',
        'https://www.sulpak.kz/f/planshetiy'
           ]
    HOST = 'https://www.sulpak.kz'

    def get_html(url,params = None):
        r = requests.get(url,headers = HEADERS, params=params)
        return r

    def get_content(html,cat_id,cur_comp):
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('div',class_ = 'product-container-right-side')
        for item in items:
            description = item.find('h3',class_ = 'title').get_text(strip=True),

            if item.find('span',class_ = 'availability').get_text() == 'Нет в наличии':
                continue
            price = int(re.sub('\D', '',item.find('div',class_ = 'price').get_text(strip = True))),
            link = HOST + item.find('a').get('href')
            name = re.sub(r'[А-я]+', '', description[0]).strip()
            url = str(cur_comp) + '-' +name.replace(' ','-')

            create(name, url, link, price[0], description[0], cat_id, cur_comp)

    def parse(URLS,cur_comp):
        for i,URL in enumerate(URLS):
            html = get_html(URL)
            if html != None and html.status_code == 200:
                get_content(html.text,i,cur_comp)
            else:
                print('Error')

    parse(URLS,cur_comp)
    print('Sulpak is correct')



