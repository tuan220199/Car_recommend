from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("categories", views.categories, name="categories"),
    
    #API path
    path("api/category/<int:category_id>/", views.category_each_brand_api, name="category_each_brand_api"),
    path("api/cars/", views.cars_api, name="cars"),
    path("api/pagnigation/", views.pagnigation_api, name="pagnigation"),
    path("api/categories/", views.categories_api, name="categories_api")
]