from django.urls import path
from . import views

urlpatterns = [
    path('', views.current_pals, name='current_pals'),
    path('new', views.matching, name='new_match'),
]