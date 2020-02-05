from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.logging_in, name='login'),
    path('logout/', views.logging_out, name='logout'),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>', views.profile_other, name='profile_other'),
    path('settings/', views.settings, name='settings'),
    path('settings/info/', views.edit_info, name='edit_info'),
    path('settings/password/', views.edit_password, name='edit_password'),
    path('notifications/', views.notifications_view, name='notifications'),
]
