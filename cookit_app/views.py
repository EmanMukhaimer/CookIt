from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from . import models
from .models import User, Category, Instruction, Ingredient, Recipe, Review

# This function to display the main page of the website
def index(request):

    context = {
        "categories" : Category.objects.all()
    }
    
    return render(request, 'index.html', context)

# This function check if any user logged in 
def check_user_logged_in(request):
    if not request.session.get('id'):
        return redirect('/')
    try:
        user = User.objects.get(id=request.session['id'])
    except (User.DoesNotExist, KeyError) :
        return redirect('/')

# This function to display the home page of the website after the user has logged in
def home(request): 
    check_user_logged_in(request)
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/')

    context = {
        
        'user': user,
        "categories" : Category.objects.all()

    }
    return render(request, 'home.html', context)

# This function renders the register page
def register_page(request):
        return render(request, 'register.html')

# This function renders the login page
def login_page(request): 
    return render(request, 'login.html')


# This function validates the login and logs the user in
def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/home')

# This function validates the registration information and creates a new user
def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_page')
    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/home')

# This function clears the session data and redirects the user to the main page
def logout(request):
    request.session.clear()
    return redirect('/')

def my_reciepes(request):
    return render(request, "my_reciepes.html")

def all_reciepes(request):
    return render(request, "all_reciepes.html")

def category_reciepes(request): 
    return render(request, "category_reciepes.html")

def add_reciepe_page(request):
    return render(request, "add_reciepe.html")

def reciepe_details(request):
    return render(request, "reciepe_details.html")

def categories(request):
    context = {
        "categories" : Category.objects.all()
    }
    return render(request, "categories.html", context)



def add_recipe(name, preparation_time, cooking_time, serving_people, reciepe_img, user, categories, instructions, ingredients, reviews, request):
    recipe = Recipe.objects.create(name=name, preparation_time=preparation_time, cooking_time=cooking_time, serving_people=serving_people, reciepe_img=reciepe_img, user = User.objects.get(id=request.session['id']))
    recipe.categories.set(categories)
    recipe.save()

    for instruction in instructions:
        Instruction.objects.create(recipe=recipe, step_text=instruction['text'], step_number=instruction['number'])


    for ingredient in ingredients:
        Ingredient.objects.create(recipe=recipe, name=ingredient['name'], quantity=ingredient['quantity'])



    #for review in reviews:
        #Review.objects.create(recipe=recipe, user=review['user'], rating=review['rating'], review=review['review'])
