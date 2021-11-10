from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('change/<int:id>/', views.create, name='change'),
    path('delete/<int:id>/', views.delete, name='delete'),
]
