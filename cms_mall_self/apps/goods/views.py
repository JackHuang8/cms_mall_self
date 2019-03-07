from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import Goods, GoodsCategory, GoodsAlbum
from goods.serializers import GoodsSerializer, GoodsCategorySerializer, GoodsAlbumSerializer


class GoodsRecommentView(ListAPIView):
    serializer_class = GoodsSerializer
    queryset = Goods.objects.filter(is_red=1).order_by('-sales')[0:4]

    # def get_queryset(self):
    #     queryset = Goods.objects.filter(is_red=1).order_by('-sales')[0:4]
    #     return queryset

    # def get(self, request):
    #     goods_obj = Goods.objects.filter(is_red=1).order_by('-sales')[0:4]
    #     data = GoodsSerializer(goods_obj, many=True).data
    #
    #     return Response(data)


class GoodsCategoryView(APIView):
    def get(self, request):
        data = []
        b_category_queryset = GoodsCategory.objects.filter(parent_id=0)
        for b_obj in b_category_queryset:
            dict = {}
            dict['title'] = b_obj.title

            s_category_queryset = GoodsCategory.objects.filter(parent=b_obj)
            # s_category_queryset = b_obj.GoodsCategory_set.all()
            dict['goodscategory_set'] = GoodsCategorySerializer(s_category_queryset, many=True).data

            goods_queryset = Goods.objects.filter(category__in=s_category_queryset).order_by('-create_time')[0:5]
            dict['goods'] = GoodsSerializer(goods_queryset, many=True).data
            data.append(dict)
        return Response(data)


# class GoodsDaohangView(GenericAPIView):
#     serializer_class = GoodsCategorySerializer
#     queryset = GoodsCategory.objects.all()
class GoodsDaohangView(APIView):

    def get(self, request, pk):
        # category_obj = self.get_object()
        category_obj = GoodsCategory.objects.get(id=pk)
        data = {
            'title':category_obj.title
        }
        if category_obj.parent_id == 0:
            data['parent'] = None
        else:
            data['parent'] = GoodsCategorySerializer(category_obj.parent).data

        return Response(data)


# class GoodsListView(APIView):
#     def get(self, request, pk):
#         ordering = request.query_params['ordering']
#         category_obj = GoodsCategory.objects.get(id=pk)
#         if category_obj.parent_id == 0:
#             s_category_queryset = GoodsCategory.objects.filter(parent=category_obj)
#             goods_queryset = Goods.objects.filter(category__in=s_category_queryset).order_by(ordering)
#         else:
#             goods_queryset = Goods.objects.filter(category=category_obj).order_by(ordering)
#         data = GoodsSerializer(goods_queryset, many=True).data
#         return Response(data)

class GoodsListView(ListAPIView):
    serializer_class = GoodsSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_time', 'sales', 'sell_price')

    def get_queryset(self):
        pk = self.kwargs[self.lookup_field]
        try:
            category_obj = GoodsCategory.objects.get(id=pk)
        except Exception as e:
            return Response({'msg':'该类别不存在'},status=400)
        if category_obj.parent_id == 0:
            s_category_queryset = GoodsCategory.objects.filter(parent=category_obj)
            goods_queryset = Goods.objects.filter(category__in=s_category_queryset)
        else:
            goods_queryset = Goods.objects.filter(category=category_obj)
        return goods_queryset


class GoodsDetailView(APIView):
    def get(self, request, pk):
        try:
            goods_obj = Goods.objects.get(id=pk)
        except Exception as e:
            return Response({'msg':'该商品不存在'},status=400)
        data = GoodsSerializer(goods_obj).data

        album_queryset = GoodsAlbum.objects.filter(goods=goods_obj)
        data['goodsalbum_set'] = GoodsAlbumSerializer(album_queryset, many=True).data

        data['category'] = GoodsCategorySerializer(goods_obj.category).data
        data['category']['parent'] =GoodsCategorySerializer(goods_obj.category.parent).data

        return Response(data)
# class GoodsDetailView(RetrieveAPIView):
#     serializer_class = GoodsSerializer

