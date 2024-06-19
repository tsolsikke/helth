from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.list_diary, name='list_diary'),
]
