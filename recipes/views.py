from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, Category
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from recipes.models import IngredientInstance
from recipes import help_functions as hp

def home(request):
    return render(request, 'Registration/home.html')


def index(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'name' : recipe.name,
        'difficulty' : recipe.difficulty,
        'image' : recipe.image,
        'step' : recipe.step_set.all().order_by('number'),
        'ingredients' : recipe.ingredientinstance_set.all(),
        'categories' : recipe.category_set.all(),
        'range_for_stars': range(recipe.difficulty),
        'range_for_rest_stars': range(recipe.difficulty+1, 6),
    }
    return render(request, 'recipes/detail.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'categories/index.html', context)


def category(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    context = {
        'category' : category,
        'recipes' : category.recipe.all()
    }
    return render(request, 'categories/detail.html', context)


def signup(request):  #przesada przerzucać do nowej aplikacji
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Registration/signup.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    query = '%' + query + '%'
    recipes = Recipe.objects.raw(
        """SELECT DISTINCT recipes_recipe.id, recipes_recipe.difficulty, recipes_recipe.name, recipes_recipe.image 
        FROM recipes_recipe 
        LEFT OUTER JOIN recipes_ingredientinstance_recipe ON (recipes_recipe.id = recipes_ingredientinstance_recipe.recipe_id) 
        INNER JOIN recipes_ingredientinstance ON recipes_ingredientinstance_recipe.ingredientinstance_id =  recipes_ingredientinstance.id
        INNER JOIN recipes_ingredient ON recipes_ingredientinstance.ingredient_id = recipes_ingredient.id
        WHERE (UPPER(recipes_recipe.name) LIKE UPPER(%s) 
        OR LOWER(recipes_ingredient.name) like %s)""", [query, query])
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/index.html', context)


def add_recipe(request):
    ii = IngredientInstance()
    context = {
        "measurement" : ii.return_measurement()
    }
    return render(request, 'recipes/add.html', context)


def add_recipe_form_sub(request):
    name = request.POST["name"]
    difficulty = request.POST["difficulty"]
    image = request.POST["image"]
    i = request.POST.get("i", False)
    step_list = []
    for j in range(int(i)):
        step_list.append(request.POST["step" + str(j)])
    k = request.POST.get("j", False)
    ing_list = []
    for j in range(int(k)):
        tuple = (request.POST["ing" + str(j)], request.POST["how_much" + str(j)], request.POST["select" + str(j)])
        ing_list.append(tuple)
    cat_i = request.POST.get("cat", False)
    cat_list = []
    for j in range(int(cat_i)):
        cat_list.append(request.POST["cat" + str(j)])
    hp.add_to_database(name, difficulty, image, step_list, ing_list, cat_list)
    return render(request, 'Adding/add_recipe.html')
"""Poprawić selecta, dodać krzyżyki do każdego stepu, kategorii przy dodawniu zamiast usuwać ostatni """