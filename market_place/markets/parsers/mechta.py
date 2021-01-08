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
        'https://www.mechta.kz/section/smartfony/',
        'https://www.mechta.kz/section/noutbuki-7n9',
        'https://www.mechta.kz/section/zerkalnye-fotoapparaty',
        'https://www.mechta.kz/section/planshety'
    ]
    HOST = 'https://www.mechta.kz'

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
        items = soup.find_all('div',class_ = 'hoverCard-child bg-white')

        category = cat_id
        company = 3
        for item in items:
            description = item.find('div',class_ = 'q-pt-md q-mt-xs q-px-md text-ts3 text-color2 ellipsis').get_text(strip=True),
            price = int(re.sub('\D', '',item.find('div',class_ = 'text-ts1').get_text(strip=True))),
            link = HOST
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
            time.sleep(15)
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
    print('Mechta is correct')
