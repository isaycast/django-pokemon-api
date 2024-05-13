from rest_framework import serializers
from .models import Pokemon, Type, Ability, Stat

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']
    
    def to_internal_value(self, data):
        # Intenta obtener el tipo por nombre, si no existe, crea uno nuevo.
        try:
            return Type.objects.get(name=data['name'])
        except Type.DoesNotExist:
            return Type.objects.create(**data)

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['name']
    
    def to_internal_value(self, data):
        # Intenta obtener la habilidad por nombre, si no existe, crea una nueva.
        try:
            return Ability.objects.get(name=data['name'])
        except Ability.DoesNotExist:
            return Ability.objects.create(**data)

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

class PokemonSerializer(serializers.ModelSerializer):
    types = serializers.ListField(child=serializers.CharField(), write_only=True)
    abilities = serializers.ListField(child=serializers.CharField(), write_only=True)
    base_stats = StatSerializer(write_only=True)

    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'height', 'weight', 'pokemon_id', 'updated_at', 'sprite_url', 'types', 'abilities', 'base_stats']

    def validate(self, data):
        name = data.get('name')
        pokemon_id = data.get('pokemon_id')
        instance = self.instance  # 'instance' será None si es una creación

        # Validación para pokemon_id
        if pokemon_id is not None:
            # Comprobar si existe un Pokemon con el mismo pokemon_id que no sea esta instancia
            existing = Pokemon.objects.filter(pokemon_id=pokemon_id).exclude(pk=instance.pk if instance else None)
            if existing.exists():
                raise serializers.ValidationError({"pokemon_id": f"A Pokemon with Id {pokemon_id} already exists."})
    
        # Validación para name
        if name:
            # Comprobar si existe un Pokemon con el mismo name que no sea esta instancia
            existing = Pokemon.objects.filter(name=name).exclude(pk=instance.pk if instance else None)
            if existing.exists():
                raise serializers.ValidationError({"name": f"A Pokemon with name {name} already exists."})
        
        return data


    def create(self, validated_data):
        stats_data = validated_data.pop('base_stats', {})
        types_names = validated_data.pop('types', [])
        abilities_names = validated_data.pop('abilities', [])

        pokemon = Pokemon.objects.create(**validated_data)

        # Process each type name and get or create the Type instance
        for name in types_names:
            type_instance, _ = Type.objects.get_or_create(name=name)
            pokemon.types.add(type_instance)

        # Process each ability name and get or create the Ability instance
        for name in abilities_names:
            ability_instance, _ = Ability.objects.get_or_create(name=name)
            pokemon.abilities.add(ability_instance)

        # Create stat
        if stats_data:
            Stat.objects.create(pokemon=pokemon, **stats_data)

        return pokemon
    
    def update(self, instance, validated_data):
        types_data = validated_data.pop('types', [])
        abilities_data = validated_data.pop('abilities', [])
        stats_data = validated_data.pop('base_stats', {})  

        instance.name = validated_data.get('name', instance.name)
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.pokemon_id = validated_data.get('pokemon_id', instance.pokemon_id)
        instance.sprite_url = validated_data.get('sprite_url', instance.sprite_url)
        instance.save()

        if types_data:
            instance.types.clear()
            for type_name in types_data:
                type_instance, created = Type.objects.get_or_create(name=type_name)
                instance.types.add(type_instance)

        if abilities_data:
            instance.abilities.clear()
            for ability_name in abilities_data:
                ability_instance, created = Ability.objects.get_or_create(name=ability_name)
                instance.abilities.add(ability_instance)

        if stats_data:
            print(Stat.objects.filter(pokemon=instance).get())
            print("stats",stats_data)
            Stat.objects.filter(pokemon=instance).delete()
            if isinstance(stats_data, dict): 
                Stat.objects.create(pokemon=instance, **stats_data)
            else:
                raise TypeError(f"Expected a dictionary in stats data, got {type(stats_data)} instead")

        return instance


    def to_representation(self, instance):
        representation = super(PokemonSerializer, self).to_representation(instance)
        representation['types'] =  [type.name for type in instance.types.all()]
        representation['abilities'] = [abilitie.name for abilitie in instance.abilities.all()]
        stat_instance = instance.base_stats.first()
        representation['base_stats'] = StatSerializer(stat_instance).data if stat_instance else {}
        return representation
