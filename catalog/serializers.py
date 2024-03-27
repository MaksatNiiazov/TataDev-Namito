from rest_framework import serializers
from .models import Category, Product, Color, Size, Variant, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Variant
        fields = ['id', 'product', 'color', 'size', 'price', 'images']

    @staticmethod
    def get_images(variant):
        images_qs = Image.objects.filter(variant=variant)
        return ImageSerializer(images_qs, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'variants']

    @staticmethod
    def get_variants(product):
        variants_qs = Variant.objects.filter(product=product)
        return VariantSerializer(variants_qs, many=True).data
