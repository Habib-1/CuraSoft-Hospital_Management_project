from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import registerView,VerifyEmail ,CustomTokenObtainPairView,UserProfileView,ChangePasswordView,PasswordResetRequestView,PasswordResetConfirmView,LogoutView
urlpatterns = [
    path('login/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', registerView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
