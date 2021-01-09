from __future__ import absolute_import, unicode_literals
from .parsers import mechta,parser_sulpak,parser_technodom,shop
from celery import shared_task
# from celery.schedules import crontab # scheduler
# scheduled task execution
@shared_task(name = 'add_new_devices')
def add_new_devices():
    try:
        mechta.main()
        parser_sulpak.main()
        parser_technodom.main()
        shop.main()
        return 'Correct'
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

