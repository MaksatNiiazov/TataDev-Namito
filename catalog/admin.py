from django.contrib import admin
from .models import Category, Product, Color, Size, Variant, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1  # Number of extra forms to display
    show_change_link = True


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Number of extra forms to display


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category__name']
    inlines = [VariantInline, ImageInline]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'hex_code']
    search_fields = ['name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'price']
    search_fields = ['product__name', 'color__name', 'size__name']
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant']
    search_fields = ['product__name']
