from django.urls import path

from user.views import UserLoginView, UserRegistrationView

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),
]
