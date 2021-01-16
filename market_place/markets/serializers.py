""" Serializer for Django project """
from rest_framework import serializers
from .models import Device, Price, Company, Category


class PriceSerializer(serializers.ModelSerializer):
    """ Give every price from our Database"""
    class Meta:
        """ Which field and which model we want to display """
        model = Price
        fields = ('price', 'date')

# ------------------------------------------------------------------------

class DeviceListSerializer(serializers.ModelSerializer):
    """ Give every device form our database """
    # getting the last price
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        """ Get last price of current device """
        try:
            price = obj.price.latest('date')
            serializer = PriceSerializer(price)
            return serializer.data['price']
        except Exception as ex:
            return ex
    # 649

    class Meta:
        """ Which field and which model we want to display """
        model = Device
        fields = ('id', 'name', 'price')


class DeviceDetailSerializer(serializers.ModelSerializer):
    """ Give all information from specific device """
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # getting all price history
    price = PriceSerializer(many=True)

    class Meta:
        """ Which field and which model we want to display """
        model = Device
        exclude = ('url', 'id')


# ------------------------------------------------------------------------


class CategoryListSerializer(serializers.ModelSerializer):
    """ Give every category form our database """
    class Meta:
        """ Which field and which model we want to display """
        model = Category
        exclude = ('url',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    """ Give all information from specific category """
    device = DeviceListSerializer(many=True)

    class Meta:
        """ Which field and which model we want to display """
        model = Category
        exclude = ('url',)


class CategoryMinPriceSerializer(serializers.ModelSerializer):
    """ Give minimum price from every category """
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        """ Give last price of device """
        try:
            price = obj.price.order_by('price').first()
            serializer = PriceSerializer(price)
            return serializer.data['price']
        except Exception as ex:
            return ex

    class Meta:
        """ Which field and which model we want to display """
        model = Category
        exclude = ('url',)


class CategoryMaxPriceSerializer(serializers.ModelSerializer):
    """ Give maximum price from every category """

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        """ Give last price of device """
        try:
            price = obj.price.order_by('price').last()
            serializer = PriceSerializer(price)
            return serializer.data['price']
        except Exception as ex:
            return ex

    class Meta:
        """ Which field and which model we want to display """
        model = Category
        exclude = ('url',)

# ------------------------------------------------------------------------


class CompanyListSerializer(serializers.ModelSerializer):
    """ Give every company form our database """
    class Meta:
        """ Which field and which model we want to display """
        model = Company
        exclude = ('url',)


class CompanyDeviceDetailSerializer(serializers.ModelSerializer):
    """ Give all information from specific company """
    device = DeviceListSerializer(many=True)

    class Meta:
        """ Which field and which model we want to display """
        model = Company
        exclude = ('url',)
