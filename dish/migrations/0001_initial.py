# Generated by Django 4.2.2 on 2024-07-15 22:01

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('sequence', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), size=None)),
                ('nationality', models.CharField(choices=[('US', 'American'), ('HU', 'Hungarian'), ('UA', 'Ukrainian'), ('IE', 'Irish'), ('IT', 'Italian'), ('GL', 'Worldwide')], default='GL', max_length=24)),
                ('level', models.CharField(choices=[('easy', 'Beginner'), ('medium', 'Intermediate'), ('moderate', 'Moderate'), ('hard', 'Advanced')], default='medium', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='DishIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandatory', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField()),
                ('unit', models.CharField(choices=[('pcs', 'Pieces'), ('g', 'Grams'), ('kg', 'Kilograms'), ('ml', 'Milliliters'), ('l', 'Liters'), ('tbsp', 'Tablespoons'), ('sp', 'Spoons')], default='pcs', max_length=24)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dish.dish')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredient.ingredient')),
            ],
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(through='dish.DishIngredient', to='ingredient.ingredient'),
        ),
    ]
