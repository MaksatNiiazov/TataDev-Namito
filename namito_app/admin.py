from django.contrib import admin
from .models import MetaInfo, MetaTag


class MetaTagInline(admin.TabularInline):
    model = MetaTag
    extra = 1


@admin.register(MetaInfo)
class MetaInfoAdmin(admin.ModelAdmin):
    list_display = ('data_for', 'slug')
    search_fields = ('data_for',)
    prepopulated_fields = {'slug': ('data_for',)}
    inlines = [MetaTagInline]


@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'meta_info')
    list_filter = ('meta_info',)
    search_fields = ('key', 'value', 'meta_info__data_for')
