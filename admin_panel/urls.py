from django.urls import path
from admin_panel import views

urlpatterns = [
    path("admin_panel/", views.admin_panel, name="admin_panel"),
    path("admin_category/", views.category, name="admin_category"),
    path("<add_Category/", views.add_Category, name="add_Category"),
    path("<str:slug>/<edit_Category/", views.edit_Category, name="edit_Category"),
    path("<str:slug>/delete_Category/", views.delete_Category, name="delete_Category"),
    path("admin_product/", views.products, name="admin_product"),
    path("<add_Product/", views.add_Product, name="add_Product"),
    path("<int:id>/<edit_Product/", views.edit_Product, name="edit_Product"),
    path("<int:id>/delete_Product/", views.delete_Product, name="delete_Product"),
    path("admin_users/", views.users, name="admin_users"),
    path("<int:id>/blockuser/", views.blockuser, name="blockuser"),
    path("<int:id>/usersprofile/", views.usersprofile, name="usersprofile"),
    path("admin_booking/", views.booking, name="admin_booking"),
]
