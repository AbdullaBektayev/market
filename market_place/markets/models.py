from django.db import models
from datetime import date

class Category(models.Model):
    title = models.CharField('Title',max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Company(models.Model):
    name = models.CharField('Name',max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

class Device(models.Model):
    name = models.CharField('Name',max_length=100)
    description = models.TextField('Description')
    category = models.ForeignKey(Category,verbose_name='Category',on_delete=models.CASCADE)
    company = models.ForeignKey(Company,verbose_name='company',on_delete=models.CASCADE)
    link = models.CharField('Link to shop',max_length=150)
    url = models.SlugField(max_length=130,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

class Price(models.Model):
    amount = models.IntegerField('Amount',help_text = 'Amount in tenge')
    date = models.DateField('Date',default=date.today)
    device = models.ForeignKey(Device,verbose_name='device',on_delete=models.CASCADE)

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = 'amount'
        verbose_name_plural = 'amounts'



class RatingStar(models.Model):
    value = models.SmallIntegerField('Value',default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'

class Rating(models.Model):
    ip = models.CharField('IP address',max_length=15)
    star = models.ForeignKey(RatingStar,on_delete=models.CASCADE,verbose_name='star')
    device = models.ForeignKey(Device,on_delete=models.CASCADE,verbose_name='device')

    def __str__(self):
        return f'{self.star} - {self.device}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Name',max_length=100)
    text = models.TextField('Massage', max_length=5000)
    parent = models.ForeignKey('self',verbose_name='Parent',on_delete=models.SET_NULL,blank=True,null=True)
    device = models.ForeignKey(Device,verbose_name='device',on_delete=models.CASCADE,)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'




# Create your models here.
