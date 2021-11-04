from django.urls import path
from audiobooks import views

app_name = 'audiobooks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('change/<int:id>/', views.create, name='change'),
    path('<int:id>/', views.audiobooks, name='audiobooks'),
    path('<int:book_id>/recording', views.recording, name='new_recording'),
    path('<int:book_id>/recording/<int:audiobook_id>/change', views.recording, name='change_recording'),
]
