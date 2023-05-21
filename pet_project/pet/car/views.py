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
from joblib import load
import numpy as np

# Function is_superuser to check if the account is super user or not
#def is_superuser(user):
#    return user.is_superuser

# Load the model from the file
load_model = load('./saveModels/model.joblib')


def index(request):
    #Home page 
    current_user = request.user
    return render(request, "car/index2.html",{
        "user_id": current_user.id
    })


def categories(request):
    #Categories page
    return render(request, "car/categories.html")


def estimate_price(request):
    """
    This function estimates the price of a car based on user input and returns the result in a rendered
    HTML template.
    
    :param request: The request object represents the HTTP request that the user made to the server
    :return: The function `estimate_price` returns a rendered HTML template with the estimated car price
    and other input data if the request method is POST, and returns a rendered HTML template for the car
    price estimation form if the request method is not POST.
    """
    if request.method == "POST":

        # Retrieve dat from form
        mark_category_input = request.POST["mark_category"]
        model = request.POST["model"]
        year = float(request.POST["year"])
        mileage = float(request.POST["mileage"])
        engine_capacity = float(request.POST["engine_capacity"])
        transmission = request.POST["transmission"]
        drive = request.POST["drive"]
        hand_drive = request.POST["hand_drive"]
        fuel = request.POST["fuel"]
        image_url = request.POST["image_url"]
        
        x_data = np.array([year, mileage, engine_capacity]).reshape(1,-1)
        prediction = load_model.predict(x_data)
        return render(request, "car/estimate_price_result.html", {
            "model": model,
            "mark_category":mark_category_input,
            "year": year,
            "mileage": mileage,
            "engine_capacity": engine_capacity,
            "transmission": transmission,
            "drive": drive,
            "hand_drive":hand_drive,
            "fuel": fuel,
            "image_url": image_url,
            "prediction": round(prediction[0])
        })
    else:
        return render(request, "car/estimate_price_form.html")

@login_required
def watch_list(request, user_id):
    user_id = user_id
    return render(request, "car/watch_list.html",{
        "user_id": user_id
    })

@login_required
def add_watch_list_api(request, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Retrieve the user_id and car_id
    data = json.loads(request.body)
    user_watch_list_id = data['user_watch_list_id']
    car_id = data['car_id']

    # Find the user object and Car Object related to the id
    user_watch_list = User.objects.get(pk=user_watch_list_id)
    list_watch = Car.objects.get(pk=car_id)

    # Create a new pair of watch list between user and car item
    new_watch_list_pair = Watch_list(
        user_watch_list = user_watch_list,
        list_watch = list_watch
    )
    new_watch_list_pair.save()
    
    return JsonResponse({"message": "Add the car item to the watch list sucessfully"}, status=201)

@login_required
def remove_watch_list_api(request, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Retrieve the user_watch_list_id and car_id from the request body
    data = json.loads(request.body)
    user_watch_list_id = data['user_watch_list_id']
    car_id = data['car_id']

    try:
        # Get the Watch_list entry that matches the given conditions
        watch_list_entry = Watch_list.objects.get(
            user_watch_list_id=user_watch_list_id,
            list_watch_id=car_id
        )
    except Watch_list.DoesNotExist:
        return JsonResponse({"error": "Watch_list entry not found."}, status=404)

    # Delete the Watch_list entry
    watch_list_entry.delete()

    return JsonResponse({"message": "Watch_list entry removed successfully."}, status=200)

def watch_list_api_all(request, user_id):
    try:
        owner = request.user
        watch_list = Watch_list.objects.order_by("-id").filter(user_watch_list=owner)

        watch_list_list = []
        for item in watch_list:
            watch_list_list.append(item.list_watch.serialize())
        
        data = {
            'results': watch_list_list
        }

        return JsonResponse(data)
    except Exception as e:
        # Log the error to the console for debugging purposes.
        print(e)
        return JsonResponse({'error': 'Something went wrong.'})

def watch_list_api(request, user_id):
    try: 
        owner = request.user
        watch_list = Watch_list.objects.order_by("-id").filter(user_watch_list=owner)

        #Pagination 
        paginator = Paginator(watch_list, 2) # Show 2 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        watch_list_list = []
        for item in page_obj:
            watch_list_list.append(item.list_watch.serialize())

        data = {
            'results': watch_list_list,
            'count': math.ceil(paginator.count/2),
            'num_pages': page_number,
        }

        return JsonResponse(data)
    except Exception as e:
        # Log the error to the console for debugging purposes.
        print(e)
        return JsonResponse({'error': 'Something went wrong.'})
   

@login_required
def own_car_post(request):
    """
    The function returns a rendered HTML template with the current user's ID passed as a context
    variable.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, any data submitted in the request, and more
    :return: The function `own_car_post` returns a rendered HTML template `own_car_post.html` with a
    context dictionary containing the `id` of the current user.
    """
    current_user = request.user
    return render(request, "car/own_car_post.html",{
        "user_id": current_user.id
    })

def own_car_post_api(request):
    try:
        owner = request.user
        cars = Car.objects.order_by("-id").filter(owner=owner)

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

@login_required
def create_new_car_post(request):
    """
    This function creates a new car post object and saves it into the database based on the data
    retrieved from a form submitted via a POST request.
    
    :param request: The request object represents the HTTP request that the user made to the server
    :return: an HTTP response redirect to the "index" page if the request method is "POST", and
    rendering the "create_new_post.html" template if the request method is not "POST".
    """
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
    """
    This function takes a category ID as input and renders a category template with the category ID
    passed as a context variable.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user's session, the requested URL, and any submitted data
    :param category_id: The category ID is a parameter that is passed to the view function through the
    URL. It represents the ID of the category that the user wants to view. The view function takes this
    parameter and uses it to retrieve the relevant data from the database and render the appropriate
    template
    :return: This function returns a rendered HTML template "car/category.html" with a context
    dictionary containing the category_id variable.
    """
    category_id = category_id
    return render(request, "car/category.html",{
        "category_id": category_id
    })


def category_each_brand_api(request, category_id):
    """
    This function retrieves a list of cars belonging to a specific category and returns them in a
    paginated JSON response.
    
    :param request: The HTTP request object containing metadata about the request, such as headers and
    user information
    :param category_id: The ID of the category for which we want to retrieve the list of cars
    :return: A JSON response containing a list of serialized cars belonging to a specific category,
    along with pagination information such as the total count of cars and the current page number. If an
    exception occurs, a JSON response with an error message is returned.
    """
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

