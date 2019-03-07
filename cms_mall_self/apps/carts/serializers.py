from rest_framework import serializers

from goods.models import Goods


class CartSerializer(serializers.Serializer):
    goods_id = serializers.IntegerField(label='商品Id', write_only=True)
    count = serializers.IntegerField(label='商品数量', write_only=True)
    selected = serializers.BooleanField(label='是否选择', write_only=True)

    def validate(self, attrs):
        try:
            Goods.objects.get(id=attrs['goods_id'])
        except Exception as e:
            raise serializers.ValidationError('该商品不存在!')
        return attrs


class CartGoodsSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(label='商品数量')
    selected = serializers.BooleanField(label='是否选择')

    class Meta:
        model = Goods
        # fields = '__all__'
        fields = ['id','title','img_url','sell_price','count','selected']
