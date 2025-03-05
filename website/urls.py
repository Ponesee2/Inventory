from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('supplier', views.supplier_list, name='supplier'),
    path('supplier_create', views.supplier_create, name='supplier_create'),
    path('suppliers/edit/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),  
    path('product_list', views.product_list, name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]