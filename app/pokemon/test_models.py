from django.test import TestCase

from .models import Pokemon
from .models import Type
from .models import Ability
from .service import ScoreService

class ModelTests(TestCase):

    def test_create_pokemon(self):
        pokemon = Pokemon.objects.create(
            pokemon_id=1,
            name='bulbasaur',
            height=7,
            weight=69,
            sprite_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png'
        )

        pokemon.types.set([Type.objects.create(name='grass'), Type.objects.create(name='poison')])
        pokemon.abilities.set([Ability.objects.create(name='overgrow'), Ability.objects.create(name='chlorophyll')])

        self.assertEqual(pokemon.__str__(), 'bulbasaur')

    def test_delete_pokemon(self):
        pokemon = Pokemon.objects.create(
            pokemon_id=2,
            name='ivysaur',
            height=10,
            weight=130,
            sprite_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png'
        )

        pokemon.types.set([Type.objects.create(name='grass'), Type.objects.create(name='poison')])
        pokemon.abilities.set([Ability.objects.create(name='overgrow'), Ability.objects.create(name='chlorophyll')])

    
        self.assertEqual(Pokemon.objects.filter(pk=pokemon.pk).count(), 1)

        pokemon.delete()

        self.assertFalse(Pokemon.objects.filter(pk=pokemon.pk).exists())

    def test_update_pokemon(self):
        pokemon = Pokemon.objects.create(
            pokemon_id=2,
            name='venosaur',
            height=10,
            weight=130,
            sprite_url='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png'
        )

        pokemon.types.set([Type.objects.create(name='grass'), Type.objects.create(name='poison')])
        pokemon.abilities.set([Ability.objects.create(name='overgrow'), Ability.objects.create(name='chlorophyll')])

        self.assertEqual(pokemon.name, 'venosaur')

        pokemon.name = 'venusaurius'
        pokemon.height = 52
        pokemon.weight = 2000
        pokemon.save()

        new_ability_names = ['Guts']
        new_abilities = Ability.objects.filter(name__in=new_ability_names)
        pokemon.abilities.set(new_abilities)

        new_type_names = ['grass']
        new_types = Type.objects.filter(name__in=new_type_names)
        pokemon.types.set(new_types)

        updated_pokemon = Pokemon.objects.get(id=pokemon.id)

        self.assertEqual(updated_pokemon.name, 'venusaurius')
        self.assertEqual(updated_pokemon.height, 52)
        self.assertEqual(updated_pokemon.weight, 2000)

    def test_score_pokemon (self):
        pokemon =  {
            "id": "74671547-4f58-4b87-a036-69c69996bc9a",
            "name": "charizard",
            "height": 17,
            "weight": 905,
            "pokemon_id": 6,
            "updated_at": "2024-05-13T18:52:51.408216Z",
            "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
            "types": [
                "fire",
                "flying"
            ],
            "abilities": [
                "blaze",
                "solar-power"
            ],
            "base_stats": {
                "hp": 78,
                "attack": 84,
                "defense": 78,
                "special_attack": 109,
                "special_defense": 85,
                "speed": 100
            }
        }
       
        self.assertEqual(ScoreService.calculate_score(pokemon)["pokemon_score"],253.6)