# Generated by Django 3.0.4 on 2020-04-06 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20200406_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinstance',
            name='how_much_of_what',
            field=models.CharField(choices=[('PSC', 'Piece'), ('C', 'Cup'), ('ML', 'Ml'), ('L', 'L'), ('G', 'G'), ('KG', 'Kg'), ('SP', 'Spoon'), ('TSP', 'Teaspoon'), ('P', 'Pinch'), ('CLV', 'Clove')], max_length=10),
        ),
    ]
