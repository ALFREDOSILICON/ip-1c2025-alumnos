# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')


# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.

def home(request):
    images = []
    favourite_list = []
    images = services.getAllImages()

    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)
        favourite_names = [fav.name for fav in favourite_list]  # ← esto extrae solo los nombres
    else:
        favourite_names = []

    return render(request, 'home.html', { 
        'images': images, 
        'favourite_list': favourite_list,
        'favourite_names': favourite_names  # ← lo pasas al template
    })


# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        images = services.filterByCharacter(name)####
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')
      
    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        images = services.filterByType(type)#####
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

from .layers.utilities import translator
   
@login_required
def saveFavourite(request):
    if request.method == 'POST':
        fav = translator.fromTemplateIntoCard(request)  # Transformamos el POST en una Card
        fav.user = request.user  # Asignamos el usuario autenticado
        services.saveFavourite(fav)  # Guardamos con lógica de negocio
    return redirect('home')

@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)  # Trae lista de favoritos como cards
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })
  
@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')