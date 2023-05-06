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
    path("estimate_price", views.estimate_price, name="estimate_price"),
    path("own_car_post", views.own_car_post, name="own_car_post"),
    path("watch_list/<int:user_id>", views.watch_list, name="watch_list"),

    #API path
    path("watch_list/api/<int:user_id>/", views.watch_list_api, name="watch_list_api"),
    path("watch_list/add/api/<int:user_id>/", views.add_watch_list_api, name="watch_list_api"),
    path("own_car_post/api/", views.own_car_post_api, name="own_car_post_api"),
    path("category/api/<int:category_id>/", views.category_each_brand_api, name="category_each_brand_api"),
    path("api/cars/", views.cars_api, name="cars"),
    path("api/pagnigation/", views.pagnigation_api, name="pagnigation"),
    path("api/categories/", views.categories_api, name="categories_api")
]