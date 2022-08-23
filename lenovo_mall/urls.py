"""lenovo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from goods.views import CategoryViewSet, BrandViewSet, GoodsViewSet
from order.views import OrderViewSet
from receiving_address.views import ReceivingAddressViewSet
from shopping_cart.views import ShoppingCartViewSet
from user.views import UserViewSet, VerificationCodeView

router = DefaultRouter()

router.register('users', UserViewSet)

router.register('receiving_addresses', ReceivingAddressViewSet)
router.register('verification-code', VerificationCodeView)

router.register('categories', CategoryViewSet)
router.register('brands', BrandViewSet)
router.register('goods', GoodsViewSet)

router.register('shopping_carts', ShoppingCartViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
