from django.urls import path

from time_manager import views

app_name = 'time_manager'

urlpatterns = [
    path('categories/', views.category_index, name='category_index'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]