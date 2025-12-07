from django.urls import path
from .views import *

urlpatterns = [
    path("avatar/<uuid:user_id>.svg", avatar_svg, name="avatar-svg"),
    path("password-changed/",change_password,name="password-change-page"),
    path("check-email/", check_email_exists, name="check-email"),
]
