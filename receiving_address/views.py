from rest_framework.viewsets import ModelViewSet

from .models import ReceivingAddress
from .serializers import ReceivingAddressSerializer, ReceivingAddressUpdateSerializer


class ReceivingAddressViewSet(ModelViewSet):
    queryset = ReceivingAddress.objects.all()

    def get_serializer_class(self):
        return ReceivingAddressUpdateSerializer if self.action == 'update' else ReceivingAddressSerializer
