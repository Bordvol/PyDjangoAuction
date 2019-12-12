from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from lots import models as lots_models
from .serializers import LotSerializer, CategorySerializer


class LotAPIView(ListAPIView):
    serializer_class = LotSerializer
    queryset = lots_models.lot.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('id', 'name')

    def get(self, request):
        lot_qs = lots_models.lot.objects.filter(is_enabled=True)
        serializer = LotSerializer(lot_qs, many=True)
        return Response(serializer.data)


class CategoryAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = lots_models.category.objects.all()

    def get(self, request):
        category_qs = lots_models.category.objects.all()
        serializer = CategorySerializer(category_qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)