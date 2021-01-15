""" Tasks for celery """
from __future__ import absolute_import, unicode_literals
import time
from selenium import webdriver
from celery import shared_task
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .parsers import mechta, parser_sulpak, parser_technodom, shop


@shared_task(name='add_new_devices')
def add_new_devices():
    """ Parse the Store """
    driver = webdriver.Remote('http://selenium:4444/wd/hub', DesiredCapabilities.CHROME)
    try:
        mechta.main('Mechta', driver)                # parser for mechta
        parser_technodom.main('Technodom', driver)   # parser for technodom
        driver.quit()
        time.sleep(20)

        parser_sulpak.main('Sulpak')                 # parser for sulpak
        shop.main('Belyy veter')                     # parser for belyy veter
        return 'Correct'
    except Exception as exp:
        driver.close()
        return exp
