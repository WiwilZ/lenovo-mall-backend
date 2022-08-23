from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    mount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_mount(self, obj):
        return obj.goods.price * obj.count


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('related_user', 'goods', 'count', 'time_created')
