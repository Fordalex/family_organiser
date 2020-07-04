from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('find_users/', views.find_users, name='find_users'),
    path('create_request/<pk>', views.create_friend_request, name='friends'),
    path('requests/', views.requests, name='requests'),
]
