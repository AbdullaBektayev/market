from __future__ import absolute_import, unicode_literals
from .parsers import mechta,parser_sulpak,parser_technodom,shop
from celery import shared_task
@shared_task(name = 'add_new_devices')
def add_new_devices():
    try:
        # mechta.main('Mechta')            # parser for mechta
        parser_sulpak.main('Sulpak')     # parser for sulpak
        # parser_technodom.main('Technodom')  # parser for technodom
        # shop.main('Belyy veter')              # parser for belyy veter


        return 'Correct'
    except Exception as e:
        return e

