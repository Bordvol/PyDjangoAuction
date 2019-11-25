from django.urls import path
from users.views import (
    ProfileView,
    LoginView,
    LogoutView,
    RegisterView
)


app_name = 'users'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
