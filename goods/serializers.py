from rest_framework import serializers

from .models import Category, Brand, Goods, Picture


class BrandsInCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    brands = BrandsInCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class PicturesInGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('id', 'picture')


class GoodsInBrandSerializer(serializers.ModelSerializer):
    pictures = PicturesInGoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        exclude = ('brand',)


class BrandSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    goods = GoodsInBrandSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'

    def create(self, validated_data):
        brand, _ = Brand.objects.get_or_create(**validated_data)
        return brand


class GoodsSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(queryset=Brand.objects.all(), slug_field='name')
    pictures = PicturesInGoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        fields = '__all__'

    def create(self, validated_data):
        goods, _ = Goods.objects.get_or_create(**validated_data)
        return goods


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
