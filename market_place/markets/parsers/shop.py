import requests
from datetime import date
import re
import psycopg2
from bs4 import BeautifulSoup
def main():
    HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36','accept':'*/*'}


    URLS = [
        'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/noutbuki/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/fotoapparaty/zerkalnye-fotoapparaty/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/planshety/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
           ]
    HOST = 'https://shop.kz'

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
        items = soup.find_all('div',class_ = 'bx_catalog_item_container gtm-impression-product')
        category = cat_id
        company = 4
        for item in items:
            name = re.sub(r'[А-я]+', '',item.find('div',class_ = 'bx_catalog_item_title').find('a').get_text(strip=True)).strip()
            description = re.sub(r'/', ' ', item.find('div',class_ = 'bx_catalog_item_articul').get_text(strip=True)).strip()
            price = int(re.sub('\D', '',item.find('span',class_ = 'bx-more-price-text').get_text(strip=True)))
            link = HOST + item.find('div',class_ = 'bx_catalog_item_title').find('a').get('href')
            url = str(company) + '-' +name.replace(' ','-')

            insert_device = """
                                        INSERT INTO markets_device (name, description, link,url,category_id,company_id)
                                        VALUES (%s,%s,%s,%s,%s,%s)
                                        ON CONFLICT (url) DO NOTHING;
                                    """
            record_to_device = (name, description, link, url, category, company)
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

            if last_price != price:
                insert_price = """ INSERT INTO markets_price (price,date,device_id)
                                            VALUES (%s,%s,%s)
                                        """
                record_to_price = (price, date.today(), last_id)
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


    print('Shop is correct')