from django.urls import path
from . import views

urlpatterns = [
    path('', views.current_pals, name='current_pals'),
    path('new/country=<str:country>/gender=<str:gender>/age=<int:min_age>~<int:max_age>/lang=<str:lang_list>/', views.matching, name='matching'),
    path('query/', views.matching_query, name='matching_query'),
    path('<str:username>/confirm/', views.matching_confirm, name='matching_confirm'),
    path('<str:username>/confirm/yes/', views.send_match_request, name='send_match_request'),
    path('respond/request_id=<int:request_id>/verb=<str:verb>/', views.respond_match_request, name='respond_match_request'),
    path('remove?username=<str:username>/confirm', views.matching_remove_confirm, name='matching_remove_confirm'),
    path('remove?username=<str:username>/', views.matching_remove, name='matching_remove'),
]