import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
import math


def index(request):
    return render(request, "car/index.html")

def categories(request):
    return render(request, "car/categories.html")

def category_each_brand_api(request, category_id):
    category = Category.objects.get(pk=category_id)
    cars = Car.objects.order_by("-id").filter(mark_category=category)

    #Pagination 
    paginator = Paginator(cars, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    car_list = []
    for car in page_obj:
        car_list.append(car.serialize())

    data = {
        'results': car_list,
        'count': math.ceil(paginator.count/10),
        'num_pages': page_number,
    }

    return JsonResponse(data)


def categories_api(request):
    categories = Category.objects.all()
    return JsonResponse([category.serialize() for category in categories], safe=False)


def pagnigation_api(request):
    """
    This function paginates a list of cars and returns a JSON response with the paginated data.
    It is noted that every page_obj has 10 car items 
    This API is special because generate api/${page} but it still can fetch that sample
    :return: a JSON response containing a list of serialized Car objects, the total count of cars
    divided by 10 (to determine the number of pages), and the current page number.
    """
    cars = Car.objects.order_by("-id").all()

    #Pagination 
    paginator = Paginator(cars, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    car_list = []
    for car in page_obj:
        car_list.append(car.serialize())

    data = {
        'results': car_list,
        'count': math.ceil(paginator.count/10),
        'num_pages': page_number,
    }

    return JsonResponse(data)


def cars_api(request):
    """
    This function retrieves all Car objects from the database and returns them as a JSON response.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any query parameters, headers, and more. In this case, it is used to retrieve a list
    of
    :return: A JSON response containing serialized data of all Car objects in the database, ordered by
    their ID in descending order.
    """
    cars = Car.objects.order_by("-id").all()
    return JsonResponse([car.serialize() for car in cars], safe=False)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "car/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "car/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "car/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "car/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "car/register.html")

