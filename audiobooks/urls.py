from django.urls import path
from audiobooks import views

app_name = 'audiobooks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('change/<int:id>/', views.create, name='change'),
    path('audiobooks/<int:id>/', views.audiobooks, name='audiobooks'),
    path('audiobooks/<int:id>/recording', views.recording, name='recording'),
]
