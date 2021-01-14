from ..models import Price,Company,Category,Device
from datetime import date

def create(name,url,link,price,description,cat_id,cur_comp):
    # print(name,url,link,price,description,cat_id,cur_comp)
    categories = ['Smartphone','Notebook','Camera','Tablet']
    category,cat_created = Category.objects.get_or_create(title = categories[cat_id], description = categories[cat_id],url = categories[cat_id])

    company,com_created = Company.objects.get_or_create(name = cur_comp,description = cur_comp,url = cur_comp)
    device, dev_created = Device.objects.filter(url = url).get_or_create(url=url, name=name, description=description, link=link,
                                                       company=company, category=category)


    all_price_obj = Price.objects.filter(device=device)
    last_price = -1
    if all_price_obj:
        last_price = all_price_obj.order_by('date').last().price

    if last_price != price:
        price = Price(price=price, device=device,date = date.today(),company = company,category = category)
        price.save()