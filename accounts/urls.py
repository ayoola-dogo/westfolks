from django.urls import path
from .views import RegisterView, UserProfileView, UpdateAccountView


app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-account/<int:pk>', UpdateAccountView.as_view(), name='update-account'),
]
