# Generated by Django 3.2 on 2024-05-09 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
