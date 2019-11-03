from django.urls import path, re_path
from django.contrib import admin
from apps.core.views import (
    index,
    auction_list,
    auction,
    lot,
    category_list,
    category,
)

app_name = 'core'

urlpatterns = [
    path('index/', index, name='index'),
    path('', index, name='index'),
    path('auctions/', auction_list, name='auction_list'),
    path('auctions/<pk>/', auction, name='auction'),
    path('lots/<pk>/', lot, name='lot'),
    path('categories/', category_list, name='category-list'),
    path('categories/<slug>/', category, name='category'),
    # re_path(r'^categories/(?P<slug>[\w-_]+)/$', func, name='category')
]
