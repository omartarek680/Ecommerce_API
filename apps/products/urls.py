from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('<slug:slug>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
]
