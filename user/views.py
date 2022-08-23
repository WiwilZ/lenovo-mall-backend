from django.core.mail import send_mail
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from lenovo_mall import settings
from .models import User, VerificationCode
from .serializers import UserSerializer, UserRegisterSerializer, UserResetPasswordSerializer, VerificationCodeSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        if self.action == 'reset_password':
            return UserResetPasswordSerializer
        return UserSerializer

    @action(methods=['patch'], detail=True)
    def reset_password(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


def send_verification_code_email(code, email):
    try:
        return send_mail(
            '【联想商城】验证码',
            f'您的验证码是【{code}】。如非本人操作，请忽略。',
            settings.EMAIL_FROM,
            [email],
            html_message=f'''
<div style="height: 400px;background-color: whitesmoke;margin: 0 auto;">
    <h2 style="text-align: center;padding-top: 15px;">【联想商城】</h2>
    <div style="margin: 0 auto;background-color: white;height: 200px;width: 500px;border: 1px solid rgb(172, 172, 172);">
        <h3 style="border-bottom: 1px solid  rgb(172, 172, 172);height: 40px;line-height: 40px;margin-top: 0;padding-left: 25px;">验证码</h3>
        <p style="margin-left: 25px;color:steelblue;">您好：{email}！欢迎使用【联想商城】！</p>
        <p style="margin-left: 25px;color:steelblue;">您的验证码是：{code}，请在五分钟内填写！</p>
        <p style="margin-left: 25px;color:gray;">@mall.wiwilz.cn</p>
    </div>
</div>'''
        )
    except Exception:
        return 0


class VerificationCodeView(CreateModelMixin, GenericViewSet):
    queryset = VerificationCode.objects.all()
    serializer_class = VerificationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        if send_verification_code_email(code, email) == 0:
            return Response({'msg': '邮件发送失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
