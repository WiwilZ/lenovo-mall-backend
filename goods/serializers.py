from rest_framework import serializers

from .models import Category, Brand, Goods, Picture


class BrandInCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    brands = BrandInCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = '__all__'

    def create(self, validated_data):
        goods, _ = Goods.objects.get_or_create(**validated_data)
        return goods


class BrandSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'

    def validate_category(self, category):
        Category.objects.get_or_create(name=category)
        return category

    def create(self, validated_data):
        brand, _ = Brand.objects.get_or_create(**validated_data)
        return brand
