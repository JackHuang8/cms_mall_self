import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User, Area, Address


# 创建序列化器
class CreateUserSerializer(serializers.ModelSerializer):
    # 指定额外字段password2，sms_code，allow
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.BooleanField(label='同意协议', write_only=True)

    token = serializers.CharField(label='登陆状态token', read_only=True)

    # 验证手机号validate_mobile(self, value)
    def validate_mobile(self, value):
        flag = re.match(r'^1[3-9]\d{9}$', value)
        if not flag:
            raise serializers.ValidationError('手机号格式错误')
        return value

    # 检验是否同意协议validate_allow(self, value)
    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('请同意用户协议')
        return value

    # 判断两次密码/短信验证码validate(self, attrs)
    def validate(self, attrs):
        # 判断两次密码
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')
        # 短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        redis_sms_code = redis_conn.get('sms_' + mobile)
        if not redis_sms_code:
            raise serializers.ValidationError('短信验证码已失效')
        if redis_sms_code.decode() != attrs['sms_code']:
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    # 创建用户create(self, validated_data)，并对密码加密User.objects.create_user(data）
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('username'),
                                        password=validated_data.get('password'), mobile=validated_data.get('mobile'))

        jwt_payload_handle = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handle = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handle(user)
        token = jwt_encode_handle(payload)

        user.token = token

        return user

    # 设置class Meta指定model、fields、extra_kwargs
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'token']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'min_length': 8,
                'max_length': 20,
                'write_only': True,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')


class UserAddressSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)

    province_id = serializers.IntegerField(label='省ID')
    city_id = serializers.IntegerField(label='市ID')
    district_id = serializers.IntegerField(label='区ID')

    def validate_mobile(self, value):
        flag = re.match(r'^1[3-9]\d{9}$', value)
        if not flag:
            raise serializers.ValidationError('手机号格式错误')
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')
