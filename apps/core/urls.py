from django.urls import path, re_path, include
from django.contrib import admin
from core.views import (
    IndexView,
    AuctionListView,
    MyAuctionListView,
    MyLotListView,
    AuctionView,
    NewLotView,
    NewAuctionView,
    NewBetView,
    NewCommentView,
    LotView,
    CheckView,
)

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('auctions/', AuctionListView.as_view(), name='auctions_list'),
    path('my_auctions/', MyAuctionListView.as_view(), name='my_auctions_list'),
    path('my_lots/', MyLotListView.as_view(), name='my_lots_list'),
    path('auctions/<pk>/', AuctionView.as_view(), name='auction'),
    path('lots/<pk>/', LotView.as_view(), name='lot'),
    path('new_lot/', NewLotView.as_view(), name='new_lot'),
    path('new_auction/', NewAuctionView.as_view(), name='new_auction'),
    path('new_bet/', NewBetView.as_view(), name='new_bet'),
    path('new_comment/', NewCommentView.as_view(), name='new_comment'),
    path('users/', include('users.urls', namespace='users')),
    path('check/', CheckView.as_view(), name='check'),
]
