from rest_framework import serializers
from .models import Device, Price, Company, Category


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ('price','date')

# ------------------------------------------------------------------------

class DeviceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('name','description')

class DeviceDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='title',read_only=True)
    company = serializers.SlugRelatedField(slug_field='name',read_only=True)
    price = PriceSerializer(many=True)

    class Meta:
        model = Device
        exclude = ('url','id')


# ------------------------------------------------------------------------


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('url','id')


class CategoryDetailSerializer(serializers.ModelSerializer):
    device = DeviceListSerializer(many=True)

    class Meta:
        model = Category
        exclude = ('url','id')


# ------------------------------------------------------------------------


class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ('url','id')





