from django.urls import path
from core.views import UserLoginView, UserRegistrationView, UserView, UserCSVUploadAPIView, UserFilterAPIView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('user/', UserView.as_view(), name="current_user"),
    path('csv/', UserCSVUploadAPIView.as_view(), name='csv_upload'),
    path('filter/', UserFilterAPIView.as_view({'get': 'list'}), name='user_filter')

]