# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    listaimagenes = transport.getAllImages()
    # 2) convertir cada img. en una card.
    listadoCARDS = []
    for elen in listaimagenes:
        card = translator.fromRequestIntoCard(elen)
        listadoCARDS.append(card)
    return listadoCARDS

    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.

   # pass

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():####
        
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        if type_filter.lower() in [t.lower() for t in card.types]:#####
        
            filtered_cards.append(card)

    return filtered_cards
   

from ..persistence import repositories

def saveFavourite(fav):
    # Verifica si ya está guardado por el usuario
    existing_fav = repositories.get_favourite_by_user_and_name(fav.user, fav.name)
    if existing_fav:
        # Ya existe, no guardar de nuevo
        return None  # Podrías devolver un mensaje si lo deseas

    return repositories.save_favourite(fav)



def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        favourite_list = repositories.get_all_favourites(user)  # Diccionarios
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite)  # Dict -> Card
            mapped_favourites.append(card)

        return mapped_favourites
      
##----------------------------------------------------------------------------
      
def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)