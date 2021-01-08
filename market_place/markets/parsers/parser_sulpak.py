import requests
from datetime import date
import re
import psycopg2
from bs4 import BeautifulSoup
def main():
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36','accept':'*/*'}

    # # Sulpak
    URLS = [
        'https://www.sulpak.kz/f/smartfoniy',
        'https://www.sulpak.kz/f/noutbuki',
        'https://www.sulpak.kz/f/zerkalniye_fotoapparatiy',
        'https://www.sulpak.kz/f/planshetiy'
           ]
    HOST = 'https://www.sulpak.kz'
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
        items = soup.find_all('div',class_ = 'product-container-right-side')

        category = cat_id
        company = 1
        for item in items:
            description = item.find('h3',class_ = 'title').get_text(strip=True),

            if item.find('span',class_ = 'availability').get_text() == 'Нет в наличии':
                continue
            price = int(re.sub('\D', '',item.find('div',class_ = 'price').get_text(strip = True))),
            link = HOST + item.find('a').get('href')
            name = re.sub(r'[А-я]+', '', description[0]).strip()
            url = str(company) + '-' +name.replace(' ','-')
            insert_device = """ 
                                INSERT INTO markets_device (name, description, link,url,category_id,company_id) 
                                VALUES (%s,%s,%s,%s,%s,%s)
                                ON CONFLICT (url) DO NOTHING;
                            """
            record_to_device = (name, description[0], link,url,category,company)
            cursor.execute(insert_device, record_to_device)
            conn.commit()

            last_id_query = f""" SELECT id FROM markets_device
                                WHERE markets_device.url = '{url}';
                            """
            cursor.execute(last_id_query)
            last_id = cursor.fetchone()[0]


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
                record_to_price = (price[0],date.today(),last_id)
                cursor.execute(insert_price, record_to_price)
                conn.commit()

    def parse(URLS,conn,cursor):
        for i,URL in enumerate(URLS):
            html = get_html(URL)
            if html != None and html.status_code == 200:
                get_content(html.text,conn,cursor,i+1)
            else:
                print('Error')

    parse(URLS,conn,cursor)
    if(conn):
        cursor.close()
        conn.close()
    print('Sulpak is correct')



