from django.urls import path
from rest_framework import routers
from .views import LotAPIView, CategoryAPIView

router = routers.SimpleRouter()

urlpatterns = [
   path('lot/', LotAPIView.as_view(), name='lot'),
   path('category/', CategoryAPIView.as_view(), name='category'),
]

urlpatterns += router.urls

