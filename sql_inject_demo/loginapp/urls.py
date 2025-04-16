from django.urls import path
from .views import login_view, register_view, update_password_view, search

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('update-password/', update_password_view, name='update_password'),
    path('search/', search, name='search')
]
