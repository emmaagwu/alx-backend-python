from django.urls import path
from .views import delete_user, signup_view
from django.contrib.auth import views as auth_views

app_name = "messaging" 

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="messaging/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("delete-account/", delete_user, name="delete_account"),
]
