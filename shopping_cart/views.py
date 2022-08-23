from rest_framework.viewsets import ModelViewSet

from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartUpdateSerializer


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()

    def get_serializer_class(self):
        return ShoppingCartUpdateSerializer if self.action == 'update' else ShoppingCartSerializer
