from django.urls import path
from category import views

urlpatterns = [
   path('',views.home,name='home'),
   path('category/<slug:category_slug>/', views.home, name='category'),
]