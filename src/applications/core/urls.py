from django.urls import path
from .views import UserLoginView, UserRegistrationView, UserView, UserCSVUploadAPIView, UserFilter

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('user/', UserView.as_view(), name="current_user"),
    path('csv/', UserCSVUploadAPIView.as_view(), name='csv_upload'),
    path('filter/', UserFilter, name='user_filter')
]