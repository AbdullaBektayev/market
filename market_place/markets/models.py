""" Our model of Database """
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """ Category table """
    title = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Company(models.Model):
    """ Company table """
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Device(models.Model):
    """ Device table """
    name = models.CharField('Name',max_length=100)
    description = models.TextField('Description')
    category = models.ForeignKey(Category,
                                 verbose_name='Category',
                                 on_delete=models.CASCADE,
                                 related_name='device')

    company = models.ForeignKey(Company,
                                verbose_name='company',
                                on_delete=models.CASCADE,
                                related_name='device')

    link = models.CharField('Link to shop', max_length=200)
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'


class Price(models.Model):
    """ Price table """
    price = models.IntegerField('Price', help_text = 'Price in tenge')
    date = models.DateField('Date', default=timezone.now)
    device = models.ForeignKey(Device,
                               verbose_name='device',
                               on_delete=models.CASCADE,
                               related_name='price')

    company = models.ForeignKey(Company,
                                verbose_name='company',
                                on_delete=models.CASCADE,
                                related_name='price',
                                default=0)

    category = models.ForeignKey(Category,
                                 verbose_name='category',
                                 on_delete=models.CASCADE,
                                 related_name='price',
                                 default=0)

    def __str__(self):
        return str(self.price)

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'


class RatingStar(models.Model):
    """ Rating Star table """
    value = models.SmallIntegerField('Value', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'


class Rating(models.Model):
    """ Rating table """
    ip = models.CharField('IP address', max_length=15)
    star = models.ForeignKey(RatingStar,
                             on_delete=models.CASCADE,
                             verbose_name='star')

    device = models.ForeignKey(Device,
                               on_delete=models.CASCADE,
                               verbose_name='device')

    def __str__(self):
        return f'{self.star} - {self.device}'

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Review(models.Model):
    """ Review table """
    email = models.EmailField()
    name = models.CharField('Name',max_length=100)
    text = models.TextField('Massage', max_length=5000)

    parent = models.ForeignKey('self', verbose_name='Parent',
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)

    device = models.ForeignKey(Device,
                               verbose_name='device',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.device}'

    class Meta:
        """ Plural or Singular """
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
