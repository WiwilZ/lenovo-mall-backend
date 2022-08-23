import random
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from order.serializers import OrderSerializer
from receiving_address.serializers import ReceivingAddressSerializer
from shopping_cart.serializers import ShoppingCartSerializer
from .models import User, VerificationCode


class UserSerializer(serializers.ModelSerializer):
    receiving_addresses = ReceivingAddressSerializer(many=True, read_only=True)
    shopping_carts = ShoppingCartSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'phone_number', 'date_joined', 'is_superuser',
            'receiving_addresses', 'shopping_carts', 'orders'
        )
        read_only_fields = ('email', 'date_joined')


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message='邮箱已被注册')])
    password = serializers.CharField(required=True, allow_blank=False, write_only=True)
    code = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=6, help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 }, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'code')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        code = data.pop('code')
        verify_records = VerificationCode.objects.filter(email=data['email']).order_by('-add_time')
        if not verify_records.exists():
            raise serializers.ValidationError('验证码不存在')

        last_record = verify_records[0]
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        if last_record.add_time < five_minutes_ago:
            raise serializers.ValidationError('验证码已过期')
        if last_record.code != code:
            raise serializers.ValidationError('验证码错误')
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserResetPasswordSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, allow_blank=False, min_length=6, max_length=6, help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'min_length': '验证码格式错误',
                                     'max_length': '验证码格式错误',
                                 }, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'code')
        # read_only_fields = ('email',)
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.pop('email')
        code = data.pop('code')
        verify_records = VerificationCode.objects.filter(email=email).order_by('-add_time')
        if not verify_records.exists():
            raise serializers.ValidationError('验证码不存在')

        last_record = verify_records[0]
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        if last_record.add_time < five_minutes_ago:
            raise serializers.ValidationError('验证码已过期')
        if last_record.code != code:
            raise serializers.ValidationError('验证码错误')
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class VerificationCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    code = serializers.HiddenField(default=f'{random.randint(0, 999999):0>6}')
    add_time = serializers.HiddenField(default=serializers.CreateOnlyDefault(timezone.now))

    class Meta:
        model = VerificationCode
        fields = ('email', 'code', 'add_time')

    def validate_email(self, email):
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if VerificationCode.objects.filter(add_time__gt=one_minute_ago, email=email).exists():
            raise serializers.ValidationError('请一分钟后再次发送')
        return email
