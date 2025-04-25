from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("hello/", views.HelloView.as_view(), name="hello"),
    path("", views.UsersApiOverview, name="home"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("users/signup/", views.signup, name="signup"),
    path("users/login/", views.login_user, name="login user"),
    path("users/get/", views.get_user, name="view_users"),
    path("users/<int:pk>/update/", views.update_user, name="update_user"),
    # path("users/<int:pk>/delete/", views.delete_user, name="inactive user"),
    path("users/verify_auth/", views.verify_auth, name="verify auth"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
