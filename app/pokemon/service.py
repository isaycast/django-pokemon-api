import requests

class PokemonApiService:
    @staticmethod
    def get_pokemon_data(pokemon_name_or_id):
        """Obtiene los datos de un pokemon de la pokeapi.
        Args:
            pokemon_name_or_id (str): Nombre o id del pokemon.
        Returns:
            dict: Diccionario con los datos del pokemon.
        Examples:
            >>> PokemonApiService.get_pokemon_data('bulbasaur')
            {'name': 'bulbasaur', 'pokemon_id': 1, 'height': 7, 'weight': 69, 'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png', 'base_stats': {'hp': 45, 'attack': 49, 'defense': 49, 'special_attack': 65, 'special_defense': 65, 'speed': 45}, 'types': ['grass', 'poison'], 'abilities': ['overgrow', 'chlorophyll']}
        """
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}")
            if response.status_code == 200:
                response = response.json()
                return {
                    'name': response['name'],
                    'pokemon_id': response['id'],
                    'height': response['height'],
                    'weight': response['weight'],
                    'sprite_url': response['sprites']['front_default'],
                    'base_stats':{
                        'hp': response['stats'][0]['base_stat'],
                        'attack': response['stats'][1]['base_stat'],
                        'defense': response['stats'][2]['base_stat'],
                        'special_attack': response['stats'][3]['base_stat'],
                        'special_defense': response['stats'][4]['base_stat'],
                        'speed': response['stats'][5]['base_stat'],
                    },
                    'types': [type_data['type']['name'] for type_data in response['types']],
                    'abilities': [ability_data['ability']['name'] for ability_data in response['abilities']],
                }
                
        except:
            return response.raise_for_status(500)




class ScoreService:
    PESO_TIPOS = 0.4
    PESO_ESTADISTICAS = 0.3
    PESO_HABILIDADES = 0.2
    PESO_OTROS = 0.1
	
    @staticmethod
    def calculate_score(pokemon_data):
        """Calcula el puntaje de un pokemon basado en sus tipos, estadísticas, habilidades y otros datos.
        Args:
            pokemon_data (dict): Diccionario con los datos del pokemon.
        Returns:
            dict: Diccionario con el puntaje del pokemon.
        Examples:
            >>> ScoreService.calculate_score({
            ...     "id": "74671547-4f58-4b87-a036-69c69996bc9a",
            ...     "name": "charizard",
            ...     "height": 17,
            ...     "weight": 905,
            ...     "pokemon_id": 6,
            ...     "updated_at": "2024-05-13T18:52:51.408216Z",
            ...     "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
            ...     "types": [
            ...         "fire",
            ...         "flying"
            ...     ],
            ...     "abilities": [
            ...         "blaze",
            ...         "solar-power"
            ...     ],
            ...     "base_stats": {
            ...         "hp": 78,
            ...         "attack": 84,
            ...         "defense": 78,
            ...         "special_attack": 109,
            ...         "special_defense": 85,
            ...         "speed": 100
            ...     }
            ... })
            {'pokemon_score': 253.6}
        """
        types_score = len(pokemon_data['types']) * ScoreService.PESO_TIPOS
        stats_score = sum([val for key, val in pokemon_data['base_stats'].items()]) * ScoreService.PESO_ESTADISTICAS
        abilities_score = len(pokemon_data['abilities']) * ScoreService.PESO_HABILIDADES
        other_score = (pokemon_data['height'] + pokemon_data['weight']) * ScoreService.PESO_OTROS
        score = types_score + stats_score + abilities_score + other_score

        return {"pokemon_score":round(score,2)}
    

        


        
