from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category_each_brand, name="category_each_brand"),
    path("new_post", views.create_new_car_post, name="create_new_car_post"),

    #API path
    path("category/api/<int:category_id>/", views.category_each_brand_api, name="category_each_brand_api"),
    path("api/cars/", views.cars_api, name="cars"),
    path("api/pagnigation/", views.pagnigation_api, name="pagnigation"),
    path("api/categories/", views.categories_api, name="categories_api")
]