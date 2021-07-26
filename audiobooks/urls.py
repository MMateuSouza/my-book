from django.urls import path
from audiobooks import views

app_name = 'audiobooks'

urlpatterns = [
    path('', views.index, name='index'),
]
