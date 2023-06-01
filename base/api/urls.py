from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
  # MyTokenObtainPairView,
  TokenRefreshView,
)



urlpatterns = [
  path('', views.getRoutes),
  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('get_users/', views.getUsers, name='get_users'),
  path('get_profiles/', views.get_profiles, name='get_profiles'),
  path('add_user/', views.add_user, name='add_user'),
  path('get_user/<str:pk>/', views.get_user, name='get_user'),
  path('update_profile/<str:pk>/', views.update_profile, name='update_profile'),
  path('delete-user/<str:pk>/', views.delete_user, name='delete_user'),
]
