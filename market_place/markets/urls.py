""" Urls of our application """
from django.urls import path
from . import views

urlpatterns = [
    path('device/', views.DeviceListView.as_view()),
    path('device/<int:pk>/', views.DeviceDetailView.as_view()),

# ------------------------------------------------------------------------

    path('category/', views.CategoryListView.as_view()),
    path('category/<int:pk>/', views.CategoryDetailView.as_view()),
    path('category/minprice/', views.CategoryMinPriceView.as_view(), name='minprice'),
    path('category/maxprice/', views.CategoryMaxPriceView.as_view(), name='maxprice'),

# ------------------------------------------------------------------------

    path('company/', views.CompanyListView.as_view()),
    path('company/<int:pk>', views.CompanyDeviceDetailView.as_view()),
]
