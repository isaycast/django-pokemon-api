# Generated by Django 3.2 on 2024-05-10 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_alter_pokemon_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]