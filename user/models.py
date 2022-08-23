from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('请输入邮箱')
        if not password:
            raise ValueError('请输入密码')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_superuser'] = True
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser):
    email = models.CharField(max_length=128, unique=True)
    phone_number = models.CharField(max_length=11, blank=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class VerificationCode(models.Model):
    email = models.CharField(max_length=128)
    code = models.CharField(max_length=6)
    add_time = models.DateTimeField(default=timezone.now)
