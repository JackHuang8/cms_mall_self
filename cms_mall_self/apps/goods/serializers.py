from rest_framework.serializers import ModelSerializer

from goods.models import Goods, GoodsCategory, GoodsAlbum


class GoodsSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


class GoodsCategorySerializer(ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsAlbumSerializer(ModelSerializer):
    class Meta:
        model = GoodsAlbum
        fields = '__all__'
