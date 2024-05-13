import uuid
from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Pokemon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    pokemon_id = models.IntegerField()
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    weight = models.IntegerField()
    sprite_url = models.URLField()

    types = models.ManyToManyField(Type)
    abilities = models.ManyToManyField(Ability)

    def __str__(self):
        return self.name

class Stat(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='base_stats', on_delete=models.CASCADE)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()
    
    def __str__(self):
        return f"hp:{self.hp}, attack:{self.attack}, defense:{self.defense}, special_attack:{self.special_attack}, special_defense:{self.special_defense}, speed:{self.speed}"