from __future__ import absolute_import, unicode_literals
from .parsers import mechta,parser_sulpak,parser_technodom,shop
from celery import shared_task
@shared_task(name = 'add_new_devices')
def add_new_devices():
    try:
        # conn = psycopg2.connect(
        #     user= 'postgres',       # place for your postgres user_name
        #     database = 'market',    # place for your postgres database
        #     password = 'root',      # place for your postgres password
        #     host = 'localhost',     # place for your postgres host
        #     port = '5432'           # place for your postgres port
        # )
        #
        # cursor = conn.cursor()


        # mechta.main('Mechta')            # parser for mechta
        parser_sulpak.main('Sulpak')     # parser for sulpak
        # parser_technodom.main(conn,cursor)  # parser for technodom
        # shop.main(conn,cursor)              # parser for Белый ветер

        # if(conn):
        #     cursor.close()
        #     conn.close()

        return 'Correct'
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

