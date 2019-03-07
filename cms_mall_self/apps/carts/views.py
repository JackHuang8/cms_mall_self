import base64
import pickle
from django.shortcuts import render
from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.serializers import CartSerializer, CartGoodsSerializer
from goods.models import Goods


class CartView(APIView):
    def post(self, request):
        cart_seri = CartSerializer(data=request.data)
        cart_seri.is_valid(raise_exception=True)
        v_data = cart_seri.validated_data

        user = request.user
        if user.is_authenticated:
            strict_redis = get_redis_connection('cart')  # type:StrictRedis
            strict_redis.hincrby('cart_%s' % user.id, v_data['goods_id'], v_data['count'])
            if v_data['selected']:
                strict_redis.sadd('cart_selected_%s' % user.id, v_data['goods_id'])
            else:
                strict_redis.srem('cart_selected_%s' % user.id, v_data['goods_id'])
            return Response(v_data)
        else:
            return Response({'msg': '请先登陆!'}, status=401)
            #     cart = request.COOKIES.get('cart')
            #     if cart:
            #         cart = pickle.loads(base64.b64decode(cart.encode()))
            #     else:
            #         cart = {}
            #     cart['goods_id'] = {
            #         'count':v_data['goods_id'],
            #         'selected':v_data['selected']
            #     }
            #     cart = base64.b64encode(pickle.dump(cart)).decode()
            #     response = Response(v_data)
            #     response.set_cookie('cart', cart, 60*60*24*365)
            #     return response

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            strict_redis = get_redis_connection('cart')  # type:StrictRedis
            cart_dict = strict_redis.hgetall('cart_%s' % user.id)  # 字典
            cart_sel = strict_redis.smembers('cart_selected_%s' % user.id)  # 列表
            cart = {}
            for goods_id, count in cart_dict.items():
                cart[int(goods_id)] = {
                    'count': count,
                    'selected': goods_id in cart_sel
                }
            cart_queryset = Goods.objects.filter(id__in=cart.keys())
            for goods in cart_queryset:
                goods.count = cart[goods.id]['count']
                goods.selected = cart[goods.id]['selected']
            data = CartGoodsSerializer(cart_queryset, many=True).data
            return Response(data)
        else:
            return Response({'msg': '请先登陆!'}, status=401)

    def put(self, request):
        cart_seri = CartSerializer(data=request.data)
        cart_seri.is_valid(raise_exception=True)
        v_data = cart_seri.validated_data
        user = request.user
        if user.is_authenticated:
            strict_redis = get_redis_connection('cart')  # type:StrictRedis

            strict_redis.hset('cart_%s' % user.id, v_data['goods_id'], v_data['count'])

            if v_data['selected']:
                # cart_sel.append(cart_dict['goods_id'])
                strict_redis.sadd('cart_selected_%s' % user.id, v_data['goods_id'])
            else:
                strict_redis.srem('cart_selected_%s' % user.id, v_data['goods_id'])
            return Response(v_data)
        else:
            return Response({'msg': '请先登陆!'}, status=401)

    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            goods_id = request.data['goods_id']
            try:
                Goods.objects.get(id=goods_id)
            except Exception as e:
                print(e)
                return Response({'msg': '该商品不存在!'}, status=404)
            strict_redis = get_redis_connection('cart')  # type:StrictRedis
            strict_redis.hdel('cart_%s' % user.id, goods_id)
            strict_redis.srem('cart_selected_%s' % user.id, goods_id)
            return Response({'msg': 'ok'})
        else:
            return Response({'msg': '请先登陆!'}, status=401)


class SelecteAll(APIView):
    def put(self, request):
        user = request.user
        if user.is_authenticated:
            selected = request.data.get('selected')
            strict_redis = get_redis_connection('cart')  # type:StrictRedis
            if selected:
                cart_dict = strict_redis.hgetall('cart_%s' % user.id)  # 字典
                strict_redis.sadd('cart_selected_%s' % user.id, *cart_dict.keys())  # 列表
            else:
                strict_redis.delete('cart_selected_%s' % user.id)
            return Response({'msg': 'ok'})
        else:
            return Response({'msg': '请先登陆!'}, status=401)


class CartCountView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            strict_redis = get_redis_connection('cart')  # type:StrictRedis
            cart_dict = strict_redis.hgetall('cart_%s' % user.id)  # 字典
            total_count = 0
            for count in cart_dict.values():
                total_count += int(count)
            return Response({'total_count':total_count})
        else:
            return Response({'msg': '请先登陆!'}, status=401)

