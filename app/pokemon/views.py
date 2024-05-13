from .service import PokemonApiService
from .service import ScoreService

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Pokemon
from .serializers import PokemonSerializer
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([AllowAny])
def add_pokemon(request):
    """Agrega un pokemon a la base de datos.
    Args:
        request (Request): Request de la petición.
    Returns:
        Response: Respuesta de la petición.
    Examples:
        >>> add_pokemon({
        ...     "pokemon_id": 1,
        ...     "name": "bulbasaur",
        ...     "height": 7,
        ...     "weight": 69,
        ...     "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        ...     "types": ["grass", "poison"],
        ...     "abilities": ["overgrow", "chlorophyll"],
        ...     "base_stats": { "hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45 }
        ... })
        
        {
        ...     "pokemon_id": 1,
        ...     "name": "bulbasaur",
        ...     "height": 7,
        ...     "weight": 69,
        ...     "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        ...     "types": ["grass", "poison"],
        ...     "abilities": ["overgrow", "chlorophyll"],
        ...     "base_stats": { "hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45 }
        ... }
    """
    serializer = PokemonSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_pokemon(request):
    """Lista todos los pokemons de la base de datos."""
    try:
        pokemons = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pokemon.DoesNotExist:
        return Response([], status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_pokemon(request, pokemon_id):
    """Obtiene un pokemon por su id.
    Args:
        pokemon_id (int): Id del pokemon.
    Returns:
        Response: Respuesta de la petición, array con un pokemon si este fue encontrado o un array vacio en el caso contrario.
    Examples:  
        >>> get_pokemon(1)
        {
            "pokemon_id": 1,
            "name": "bulbasaur",
            "height": 7,
            "weight": 69,
            "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "types": ["grass", "poison"],
            "abilities": ["overgrow", "chlorophyll"],
            "base_stats": { "hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45 }
        }
        """
    try:
        pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)
        serializer = PokemonSerializer(pokemon)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pokemon.DoesNotExist:
        return Response({'error': 'Pokemon not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def find_pokemon_by_name_or_id(request, text):
    """Obtiene un pokemon por su nombre o id.
    Args:
        text (str): Nombre o id del pokemon.
    Returns:
        Response: Respuesta de la petición, array con un pokemon si este fue encontrado o un array vacio en el caso contrario.
    Examples:
        >>> find_pokemon_by_name_or_id('bulbasaur')
        {
            "pokemon_id": 1,
            "name": "bulbasaur",
            "height": 7,
            "weight": 69,
            "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "types": ["grass", "poison"],
            "abilities": ["overgrow", "chlorophyll"],
            "base_stats": { "hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45 }
        }
    """
    try:
        pokemon_data = PokemonApiService.get_pokemon_data(text)
        print(pokemon_data)
        if not pokemon_data:
            return Response([], status=status.HTTP_404_NOT_FOUND)
        return Response([pokemon_data], status=status.HTTP_200_OK)
    except:
        return Response([], status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def pokemon_score(request, pokemon_id):
    """Calcula el puntaje de un pokemon.
    Args:
        pokemon_id (int): Id del pokemon.
    Returns:
        Response: Respuesta de la petición, json con el puntaje del pokemon si este fue encontrado o un json vacio en el caso contrario."""
    try:
        
        pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)
        serializer = PokemonSerializer(pokemon)
        pokemon_score = ScoreService.calculate_score(serializer.data)
        return Response(pokemon_score, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_pokemon(request, pokemon_id):
    """Elimina un pokemon de la base de datos.
    Args:
        pokemon_id (int): Id del pokemon.
    Returns:
        Response: Respuesta de la petición. 204 si el pokemon fue eliminado correctamente.
    Examples:
        >>> delete_pokemon(1)
        { 'detail': 'Pokemon deleted successfully' }
    """
    pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)    
    pokemon.delete()
    return Response({'detail': 'Pokemon deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_pokemon(request, pokemon_id):
    """Actualiza un pokemon de la base de datos.
    Args:
        pokemon_id (int): Id del pokemon.
    Returns:
        Response: Respuesta de la petición. 200 si el pokemon fue actualizado correctamente y un json con la informacion actualizada del pokemon.
    Examples:
        >>> update_pokemon(1)
        {
            "pokemon_id": 1,
            "name": "bulbasaur",
            "height": 7,
            "weight": 69,
            "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "types": ["grass", "poison"],
            "abilities": ["overgrow", "chlorophyll"],
            "base_stats": { "hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45 }
        }

        """
    pokemon = get_object_or_404(Pokemon, pokemon_id=pokemon_id)
    partial = request.method == 'PATCH'
    serializer = PokemonSerializer(pokemon, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)