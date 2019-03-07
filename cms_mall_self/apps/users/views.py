import random

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from redis.client import StrictRedis
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from users import serializers
from users.models import User, Area
from users.serializers import AreaSerializer, SubAreaSerializer, UserAddressSerializer


class SMSCodeView(APIView):
    def get(self, request, mobile):
        # 获取StrictRedis保存数据
        strict_redis = get_redis_connection('verify_codes')  # type:StrictRedis
        # 检查是否在60s内有发送记录
        sms_flag = strict_redis.get('sms_flag_' + mobile)
        if sms_flag:
            return Response({'msg': '短信发送过于频繁!'})
        # 生成短信验证码
        sms_code = random.randint(0, 999999)
        sms_code = '%06d' % sms_code
        # 使用云通讯发送短信验证码(Celery异步发送短信)
        print(sms_code)

        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code)

        # strict_redis.setex('sms_' + mobile, 5 * 60, sms_code)
        # strict_redis.setex('sms_flag_' + mobile, 60, 1)

        # 使用redis pipeline保存短信验证码(5分钟)
        pipeline = strict_redis.pipeline()
        pipeline.setex('sms_' + mobile, 5 * 60, sms_code)
        pipeline.setex('sms_flag_' + mobile, 60, 1)
        pipeline.execute()
        # 返回数据
        return Response({'msg': 'ok'})


class UsernameView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return Response({"username": username, 'count': count})


class UserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()


class AddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'user_id':request.user.id,
            'default_address_id':request.user.default_address_id,
            'addresses':serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        address = self.get_object()
        address.is_deleted = True
        address.save()

        return Response(status=204)

    # put /addresses/pk/status/
    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'msg': 'OK'}, status=200)
