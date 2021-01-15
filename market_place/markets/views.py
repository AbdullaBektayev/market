""" View page """
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from .models import Device, Category, Company
from .serializers import DeviceListSerializer, DeviceDetailSerializer, \
    CategoryListSerializer,  CategoryDetailSerializer, \
    CategoryMinPriceSerializer, CategoryMaxPriceSerializer, \
    CompanyListSerializer,CompanyDeviceDetailSerializer

# ------------------------------------------------------------------------

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class DeviceListView(APIView):
    """ Give every device form our database """
    def get(self, request):
        """ If we have this info in cache then take from cache or from database"""
        if 'devices' in cache:
            serializer = cache.get('devices')
            return Response(serializer.data)
        else:
            devices = Device.objects.all()
            serializer = DeviceListSerializer(devices, many=True)
            cache.set('devices', serializer, timeout=CACHE_TTL)
            return Response(serializer.data)


class DeviceDetailView(APIView):
    """ Give all information from specific device """
    def get(self, request, pk):
        """ If we have this info in cache then take from cache or from database"""
        device_id = 'device' + '_' + str(pk)
        if device_id in cache:
            serializer = cache.get(device_id)
            return Response(serializer.data)
        else:
            device = Device.objects.get(id=pk)
            serializer = DeviceDetailSerializer(device)
            cache.set(device_id, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)

# ------------------------------------------------------------------------


class CategoryListView(APIView):
    """ Give every category form our database """

    def get(self, request):
        """ If we have this info in cache then take from cache or from database"""
        category = 'categories'
        if category in cache:
            serializer = cache.get(category)
            return Response(serializer.data)
        else:
            categories = Category.objects.all()
            serializer = CategoryListSerializer(categories, many=True)
            cache.set(category, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)


class CategoryDetailView(APIView):
    """ Give all information from specific category """
    def get(self, request, pk):
        """ If we have this info in cache then take from cache or from database"""
        category_id = 'categories' + '_' + str(pk)
        if category_id in cache:
            serializer = cache.get(category_id)
            return Response(serializer.data)
        else:
            category = Category.objects.get(id=pk)
            serializer = CategoryDetailSerializer(category)
            cache.set(category_id, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)


class CategoryMinPriceView(APIView):

    def get(self, request):
        """ If we have this info in cache then take from cache or from database"""
        category_min = 'categories_min'
        if category_min in cache:
            serializer = cache.get(category_min)
            return Response(serializer.data)
        else:
            category = Category.objects.all()
            serializer = CategoryMinPriceSerializer(category, many=True)
            cache.set(category_min, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)


class CategoryMaxPriceView(APIView):

    def get(self,request):
        """ If we have this info in cache then take from cache or from database"""
        category_max = 'categories_max'
        if category_max in cache:
            serializer = cache.get(category_max)
            return Response(serializer.data)
        else:
            category = Category.objects.all()
            serializer = CategoryMaxPriceSerializer(category, many=True)
            cache.set(category_max, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)

# ------------------------------------------------------------------------


class CompanyListView(APIView):
    """ Give every company form our database """

    def get(self, request):
        """ If we have this info in cache then take from cache or from database"""
        company = 'company'
        if company in cache:
            serializer = cache.get(company)
            return Response(serializer.data)
        else:
            companies = Company.objects.all()
            serializer = CompanyListSerializer(companies, many=True)
            cache.set(company, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)


class CompanyDeviceDetailView(APIView):
    """ Give all information from specific company """

    def get(self, request, pk):
        """ If we have this info in cache then take from cache or from database """
        company_id = 'company' + '_' + str(pk)
        if company_id in cache:
            serializer = cache.get(company_id)
            return Response(serializer.data)
        else:
            company = Company.objects.get(id=pk)
            serializer = CompanyDeviceDetailSerializer(company)
            cache.set(company_id, serializer, timeout=CACHE_TTL)
            return Response(serializer.data)
