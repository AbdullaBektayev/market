from rest_framework import serializers
from .models import Device, Price, Company, Category


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ('price','date')

# ------------------------------------------------------------------------

class DeviceListSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()
    # getting the last price
    def get_price(self, obj):
        try:
            price = obj.price.latest('date')
            serializer = PriceSerializer(price)
            return serializer.data
        except Exception as ex:
            return None

    class Meta:
        model = Device
        fields = ('id','name','price')

class DeviceDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='title',read_only=True)
    company = serializers.SlugRelatedField(slug_field='name',read_only=True)
    # getting all price history
    price = PriceSerializer(many=True)

    class Meta:
        model = Device
        exclude = ('url','id')


# ------------------------------------------------------------------------


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('url',)


class CategoryDetailSerializer(serializers.ModelSerializer):
    device = DeviceListSerializer(many=True)

    class Meta:
        model = Category
        exclude = ('url',)


# ------------------------------------------------------------------------


class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ('url',)

class CompanyDeviceDetailSerializer(serializers.ModelSerializer):
    device = DeviceListSerializer(many=True)

    class Meta:
        model = Company
        exclude = ('url',)




