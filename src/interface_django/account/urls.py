# users/adapters/urls.py
from django.urls import path
from account.views import RegisterUserView, AuthenticateUserView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", AuthenticateUserView.as_view(), name="login"),
]
