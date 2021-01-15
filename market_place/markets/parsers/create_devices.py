""" File for adding information to database from our parser """
import sys
from datetime import date
from ..models import Price, Company, Category, Device
sys.path.append("..")


def create(device_info):
    """ Create and add Devices to our Database """
    name, url, link, price, description, cat_id, cur_comp = device_info
    categories = ['Smartphone', 'Notebook', 'Camera', 'Tablet']

    category, _ = Category.objects.get_or_create(title=categories[cat_id],
                                                 description=categories[cat_id],
                                                 url=categories[cat_id])

    company, _ = Company.objects.get_or_create(name=cur_comp,
                                               description=cur_comp,
                                               url=cur_comp)

    device, _ = Device.objects.filter(url=url).get_or_create(url=url, name=name,
                                                             description=description,
                                                             link=link, company=company,
                                                             category=category)

    all_price_obj = Price.objects.filter(device=device)
    last_price = -1
    if all_price_obj:
        last_price = all_price_obj.order_by('date').last().price

    if last_price != price:
        price = Price(price=price, device=device,
                      date=date.today(), company=company, category=category)
        price.save()
