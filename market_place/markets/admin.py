from django.contrib import admin

# Register your models here.
from .models import Category, Device, Company, Price, Review,RatingStar,Rating

admin.site.register(Category)
admin.site.register(Device)
admin.site.register(Company)
admin.site.register(Price)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(RatingStar)