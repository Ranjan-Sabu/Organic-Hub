from django.urls import path
from Accounts import views

urlpatterns = [
   path('', views.home,name='home'),
   path('register/',views.user_register,name='register'),
   path('login/',views.login_user,name='login'),
   path('logout/',views.user_logout,name='logout'),
   path('dashboard/',views.dashboard,name='dashboard'),
   path('forgotPassword/',views.forgotPassword,name='forgotPassword')
]