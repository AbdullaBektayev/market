import requests
import time
from selenium import webdriver
from datetime import date
import re
import psycopg2
from bs4 import BeautifulSoup
def main():
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36','accept':'*/*'}

    URLS = [
        'https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony/',
        'https://www.technodom.kz/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki',
        'https://www.technodom.kz/fototehnika-i-kvadrokoptery/fotoapparaty/fotoapparaty-zerkal-nye',
        'https://www.technodom.kz/smartfony-i-gadzhety/planshety-i-jelektronnye-knigi/planshety'
    ]
    HOST = 'https://www.technodom.kz'

    conn = psycopg2.connect(
        user= 'postgres',
        database = 'market',
        password = 'root',
        host = 'localhost',
        port = '5432'
    )
    cursor = conn.cursor()

    def get_html(url,params = None):
        r = requests.get(url,headers = HEADERS, params=params)
        return r

    def get_content(html,conn,cursor,cat_id):
        soup = BeautifulSoup(html,'html.parser')
        items = soup.find_all('li',class_='ProductCard')

        category = cat_id
        company = 2
        for item in items:
            description = item.find('h4').get_text(strip=True),
            price = int(re.sub('\D', '',item.find('p',class_ = 'ProductPrice').find('data').get_text(strip = True))),
            link = HOST + item.find('a').get('href')
            name = re.sub(r'[А-я,\',\"]+', '', description[0]).strip()
            url = str(company) + '-' + name.replace(' ','-')
            insert_device = """ 
                                        INSERT INTO markets_device (name, description, link,url,category_id,company_id) 
                                        VALUES (%s,%s,%s,%s,%s,%s)
                                        ON CONFLICT (url) DO NOTHING;
                                    """
            record_to_device = (name, description[0], link, url, category, company)
            cursor.execute(insert_device, record_to_device)
            conn.commit()

            last_id_query = f""" SELECT id FROM markets_device
                                        WHERE markets_device.url = '{url}';
                                    """
            cursor.execute(last_id_query)
            last_id = cursor.fetchone()
            if last_id:
                last_id = last_id[0]

            last_price_query = f""" SELECT price FROM markets_price
                                            WHERE markets_price.device_id = {last_id}
                                            ORDER BY id DESC
                                            LIMIT 1;
                                        """
            cursor.execute(last_price_query)

            last_price = cursor.fetchone()
            if last_price:
                last_price = last_price[0]

            if last_price != price[0]:
                insert_price = """ INSERT INTO markets_price (price,date,device_id)
                                            VALUES (%s,%s,%s)
                                        """
                record_to_price = (price[0], date.today(), last_id)
                cursor.execute(insert_price, record_to_price)
                conn.commit()

    def parse(URLS,conn,cursor,driver):
        for i,URL in enumerate(URLS):
            driver.get(URL)
            time.sleep(5)
            html = driver.page_source
            if html != None:
                get_content(html,conn,cursor,i+1)
            else:
                print('Error')

    driver = webdriver.Chrome()
    parse(URLS,conn,cursor,driver)
    driver.close()
    if(conn):
        cursor.close()
        conn.close()
    print('Technodom is correct')
