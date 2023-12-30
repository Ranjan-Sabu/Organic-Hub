from django.urls import path
from Accounts import views

urlpatterns = [
    path("register/", views.user_register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("vieworder/<int:id>", views.vieworder, name="vieworder"),
    path("editprofile/", views.editprofile, name="editprofile"),
    path("forgotPassword/", views.forgotPassword, name="forgotPassword"),
    path(
        "resetpassword_validate/<uidb64>/<token>/",
        views.resetpassword_validate,
        name="resetpassword_validate",
    ),
    path("resetpassword/", views.resetpassword, name="resetpassword"),
    path("changepassword/", views.changepassword, name="changepassword"),
]
