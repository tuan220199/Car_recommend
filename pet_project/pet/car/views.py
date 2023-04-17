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
from django.contrib.auth.decorators import user_passes_test

# Function is_superuser to check if the account is super user or not
def is_superuser(user):
    return user.is_superuser

def index(request):
    return render(request, "car/index.html")

def categories(request):
    return render(request, "car/categories.html")

@login_required
def create_new_car_post(request):
    if request.method == "POST":
        
        # current user
        current_user = request.user

        # Retrieve dat from form
        price = float(request.POST["price"])
        model = request.POST["model"]
        year = float(request.POST["year"])
        mileage = float(request.POST["mileage"])
        engine_capacity = float(request.POST["engine_capacity"])
        transmission = request.POST["transmission"]
        drive = request.POST["drive"]
        hand_drive = request.POST["hand_drive"]
        fuel = request.POST["fuel"]
        image_url = request.POST["image_url"]
        
        # Convert mark category from string into object in database
        mark_category_input = request.POST["mark_category"]
        categories = Category.objects.all()
        category_id = 0
        for category in categories:
            if mark_category_input == category.groups:
                category_id = category.id

        mark_category = Category.objects.get(pk=category_id)

        # Create a new car post object and save into database 
        new_car = Car(price=price, year=year, mileage=mileage, engine_capacity=engine_capacity, model=model, transmission=transmission, drive=drive, hand_drive=hand_drive, fuel=fuel, image_url=image_url, mark_category=mark_category, owner=current_user) 
        new_car.save()
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "car/create_new_post.html")



def category_each_brand(request, category_id):
    category_id = category_id
    return render(request, "car/category.html",{
        "category_id": category_id
    })


def category_each_brand_api(request, category_id):
    try:
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

    except Exception as e:
        # Log the error to the console for debugging purposes.
        print(e)
        return JsonResponse({'error': 'Something went wrong.'})

# This view "categories_api" only superuser account can log in
#@user_passes_test(is_superuser)
def categories_api(request):
    categories = Category.objects.all()
    return JsonResponse([category.serialize() for category in categories], safe=False)

#@user_passes_test(is_superuser)
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

# This view "cars_api" can only be accessed after the user log in
@login_required
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

