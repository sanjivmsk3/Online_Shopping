"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
    path('',home,name='homepage'),
    path('product/<str:slug>/',product,name='product'),
    path('cat/<str:cat_slug>/',catview,name='cat'),
    path('search/',search,name='search'),
    path('cart/',ordersummery,name='cart'),
    path('add-to-cart/<str:slug>/',addtocart,name='add-to-cart'),
    path('remove-to-cart/<str:slug>/',ramovetocart,name='remove-to-cart'),
    path("checkout/",checkout,name="checkout"),
    path("add-coupon/",coupon_add,name="add-coupon"),
    path("remove-coupon/",removecoupon,name="remove-coupon"),
    path("makepayment/",makepayment,name="makepayment"),
    path("myorder/",myorder,name="myorder"),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
