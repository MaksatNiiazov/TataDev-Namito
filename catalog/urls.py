from django.urls import path

from catalog.views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView, ColorListView, \
    ColorDetailView, SizeListView, SizeDetailView, VariantListView, VariantDetailView, ImageListView, ImageDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('colors/', ColorListView.as_view()),
    path('colors/<int:pk>/', ColorDetailView.as_view()),
    path('sizes/', SizeListView.as_view()),
    path('sizes/<int:pk>/', SizeDetailView.as_view()),
    path('variants/', VariantListView.as_view()),
    path('variants/<int:pk>/', VariantDetailView.as_view()),
    path('images/', ImageListView.as_view()),
    path('images/<int:pk>/', ImageDetailView.as_view()),

]
