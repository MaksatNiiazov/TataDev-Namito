from django.contrib import admin
from .models import Category, Product, Variant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    # filter_horizontal = ('tags',)


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'price')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__name', 'color', 'size')


@admin.register(Product)
class ProductWithVariantsAdmin(ProductAdmin):
    inlines = [VariantInline]


