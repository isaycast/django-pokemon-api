from django.urls import path

from . import views

urlpatterns = [
    path("add", views.add_pokemon, name="add_pokemon"),
    path("get/id/<int:pokemon_id>/", views.get_pokemon, name="pokemon_detail"),
    path("score/<int:pokemon_id>", views.pokemon_score, name="cal_pokemon_score"),
    path("all-pokemons-registered", views.list_pokemon, name="pokemon_list"),
    path("find/name-id/<str:text>", views.find_pokemon_by_name_or_id, name="find_pokemon_by_name_or_id"),
    path("delete/<int:pokemon_id>", views.delete_pokemon, name="delete_pokemon"),
    path("update/<int:pokemon_id>", views.update_pokemon, name="update_pokemon"),
]