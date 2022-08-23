from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderSerializer, OrderUpdateSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        return OrderUpdateSerializer if self.action == 'update' else OrderSerializer
