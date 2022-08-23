from rest_framework import serializers

from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    mount = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def get_mount(self, obj):
        return obj.goods.price * obj.count

    def create(self, validated_data):
        try:
            shopping_cart = ShoppingCart.objects.get(related_user=validated_data['related_user'],
                                                     goods=validated_data['goods'])
            shopping_cart.count += validated_data['count']
            shopping_cart.save()
        except ShoppingCart.DoesNotExist:
            shopping_cart = ShoppingCart.objects.create(**validated_data)
        return shopping_cart


class ShoppingCartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('count',)
