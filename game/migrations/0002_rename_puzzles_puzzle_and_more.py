# Generated by Django 5.1.3 on 2024-12-01 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Puzzles',
            new_name='Puzzle',
        ),
        migrations.RenameModel(
            old_name='PuzzleDistinctSolutions',
            new_name='PuzzleDistinctSolution',
        ),
    ]
