from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device, Category, Company
from .serializers import DeviceListSerializer, DeviceDetailSerializer, CategoryListSerializer, CompanyListSerializer, \
    CategoryDetailSerializer


class DeviceListView(APIView):

    def get(self,request):
        devices = Device.objects.all()
        serializer = DeviceListSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceDetailView(APIView):

    def get(self,request,pk):
        device = Device.objects.get(id = pk)
        serializer = DeviceDetailSerializer(device)
        return Response(serializer.data)

class CategoryListView(APIView):

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories,many=True)
        return Response(serializer.data)

class CategoryDetailView(APIView):

    def get(self,request,pk):
        category = Category.objects.get(id = pk)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)

class CompanyListView(APIView):

    def get(self, request):
        categories = Company.objects.all()
        serializer = CompanyListSerializer(categories, many=True)
        return Response(serializer.data)
