from rest_framework import serializers
from lots import models as lots_models
from auctions import models as auctions_models

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = lots_models.category
        fields = '__all__'


class LotSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    is_enabled = serializers.BooleanField(read_only=True)

    class Meta:
        model = lots_models.lot
        exclude = ('image', 'slug', 'user_id', 'info')
        read_only_fields = ('created_at','updated_at')

