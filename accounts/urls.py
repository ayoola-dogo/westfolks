from django.urls import path
from .views import RegisterView, UserProfileView, UpdateAccountView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-account/<int:pk>', UpdateAccountView.as_view(), name='update-account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/edit_password.html'),
         name='password-reset'),
]
