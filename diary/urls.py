from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.top, name='top'),
    path('<str:year>-<str:month>-<str:day>', views.top, name='top'),
    path('<str:year>-<str:month>', views.list_diary_month, name='list_diary_month'),
]
