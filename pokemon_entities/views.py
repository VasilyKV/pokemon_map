import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from pokemon_entities.models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def get_image_url(image_field):
    if image_field:
        return image_field.url


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_entities_in_present = PokemonEntity.objects.exclude(
        appeared_at=None
    ).exclude(
        disappeared_at=None
    ).filter(
        appeared_at__lte=localtime()
    ).filter(
        disappeared_at__gte=localtime()
    )
    for pokemon_entity in pokemons_entities_in_present:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                get_image_url(pokemon_entity.pokemon.image))
        )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(get_image_url(pokemon.image)),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities_in_present = PokemonEntity.objects.filter(
        pokemon__id=pokemon_id
    ).exclude(
        appeared_at=None
    ).exclude(
        disappeared_at=None
    ).filter(
        appeared_at__lte=localtime()
    ).filter(
        disappeared_at__gte=localtime()
    )
    for pokemon_entity in pokemon_entities_in_present:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(
                get_image_url(pokemon_entity.pokemon.image))
        )

    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_description = {
        'title_ru': pokemon.title_ru,
        'img_url': request.build_absolute_uri(get_image_url(pokemon.image)),
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
    }
    if pokemon.previous_evolution:
        pokemon_description['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title_ru,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(get_image_url(pokemon.previous_evolution.image))
        }
    next_evolutions = pokemon.next_evolution.all()
    if next_evolutions:
        next_evolution = next_evolutions.first()
        pokemon_description['next_evolution'] = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(get_image_url(next_evolution.image))
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_description
    })
