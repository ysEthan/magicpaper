from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/<int:pk>/update/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    path('spu/', views.spu_list, name='spu_list'),
    path('spu/add/', views.spu_add, name='spu_add'),
    path('spu/<int:pk>/update/', views.spu_update, name='spu_update'),
    path('spu/<int:pk>/delete/', views.spu_delete, name='spu_delete'),

    path('sku/', views.sku_list, name='sku_list'),
    path('sku/add/', views.sku_add, name='sku_add'),
    path('sku/<int:pk>/update/', views.sku_update, name='sku_update'),
    path('sku/<int:pk>/delete/', views.sku_delete, name='sku_delete'),
] 