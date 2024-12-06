from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
] 