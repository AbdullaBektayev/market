from __future__ import absolute_import, unicode_literals

import time

from .parsers import mechta,parser_sulpak,parser_technodom,shop
from celery import shared_task
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
@shared_task(name = 'add_new_devices')
def add_new_devices():
    try:
        driver = webdriver.Remote('http://selenium:4444/wd/hub', DesiredCapabilities.CHROME)
        mechta.main('Mechta',driver)            # parser for mechta
        parser_technodom.main('Technodom',driver)  # parser for technodom
        driver.quit()
        time.sleep(20)
        parser_sulpak.main('Sulpak')     # parser for sulpak
        shop.main('Belyy veter')              # parser for belyy veter
        return 'Correct'
    except Exception as e:
        return 'Incorrect'

