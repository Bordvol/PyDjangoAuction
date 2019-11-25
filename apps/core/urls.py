from django.urls import path, re_path, include
from django.contrib import admin
from core.views import (
    IndexView,
    AuctionListView,
    AuctionView,
    NewLotView,
  #  auctions_list,
    auction,
    lot,
    category_list,
    category,
)

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('auctions/', AuctionListView.as_view(), name='auctions_list'),
    path('auctions/<pk>/', AuctionView.as_view(), name='auction'),
    path('new_lot/', NewLotView.as_view(), name='new_lot'),
    path('users/', include('users.urls', namespace='users')),
]
